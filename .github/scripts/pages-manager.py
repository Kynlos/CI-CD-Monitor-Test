#!/usr/bin/env python3
"""
Intelligent GitHub Pages Documentation Manager

Features:
- LLM-powered agentic decision making
- Reads ALL existing pages to understand structure
- Decides: create new page, append to existing, or modify existing
- Professional documentation website generation
- Maintains consistent structure and navigation
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Import LLM wrapper
sys.path.insert(0, str(Path(__file__).parent))
from llm import get_client

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
MODEL = 'openai/gpt-oss-120b'  # Use more powerful model for better decisions

PAGES_DIR = Path('docs-site')
MAPPING_FILE = '.github/pages-mapping.json'


class PagesManager:
    def __init__(self):
        self.mapping = self.load_mapping()
        self.existing_pages = self.scan_existing_pages()
        
    def load_mapping(self) -> Dict:
        """Load persistent pages mapping"""
        if os.path.exists(MAPPING_FILE):
            with open(MAPPING_FILE, 'r') as f:
                return json.load(f)
        return {
            'version': '1.0',
            'last_updated': datetime.now().isoformat(),
            'file_to_page': {},
            'page_metadata': {},
            'site_structure': {
                'index.md': {'title': 'Home', 'category': 'root'},
                'api/': {'title': 'API Reference', 'category': 'api'},
                'modules/': {'title': 'Modules', 'category': 'modules'},
                'features/': {'title': 'Features', 'category': 'features'}
            }
        }
    
    def save_mapping(self):
        """Save mapping to disk"""
        self.mapping['last_updated'] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
        with open(MAPPING_FILE, 'w') as f:
            json.dump(self.mapping, indent=2, fp=f)
        print(f"✓ Saved mapping to {MAPPING_FILE}")
    
    def scan_existing_pages(self) -> Dict[str, str]:
        """Scan all existing documentation pages"""
        pages = {}
        
        if not PAGES_DIR.exists():
            print("ℹ️  Pages directory doesn't exist yet, will create")
            PAGES_DIR.mkdir(parents=True, exist_ok=True)
            return pages
        
        for md_file in PAGES_DIR.rglob('*.md'):
            relative_path = md_file.relative_to(PAGES_DIR)
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    pages[str(relative_path)] = content
            except Exception as e:
                print(f"⚠️  Could not read {relative_path}: {e}")
        
        print(f"✓ Found {len(pages)} existing documentation pages")
        for page in list(pages.keys())[:10]:
            print(f"  - {page}")
        if len(pages) > 10:
            print(f"  ... and {len(pages) - 10} more")
        
        return pages
    
    def make_intelligent_decision(self, source_file: str, doc_content: str) -> Tuple[str, str, str]:
        """
        LLM makes agentic decision about documentation placement
        
        Returns:
            (page_path, action, reasoning)
            action: 'create', 'append', 'modify'
        """
        print(f"\n🤔 Making intelligent decision for {source_file}...")
        
        # Build context for LLM
        existing_pages_summary = "\n".join([
            f"  {path}: {content[:200]}..." 
            for path, content in list(self.existing_pages.items())[:15]
        ])
        
        if not existing_pages_summary:
            existing_pages_summary = "  (No pages exist yet)"
        
        prompt = f"""You are a professional documentation architect. Analyze this code documentation and decide the BEST way to integrate it into the documentation website.

**Source File:** {source_file}

**Generated Documentation:**
```markdown
{doc_content[:2000]}
```

**Existing Documentation Pages:**
{existing_pages_summary}

**Site Structure:**
- index.md - Homepage
- api/ - API Reference pages
- guides/ - User guides and tutorials
- changelog/ - Version history

**Your Task:**
Decide ONE of these actions:

1. **CREATE** a new page
   - When: This is a completely new topic/module
   - Example: "api/payment-processing.md"

2. **APPEND** to existing page
   - When: Adding new functions/features to existing module
   - Example: Append to "api/authentication.md"

3. **MODIFY** existing page
   - When: Updating documentation for changed functions
   - Example: Update section in "api/authentication.md"

**Output Format (JSON only):**
{{
  "action": "create|append|modify",
  "page_path": "path/to/page.md",
  "reasoning": "Brief explanation",
  "section_title": "Section name (if append/modify)"
}}

Be smart about organization. Group related functionality together. Use clear, professional page names.
"""

        try:
            response = requests.post(
                GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': MODEL,
                    'messages': [
                        {'role': 'system', 'content': 'You are a documentation architect. Return ONLY valid JSON.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.2,
                    'max_tokens': 200
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result_text = response.json()['choices'][0]['message']['content'].strip()
                
                # Extract JSON from response
                result_text = result_text.strip('`').strip()
                if result_text.startswith('json'):
                    result_text = result_text[4:].strip()
                
                decision = json.loads(result_text)
                
                action = decision.get('action', 'create')
                page_path = decision.get('page_path', f"api/{Path(source_file).stem}.md")
                reasoning = decision.get('reasoning', 'Auto-generated')
                
                print(f"  ✓ LLM Decision: {action.upper()} → {page_path}")
                print(f"  📝 Reasoning: {reasoning}")
                
                return (page_path, action, reasoning)
            else:
                print(f"  ⚠️  LLM failed, using fallback")
                return self._fallback_decision(source_file)
        except Exception as e:
            print(f"  ⚠️  Error: {e}, using fallback")
            return self._fallback_decision(source_file)
    
    def _fallback_decision(self, source_file: str) -> Tuple[str, str, str]:
        """Fallback decision if LLM fails"""
        stem = Path(source_file).stem
        
        if 'auth' in source_file.lower():
            return ('api/authentication.md', 'create', 'Authentication module')
        elif 'database' in source_file.lower():
            return ('api/database.md', 'create', 'Database module')
        elif 'payment' in source_file.lower():
            return ('api/payments.md', 'create', 'Payment processing')
        elif 'email' in source_file.lower():
            return ('api/notifications.md', 'create', 'Email/notifications')
        else:
            return (f'api/{stem}.md', 'create', f'{stem} module')
    
    def apply_documentation_change(self, page_path: str, action: str, 
                                  doc_content: str, section_title: str = None) -> bool:
        """Apply documentation change based on action"""
        full_path = PAGES_DIR / page_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if action == 'create':
            return self._create_page(full_path, doc_content)
        elif action == 'append':
            return self._append_to_page(full_path, doc_content, section_title)
        elif action == 'modify':
            return self._modify_page(full_path, doc_content, section_title)
        else:
            print(f"⚠️  Unknown action: {action}")
            return False
    
    def _create_page(self, path: Path, content: str) -> bool:
        """Create a new documentation page"""
        print(f"  📄 Creating new page: {path}")
        
        # Add frontmatter for GitHub Pages
        page_content = f"""---
title: {path.stem.replace('-', ' ').title()}
layout: default
---

{content}
"""
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(page_content)
            print(f"  ✓ Created: {path}")
            return True
        except Exception as e:
            print(f"  ❌ Error creating page: {e}")
            return False
    
    def _append_to_page(self, path: Path, content: str, section_title: str) -> bool:
        """Append content to existing page"""
        print(f"  ➕ Appending to: {path}")
        
        if not path.exists():
            print(f"  ⚠️  Page doesn't exist, creating instead")
            return self._create_page(path, content)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                existing = f.read()
            
            # Add new section
            section_header = f"\n\n## {section_title}\n\n" if section_title else "\n\n"
            updated = existing + section_header + content
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(updated)
            
            print(f"  ✓ Appended to: {path}")
            return True
        except Exception as e:
            print(f"  ❌ Error appending: {e}")
            return False
    
    def _modify_page(self, path: Path, new_content: str, section_title: str) -> bool:
        """Intelligently modify existing page"""
        print(f"  ✏️  Modifying: {path}")
        
        if not path.exists():
            print(f"  ⚠️  Page doesn't exist, creating instead")
            return self._create_page(path, new_content)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                existing = f.read()
            
            # Use LLM to intelligently merge content
            merged = self._intelligent_merge(existing, new_content, section_title, path.name)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(merged)
            
            print(f"  ✓ Modified: {path}")
            return True
        except Exception as e:
            print(f"  ❌ Error modifying: {e}")
            return False
    
    def _intelligent_merge(self, existing: str, new_content: str, 
                          section_title: str, page_name: str) -> str:
        """Use LLM to intelligently merge new content into existing page"""
        print(f"    🧠 Using LLM to merge content...")
        
        prompt = f"""You are a documentation editor. Intelligently merge new documentation into an existing page.

**Existing Page ({page_name}):**
```markdown
{existing[:3000]}
```

**New Content to Integrate:**
```markdown
{new_content[:2000]}
```

**Section Focus:** {section_title or 'General update'}

**Your Task:**
1. If content is about NEW functions/features → ADD new section
2. If content UPDATES existing functions → REPLACE old section with new
3. If content is SIMILAR to existing → MERGE intelligently
4. Maintain existing frontmatter (---)
5. Keep consistent formatting and structure
6. Update "Last updated" timestamps

Return the COMPLETE merged page content in markdown format.
"""

        try:
            response = requests.post(
                GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': MODEL,
                    'messages': [
                        {'role': 'system', 'content': 'You are a documentation editor. Return clean markdown.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.3,
                    'max_tokens': 4000
                },
                timeout=45
            )
            
            if response.status_code == 200:
                merged = response.json()['choices'][0]['message']['content'].strip()
                
                # Clean up code fences if LLM wrapped it
                if merged.startswith('```markdown'):
                    merged = merged[11:]
                if merged.startswith('```'):
                    merged = merged[3:]
                if merged.endswith('```'):
                    merged = merged[:-3]
                
                print(f"    ✓ LLM merged content successfully")
                return merged.strip()
            else:
                print(f"    ⚠️  LLM merge failed, appending instead")
                return existing + f"\n\n## {section_title or 'Update'}\n\n" + new_content
        except Exception as e:
            print(f"    ⚠️  Error in LLM merge: {e}, appending instead")
            return existing + f"\n\n## {section_title or 'Update'}\n\n" + new_content
    
    def generate_index_page(self):
        """Generate/update main index.md and section index pages"""
        print("\n📑 Generating index pages...")
        
        # Collect all pages
        all_pages = {}
        for md_file in PAGES_DIR.rglob('*.md'):
            if md_file.name == 'index.md':
                continue
            relative = md_file.relative_to(PAGES_DIR)
            all_pages[str(relative)] = md_file
        
        # Generate API index
        api_pages = [p for p in all_pages.keys() if p.startswith('api/')]
        if api_pages:
            api_index = f"""---
title: API Reference
layout: default
category: API Reference
---

# API Reference

Low-level API documentation for all functions, classes, and interfaces.

## Available APIs

"""
            for page in sorted(api_pages):
                title = Path(page).stem.replace('-', ' ').title()
                api_index += f"- **[{title}]({Path(page).name})** - Technical API documentation\n"
            
            api_index += f"\n**Total:** {len(api_pages)} API pages\n\n"
            api_index += "---\n\n*Auto-generated by CI/CD Documentation System*\n"
            
            with open(PAGES_DIR / 'api' / 'index.md', 'w') as f:
                f.write(api_index)
            print(f"  ✓ Updated api/index.md with {len(api_pages)} pages")
        
        # Generate Modules index
        module_pages = [p for p in all_pages.keys() if p.startswith('modules/')]
        modules_index = f"""---
title: Modules
layout: default
category: Modules
---

# Modules

Module architecture and design documentation.

## Available Modules

"""
        if module_pages:
            for page in sorted(module_pages):
                title = Path(page).stem.replace('-', ' ').title()
                modules_index += f"- **[{title}]({Path(page).name})** - Module architecture and design\n"
            modules_index += f"\n**Total:** {len(module_pages)} modules\n\n"
        else:
            modules_index += "*No module documentation yet. Module-level docs will be auto-generated as the codebase evolves.*\n\n"
            modules_index += "Modules provide architectural overview, design decisions, and how different components interact.\n\n"
        
        modules_index += "---\n\n*Auto-generated by CI/CD Documentation System*\n"
        
        (PAGES_DIR / 'modules').mkdir(exist_ok=True)
        with open(PAGES_DIR / 'modules' / 'index.md', 'w') as f:
            f.write(modules_index)
        print(f"  ✓ Updated modules/index.md")
        
        # Generate Features index
        feature_pages = [p for p in all_pages.keys() if p.startswith('features/')]
        features_index = f"""---
title: Features
layout: default
category: Features
---

# Features

User-facing feature documentation and guides.

## Available Features

"""
        if feature_pages:
            for page in sorted(feature_pages):
                title = Path(page).stem.replace('-', ' ').title()
                features_index += f"- **[{title}]({Path(page).name})** - Feature guide and tutorial\n"
            features_index += f"\n**Total:** {len(feature_pages)} features\n\n"
        else:
            features_index += "*No feature documentation yet. Feature guides will be auto-generated as you develop.*\n\n"
            features_index += "Features provide user-facing documentation on how to use and configure the system.\n\n"
        
        features_index += "---\n\n*Auto-generated by CI/CD Documentation System*\n"
        
        (PAGES_DIR / 'features').mkdir(exist_ok=True)
        with open(PAGES_DIR / 'features' / 'index.md', 'w') as f:
            f.write(features_index)
        print(f"  ✓ Updated features/index.md")
        
        # Generate main index  
        index_content = f"""---
title: Home
layout: default
---

# Welcome to the Documentation

This is the auto-generated documentation website for the CI/CD Monitor Test project.

## Quick Links

- [API Reference](api/) - Complete API documentation for all modules
- [Guides](guides/) - Step-by-step tutorials and how-to guides
- [Changelog](changelog/) - Version history and notable changes

## Features

This documentation is:
- **Auto-generated** from code changes
- **Always up-to-date** with the latest code
- **Intelligently organized** by AI
- **Professionally formatted** with consistent styling

## About

This documentation is automatically generated and maintained by our intelligent CI/CD system with breaking change detection, code analysis, and security scanning.

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        index_path = PAGES_DIR / 'index.md'
        with open(index_path, 'w') as f:
            f.write(index_content)
        
        print(f"  ✓ Generated main index.md")


def process_docs_to_pages(doc_files: List[str]):
    """Process documentation files to GitHub Pages"""
    print("="*80)
    print("INTELLIGENT GITHUB PAGES MANAGER")
    print("="*80)
    
    manager = PagesManager()
    changes_made = []
    
    for doc_file in doc_files:
        if not os.path.exists(doc_file):
            continue
        
        print(f"\n📄 Processing: {doc_file}")
        
        # Read doc content
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine source file
        doc_path = Path(doc_file)
        source_file = doc_path.stem + '.ts'
        
        # Make intelligent decision
        page_path, action, reasoning = manager.make_intelligent_decision(source_file, content)
        
        # Apply change
        success = manager.apply_documentation_change(page_path, action, content)
        
        if success:
            changes_made.append({
                'source': source_file,
                'page': page_path,
                'action': action,
                'reasoning': reasoning
            })
            
            # Record mapping
            manager.mapping['file_to_page'][source_file] = page_path
            if page_path not in manager.mapping['page_metadata']:
                manager.mapping['page_metadata'][page_path] = {
                    'created': datetime.now().isoformat(),
                    'sources': []
                }
            if source_file not in manager.mapping['page_metadata'][page_path]['sources']:
                manager.mapping['page_metadata'][page_path]['sources'].append(source_file)
            manager.mapping['page_metadata'][page_path]['last_updated'] = datetime.now().isoformat()
            manager.mapping['page_metadata'][page_path]['last_action'] = action
    
    # Generate index page
    manager.generate_index_page()
    
    # Save mapping
    manager.save_mapping()
    
    # Generate summary
    summary = f"""# GitHub Pages Update Summary

**Changes Made:** {len(changes_made)}

"""
    
    for change in changes_made:
        summary += f"### {change['source']} → {change['page']}\n"
        summary += f"- **Action:** {change['action'].upper()}\n"
        summary += f"- **Reasoning:** {change['reasoning']}\n\n"
    
    with open('pages_summary.md', 'w') as f:
        f.write(summary)
    
    print("\n" + "="*80)
    print("GITHUB PAGES MANAGER COMPLETE")
    print("="*80)
    print(f"✓ {len(changes_made)} pages updated")
    print(f"✓ Mapping saved to {MAPPING_FILE}")
    print(f"✓ Site generated in {PAGES_DIR}")


if __name__ == '__main__':
    # Get changed source files
    changed_source_files = []
    if os.path.exists('changed_files.txt'):
        with open('changed_files.txt', 'r') as f:
            changed_source_files = [line.strip() for line in f if line.strip()]
    
    if not changed_source_files:
        print("No changed source files")
        sys.exit(0)
    
    # Map to doc files
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("No docs directory")
        sys.exit(0)
    
    doc_files_to_process = []
    for source_file in changed_source_files:
        source_path = Path(source_file)
        doc_filename = source_path.stem + '.md'
        doc_path = docs_dir / doc_filename
        
        if doc_path.exists():
            doc_files_to_process.append(str(doc_path))
    
    if not doc_files_to_process:
        print("No documentation files for changed sources")
        sys.exit(0)
    
    print(f"Found {len(doc_files_to_process)} documentation files\n")
    
    process_docs_to_pages(doc_files_to_process)
