#!/usr/bin/env python3
"""
Smart Wiki Manager - Intelligently routes documentation to GitHub Wiki pages

Features:
1. Persistent mapping (never forgets where things go)
2. Reads existing wiki pages for smart routing decisions
3. LLM-powered intelligent categorization
4. Verification and consistency checks
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')  # owner/repo
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'openai/gpt-oss-120b'  # Use more powerful model for better content decisions

# Persistent mapping file (committed to repo)
MAPPING_FILE = '.github/wiki-mapping.json'

class WikiManager:
    def __init__(self):
        self.mapping = self.load_mapping()
        self.existing_pages = self.fetch_wiki_pages()
        
    def load_mapping(self) -> Dict:
        """Load persistent wiki mapping"""
        if os.path.exists(MAPPING_FILE):
            with open(MAPPING_FILE, 'r') as f:
                return json.load(f)
        return {
            'version': '1.0',
            'last_updated': datetime.now().isoformat(),
            'file_to_page': {},  # file_path -> wiki_page_name
            'page_metadata': {}  # wiki_page_name -> {category, description, files}
        }
    
    def save_mapping(self):
        """Save mapping to disk"""
        self.mapping['last_updated'] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
        with open(MAPPING_FILE, 'w') as f:
            json.dump(self.mapping, indent=2, fp=f)
        print(f"✓ Saved mapping to {MAPPING_FILE}")
    
    def fetch_wiki_pages(self) -> List[str]:
        """Fetch all existing wiki page names from GitHub"""
        if not GITHUB_TOKEN or not GITHUB_REPO:
            print("⚠️  GitHub credentials not set, cannot fetch wiki pages")
            return []
        
        try:
            # GitHub Wiki API endpoint
            owner, repo = GITHUB_REPO.split('/')
            url = f"https://api.github.com/repos/{owner}/{repo}/wiki/pages"
            
            headers = {
                'Authorization': f'token {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                pages = response.json()
                page_names = [p['title'] for p in pages]
                print(f"✓ Found {len(page_names)} existing wiki pages:")
                for page in page_names[:10]:
                    print(f"  - {page}")
                if len(page_names) > 10:
                    print(f"  ... and {len(page_names) - 10} more")
                return page_names
            elif response.status_code == 404:
                print("ℹ️  No wiki pages exist yet (wiki not initialized)")
                return []
            else:
                print(f"⚠️  Failed to fetch wiki pages: {response.status_code}")
                return []
        except Exception as e:
            print(f"⚠️  Error fetching wiki pages: {e}")
            return []
    
    def determine_wiki_page(self, file_path: str, file_content: str) -> str:
        """
        Intelligently determine which wiki page this file should go to.
        Uses LLM with context of existing pages and previous mappings.
        """
        # Check if we already have a mapping
        if file_path in self.mapping['file_to_page']:
            existing = self.mapping['file_to_page'][file_path]
            print(f"  📌 Using existing mapping: {file_path} → {existing}")
            return existing
        
        # Use LLM to make intelligent decision
        print(f"  🤔 Determining wiki page for {file_path}...")
        
        existing_pages_text = "\n".join([f"  - {p}" for p in self.existing_pages]) if self.existing_pages else "  (No pages yet)"
        
        previous_mappings_text = ""
        if self.mapping['file_to_page']:
            examples = list(self.mapping['file_to_page'].items())[:10]
            previous_mappings_text = "Previous mappings:\n" + "\n".join([f"  - {f} → {p}" for f, p in examples])
        
        prompt = f"""You are a documentation organizer. Determine the BEST wiki page name for this code file.

File: {file_path}

File content preview:
```
{file_content[:1000]}
```

Existing wiki pages:
{existing_pages_text}

{previous_mappings_text}

RULES:
1. Use existing pages when appropriate (prefer consistency)
2. Create new pages for distinct modules/domains
3. Group related functionality together
4. Use clear, descriptive names (e.g., "Authentication-API", "Database-Layer")
5. For files in same directory/domain, use same page
6. Use Title-Case-With-Dashes format

Examples:
- auth.ts → "Authentication-API"
- database.ts → "Database-Layer"  
- api/users.ts → "API-Users"
- utils/format.ts → "Utilities"
- test files → "Testing-Guide"

Return ONLY the wiki page name, nothing else."""

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
                        {'role': 'system', 'content': 'You are a documentation expert. Return only the wiki page name.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.1,
                    'max_tokens': 50
                },
                timeout=15
            )
            
            if response.status_code == 200:
                page_name = response.json()['choices'][0]['message']['content'].strip()
                # Clean up response (remove quotes, extra text)
                page_name = page_name.strip('"\'`').split('\n')[0].strip()
                print(f"  ✓ LLM decision: {file_path} → {page_name}")
                
                # Verify it's a valid page name
                if not page_name or len(page_name) > 100 or '/' in page_name:
                    # Fallback to simple naming
                    page_name = self._fallback_page_name(file_path)
                    print(f"  ⚠️  Invalid LLM response, using fallback: {page_name}")
                
                return page_name
            else:
                print(f"  ⚠️  LLM failed ({response.status_code}), using fallback")
                return self._fallback_page_name(file_path)
        except Exception as e:
            print(f"  ⚠️  Error calling LLM: {e}, using fallback")
            return self._fallback_page_name(file_path)
    
    def _fallback_page_name(self, file_path: str) -> str:
        """Fallback logic if LLM fails"""
        path = Path(file_path)
        
        # Check directory-based patterns
        parts = path.parts
        if 'auth' in file_path.lower():
            return 'Authentication-API'
        elif 'database' in file_path.lower() or 'db' in file_path.lower():
            return 'Database-Layer'
        elif 'api' in parts:
            # api/users.ts → API-Users
            return f"API-{path.stem.title()}"
        elif 'test' in file_path.lower():
            return 'Testing-Guide'
        elif 'util' in file_path.lower() or 'helper' in file_path.lower():
            return 'Utilities'
        else:
            # Default: use file name
            return path.stem.replace('_', '-').replace('.', '-').title()
    
    def update_wiki_page(self, page_name: str, content: str) -> bool:
        """Update or create a wiki page via GitHub API"""
        if not GITHUB_TOKEN or not GITHUB_REPO:
            print(f"  ⚠️  Cannot update wiki: missing credentials")
            return False
        
        try:
            owner, repo = GITHUB_REPO.split('/')
            
            # GitHub Wiki uses git, so we need to clone, update, push
            # For now, we'll use the simpler approach of just outputting the content
            # and letting the workflow handle the git operations
            
            # Create wiki output directory
            wiki_dir = Path('wiki_updates')
            wiki_dir.mkdir(exist_ok=True)
            
            # Save content to file (workflow will commit this)
            wiki_file = wiki_dir / f"{page_name}.md"
            
            # If page already exists, read it and append/update
            existing_content = ""
            if wiki_file.exists():
                with open(wiki_file, 'r') as f:
                    existing_content = f.read()
            
            # Merge content intelligently
            merged_content = self._merge_wiki_content(existing_content, content, page_name)
            
            with open(wiki_file, 'w') as f:
                f.write(merged_content)
            
            print(f"  ✓ Prepared wiki update: {wiki_file}")
            return True
            
        except Exception as e:
            print(f"  ❌ Error updating wiki: {e}")
            return False
    
    def _merge_wiki_content(self, existing: str, new: str, page_name: str) -> str:
        """Intelligently merge new content into existing wiki page using LLM"""
        if not existing:
            # New page
            header = f"# {page_name.replace('-', ' ')}\n\n"
            header += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            return header + new
        
        # Use LLM to intelligently merge
        print(f"    🧠 Using LLM to intelligently merge content...")
        
        prompt = f"""You are a wiki editor. Intelligently merge new documentation into existing wiki page.

**Existing Wiki Page:**
```markdown
{existing[:3000]}
```

**New Documentation:**
```markdown
{new[:2000]}
```

**Task:**
1. If documenting NEW functions/classes → ADD as new section
2. If UPDATING existing functions → REPLACE that section
3. If similar content exists → MERGE and deduplicate
4. Update "Last updated" timestamp to: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
5. Maintain wiki structure and formatting

Return the COMPLETE merged wiki page.
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
                        {'role': 'system', 'content': 'You are a wiki editor. Return clean markdown.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.3,
                    'max_tokens': 4000
                },
                timeout=45
            )
            
            if response.status_code == 200:
                merged = response.json()['choices'][0]['message']['content'].strip()
                
                # Clean up if LLM wrapped in code fences
                if merged.startswith('```markdown'):
                    merged = merged[11:]
                if merged.startswith('```'):
                    merged = merged[3:]
                if merged.endswith('```'):
                    merged = merged[:-3]
                
                print(f"    ✓ LLM merged content intelligently")
                return merged.strip()
            else:
                print(f"    ⚠️  LLM merge failed, using simple append")
                return self._simple_merge(existing, new)
        except Exception as e:
            print(f"    ⚠️  Error in LLM merge: {e}, using simple append")
            return self._simple_merge(existing, new)
    
    def _simple_merge(self, existing: str, new: str) -> str:
        """Simple merge fallback"""
        lines = existing.split('\n')
        
        # Update timestamp
        for i, line in enumerate(lines):
            if line.startswith('*Last updated:'):
                lines[i] = f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
                break
        
        return '\n'.join(lines) + '\n\n---\n\n' + new
    
    def record_mapping(self, file_path: str, page_name: str):
        """Record the file-to-page mapping"""
        self.mapping['file_to_page'][file_path] = page_name
        
        # Update page metadata
        if page_name not in self.mapping['page_metadata']:
            self.mapping['page_metadata'][page_name] = {
                'created': datetime.now().isoformat(),
                'files': []
            }
        
        if file_path not in self.mapping['page_metadata'][page_name]['files']:
            self.mapping['page_metadata'][page_name]['files'].append(file_path)
        
        self.mapping['page_metadata'][page_name]['last_updated'] = datetime.now().isoformat()
    
    def verify_consistency(self) -> bool:
        """Verify mapping is consistent and valid"""
        print("\n🔍 Verifying mapping consistency...")
        
        issues = []
        
        # Check for duplicate mappings
        page_files = {}
        for file_path, page_name in self.mapping['file_to_page'].items():
            if page_name not in page_files:
                page_files[page_name] = []
            page_files[page_name].append(file_path)
        
        # Verify metadata matches mappings
        for page_name, metadata in self.mapping['page_metadata'].items():
            if page_name not in page_files:
                issues.append(f"Metadata exists for {page_name} but no files mapped")
            else:
                mapped = set(page_files[page_name])
                recorded = set(metadata['files'])
                if mapped != recorded:
                    issues.append(f"Mismatch in {page_name}: mapped={len(mapped)}, recorded={len(recorded)}")
        
        if issues:
            print("⚠️  Consistency issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✓ Mapping is consistent")
            return True
    
    def generate_summary(self) -> str:
        """Generate a summary of wiki organization"""
        summary = "## 📚 Wiki Organization Summary\n\n"
        summary += f"**Total Pages:** {len(self.mapping['page_metadata'])}\n\n"
        
        for page_name, metadata in sorted(self.mapping['page_metadata'].items()):
            file_count = len(metadata['files'])
            summary += f"### {page_name}\n"
            summary += f"- **Files:** {file_count}\n"
            summary += f"- **Last Updated:** {metadata.get('last_updated', 'N/A')}\n"
            
            if file_count <= 5:
                summary += "- **Contains:**\n"
                for f in metadata['files']:
                    summary += f"  - `{f}`\n"
            else:
                summary += f"- **Contains:** {file_count} files\n"
            
            summary += "\n"
        
        return summary


def process_documentation_to_wiki(doc_files: List[str]):
    """
    Main function: Process documentation files and route to wiki pages
    """
    print("="*80)
    print("SMART WIKI MANAGER")
    print("="*80)
    
    manager = WikiManager()
    
    # Process each documentation file
    updates_made = []
    
    for doc_file in doc_files:
        if not os.path.exists(doc_file):
            print(f"⚠️  {doc_file} not found")
            continue
        
        print(f"\n📄 Processing: {doc_file}")
        
        # Read doc content
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine source file (doc filename is based on source)
        # e.g., docs/auth.md → auth.ts
        doc_path = Path(doc_file)
        source_file = doc_path.stem + '.ts'  # Assume .ts for now
        
        # Try to find actual source file
        possible_sources = [
            source_file,
            Path('src') / source_file,
            doc_path.stem + '.js',
            doc_path.stem + '.py'
        ]
        
        actual_source = None
        source_content = ""
        
        for possible in possible_sources:
            if os.path.exists(str(possible)):
                actual_source = str(possible)
                with open(actual_source, 'r') as f:
                    source_content = f.read()
                break
        
        if not actual_source:
            # Fallback: use doc filename
            actual_source = source_file
            print(f"  ⚠️  Source file not found, using: {actual_source}")
        
        # Determine wiki page
        page_name = manager.determine_wiki_page(actual_source, source_content)
        
        # Update wiki page
        success = manager.update_wiki_page(page_name, content)
        
        if success:
            # Record mapping
            manager.record_mapping(actual_source, page_name)
            updates_made.append({
                'file': actual_source,
                'page': page_name
            })
    
    # Save mapping
    manager.save_mapping()
    
    # Verify consistency
    manager.verify_consistency()
    
    # Generate summary
    summary = manager.generate_summary()
    
    # Save summary to output
    with open('wiki_summary.md', 'w') as f:
        f.write(summary)
        f.write("\n## Updates Made\n\n")
        for update in updates_made:
            f.write(f"- `{update['file']}` → [{update['page']}]\n")
    
    print("\n" + "="*80)
    print("WIKI MANAGER COMPLETE")
    print("="*80)
    print(f"✓ {len(updates_made)} wiki pages updated")
    print(f"✓ Mapping saved to {MAPPING_FILE}")
    print(f"✓ Summary saved to wiki_summary.md")
    
    return updates_made


if __name__ == '__main__':
    # Get list of CHANGED source files to determine which docs to process
    changed_source_files = []
    if os.path.exists('changed_files.txt'):
        with open('changed_files.txt', 'r') as f:
            changed_source_files = [line.strip() for line in f if line.strip()]
    
    if not changed_source_files:
        print("No changed source files detected")
        sys.exit(0)
    
    # Map source files to their doc files
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("No docs directory found")
        sys.exit(0)
    
    # Only process docs for files that actually changed
    doc_files_to_process = []
    for source_file in changed_source_files:
        source_path = Path(source_file)
        doc_filename = source_path.stem + '.md'
        doc_path = docs_dir / doc_filename
        
        if doc_path.exists():
            doc_files_to_process.append(str(doc_path))
    
    if not doc_files_to_process:
        print("No documentation files found for changed source files")
        sys.exit(0)
    
    print(f"Found {len(doc_files_to_process)} documentation files for changed sources")
    
    process_documentation_to_wiki(doc_files_to_process)
