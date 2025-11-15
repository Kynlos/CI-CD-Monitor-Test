#!/usr/bin/env python3
"""
Advanced Auto Documentation Generator for CI/CD

Features:
1. Breaking change detection with auto-labeling
2. Changelog generation
3. Diff-aware documentation (only changed code)
4. Cross-file impact analysis
5. Smart PR comments
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'openai/gpt-oss-20b'  # Default (balanced speed and quality)
# MODEL = 'openai/gpt-oss-120b'  # More powerful but slower and more expensive

def extract_symbols_detailed(content):
    """Extract symbols with detailed information"""
    symbols = []
    
    # Functions with full signatures
    for match in re.finditer(r'^(export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*([^{;]+))?', content, re.MULTILINE):
        symbols.append({
            'type': 'function',
            'name': match.group(2),
            'params': match.group(3).strip() if match.group(3) else '',
            'returns': match.group(4).strip() if match.group(4) else 'void',
            'exported': bool(match.group(1)),
            'signature': match.group(0).strip()
        })
    
    # Classes
    for match in re.finditer(r'^(export\s+)?class\s+(\w+)', content, re.MULTILINE):
        symbols.append({
            'type': 'class',
            'name': match.group(2),
            'exported': bool(match.group(1)),
            'signature': match.group(0).strip()
        })
    
    # Interfaces
    for match in re.finditer(r'^(export\s+)?interface\s+(\w+)', content, re.MULTILINE):
        symbols.append({
            'type': 'interface',
            'name': match.group(2),
            'exported': bool(match.group(1)),
            'signature': match.group(0).strip()
        })
    
    return symbols

def detect_breaking_changes(old_content, new_content):
    """Detect breaking changes between versions"""
    if not old_content:
        return {'has_breaking': False, 'changes': []}
    
    old_symbols = {s['name']: s for s in extract_symbols_detailed(old_content)}
    new_symbols = {s['name']: s for s in extract_symbols_detailed(new_content)}
    
    breaking_changes = []
    
    # Removed exports
    for name, sym in old_symbols.items():
        if sym['exported'] and name not in new_symbols:
            breaking_changes.append({
                'type': 'removed',
                'symbol': name,
                'severity': 'BREAKING',
                'message': f"Removed exported {sym['type']}: {name}"
            })
    
    # Modified signatures
    for name in set(old_symbols.keys()) & set(new_symbols.keys()):
        old_sym = old_symbols[name]
        new_sym = new_symbols[name]
        
        if old_sym['exported'] and old_sym['signature'] != new_sym['signature']:
            # Check if parameters changed
            if old_sym.get('params') != new_sym.get('params'):
                breaking_changes.append({
                    'type': 'signature_change',
                    'symbol': name,
                    'severity': 'BREAKING',
                    'message': f"Modified signature of {name}",
                    'old': old_sym['signature'],
                    'new': new_sym['signature']
                })
    
    return {
        'has_breaking': len(breaking_changes) > 0,
        'changes': breaking_changes
    }

def get_git_diff(file_path):
    """Get git diff for a file"""
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'diff', 'HEAD~1', 'HEAD', file_path],
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return None

def analyze_cross_file_impact(files_data):
    """Analyze cross-file dependencies and impacts"""
    impacts = []
    
    all_symbols = {}
    for file_path, content in files_data.items():
        symbols = extract_symbols_detailed(content)
        for sym in symbols:
            all_symbols[sym['name']] = {
                'file': file_path,
                'type': sym['type'],
                'exported': sym['exported']
            }
    
    # Find references to changed symbols in other files
    for changed_file, content in files_data.items():
        for symbol_name, symbol_info in all_symbols.items():
            if symbol_info['file'] != changed_file:
                # Check if changed file references symbols from other files
                if re.search(rf'\b{symbol_name}\b', content):
                    impacts.append({
                        'changed_file': Path(changed_file).name,
                        'affects_file': Path(symbol_info['file']).name,
                        'symbol': symbol_name,
                        'type': symbol_info['type']
                    })
    
    return impacts

def generate_changelog_entry(file_path, old_content, new_content, breaking_info):
    """Generate changelog entry for this change"""
    old_symbols = {s['name']: s for s in extract_symbols_detailed(old_content)} if old_content else {}
    new_symbols = {s['name']: s for s in extract_symbols_detailed(new_content)}
    
    added = [name for name in new_symbols if name not in old_symbols and new_symbols[name]['exported']]
    removed = [name for name in old_symbols if name not in new_symbols and old_symbols[name]['exported']]
    modified = []
    
    for name in set(old_symbols.keys()) & set(new_symbols.keys()):
        if old_symbols[name]['signature'] != new_symbols[name]['signature']:
            modified.append(name)
    
    entry = []
    
    if breaking_info['has_breaking']:
        entry.append(f"### ⚠️ BREAKING CHANGES")
        for change in breaking_info['changes']:
            entry.append(f"- {change['message']}")
    
    if added:
        entry.append(f"### ✨ Added")
        for name in added:
            entry.append(f"- `{name}` ({new_symbols[name]['type']})")
    
    if modified and not breaking_info['has_breaking']:
        entry.append(f"### 🔄 Changed")
        for name in modified:
            entry.append(f"- `{name}` signature updated")
    
    if removed:
        entry.append(f"### 🗑️ Removed")
        for name in removed:
            entry.append(f"- `{name}` ({old_symbols[name]['type']})")
    
    return '\n'.join(entry) if entry else None

def generate_documentation(file_context, file_path):
    """Generate documentation using Groq API"""
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set")
        return "Documentation generation failed: No API key"
    
    prompt = f"""Generate comprehensive API documentation for this code file.

{file_context}

Include:
1. Overview - What this module does
2. Exports - All exported functions, classes, interfaces
3. Usage Examples - Practical examples for each export
4. Parameters - Describe each parameter
5. Return Values - What each function returns

Be thorough but concise. Format as GitHub-flavored Markdown."""

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
                    {'role': 'system', 'content': 'You are a technical documentation expert.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 2000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error generating docs: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def generate_impact_analysis(impacts, file_list):
    """Generate cross-file impact analysis"""
    if not impacts:
        return "No cross-file impacts detected."
    
    analysis = "## 🔗 Cross-File Impact Analysis\n\n"
    analysis += "These changes may affect other parts of the codebase:\n\n"
    
    by_file = {}
    for impact in impacts:
        key = impact['changed_file']
        if key not in by_file:
            by_file[key] = []
        by_file[key].append(impact)
    
    for file, file_impacts in by_file.items():
        analysis += f"### {file}\n"
        for imp in file_impacts:
            analysis += f"- References `{imp['symbol']}` from `{imp['affects_file']}`\n"
        analysis += "\n"
    
    return analysis

def main():
    print("Advanced Auto Documentation Generator")
    print("="*80)
    
    # Read changed files
    if not os.path.exists('changed_files.txt'):
        print("No changed files detected")
        sys.exit(0)
    
    with open('changed_files.txt', 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]
    
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py', '.go', '.rs', '.java', '.cpp', '.cc', '.c', '.h', '.hpp'}
    code_files = [f for f in changed_files if Path(f).suffix in code_extensions]
    
    if not code_files:
        print("No code files changed")
        sys.exit(0)
    
    print(f"Processing {len(code_files)} changed files\n")
    
    # Read files and get diffs
    files_data = {}
    file_diffs = {}
    old_contents = {}
    breaking_changes_detected = False
    all_breaking_changes = []
    
    for file_path in code_files:
        if not os.path.exists(file_path):
            print(f"  SKIP: {file_path} (deleted)")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            files_data[file_path] = content
            diff = get_git_diff(file_path)
            file_diffs[file_path] = diff
            
            # Try to get old version
            import subprocess
            try:
                old = subprocess.run(
                    ['git', 'show', f'HEAD~1:{file_path}'],
                    capture_output=True,
                    text=True
                )
                old_contents[file_path] = old.stdout if old.returncode == 0 else None
            except:
                old_contents[file_path] = None
            
            print(f"  OK: {file_path} ({len(content)} chars)")
        except Exception as e:
            print(f"  ERROR: {file_path} - {e}")
    
    if not files_data:
        print("\nNo files to process")
        sys.exit(0)
    
    # Detect breaking changes
    print("\n" + "="*80)
    print("ANALYZING CHANGES")
    print("="*80)
    
    for file_path, content in files_data.items():
        old_content = old_contents.get(file_path)
        breaking_info = detect_breaking_changes(old_content, content)
        
        if breaking_info['has_breaking']:
            breaking_changes_detected = True
            all_breaking_changes.extend(breaking_info['changes'])
            print(f"\n⚠️  BREAKING CHANGES in {Path(file_path).name}:")
            for change in breaking_info['changes']:
                print(f"   - {change['message']}")
    
    # Analyze cross-file impacts
    print("\n" + "="*80)
    print("CROSS-FILE IMPACT ANALYSIS")
    print("="*80)
    impacts = analyze_cross_file_impact(files_data)
    if impacts:
        print(f"Found {len(impacts)} cross-file dependencies")
        for imp in impacts[:5]:
            print(f"  - {imp['changed_file']} references {imp['symbol']} from {imp['affects_file']}")
    else:
        print("No cross-file impacts detected")
    
    # Create docs folder
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Generate documentation for each file
    print("\n" + "="*80)
    print("GENERATING DOCUMENTATION")
    print("="*80)
    
    doc_files_created = []
    changelog_entries = []
    
    for file_path, content in files_data.items():
        print(f"\n📝 {Path(file_path).name}...")
        
        # Generate diff-aware context
        old_content = old_contents.get(file_path, '')
        breaking_info = detect_breaking_changes(old_content, content)
        
        # Create diff-aware documentation
        diff_context = f"## {Path(file_path).name}\n\n"
        
        if old_content:
            diff_context += "### What Changed\n"
            diff = file_diffs.get(file_path, '')
            if diff:
                diff_context += f"```diff\n{diff[:1000]}\n```\n\n"
            diff_context += "### Current Code\n"
        
        diff_context += f"```typescript\n{content}\n```\n\n"
        
        # Generate documentation
        doc_content = generate_documentation(diff_context, file_path)
        
        # Save to docs folder
        doc_filename = Path(file_path).stem + '.md'
        doc_path = docs_dir / doc_filename
        
        with open(doc_path, 'w') as f:
            f.write(f"# {Path(file_path).name}\n\n")
            f.write(f"*Auto-generated from `{file_path}`*\n\n")
            
            if breaking_info['has_breaking']:
                f.write("## ⚠️ Breaking Changes\n\n")
                for change in breaking_info['changes']:
                    f.write(f"- **{change['type'].upper()}**: {change['message']}\n")
                    if 'old' in change and 'new' in change:
                        f.write(f"  - Before: `{change['old']}`\n")
                        f.write(f"  - After: `{change['new']}`\n")
                f.write("\n")
            
            f.write(doc_content)
        
        doc_files_created.append(str(doc_path))
        print(f"   ✓ Created {doc_path}")
        
        # Generate changelog entry
        changelog = generate_changelog_entry(file_path, old_content, content, breaking_info)
        if changelog:
            changelog_entries.append({
                'file': Path(file_path).name,
                'content': changelog
            })
    
    # Update CHANGELOG.md
    print("\n" + "="*80)
    print("UPDATING CHANGELOG")
    print("="*80)
    
    update_changelog(changelog_entries)
    
    # Generate impact analysis
    impact_report = generate_impact_analysis(impacts, code_files)
    
    # Generate smart PR comment
    print("\n" + "="*80)
    print("GENERATING PR COMMENT")
    print("="*80)
    
    pr_comment = generate_smart_pr_comment(
        code_files,
        doc_files_created,
        all_breaking_changes,
        impacts,
        changelog_entries
    )
    
    with open('doc_output.md', 'w') as f:
        f.write(pr_comment)
    
    # Create breaking changes label file if needed
    if breaking_changes_detected:
        with open('breaking_changes.txt', 'w') as f:
            f.write('true')
        print("\n⚠️  BREAKING CHANGES DETECTED - Will label PR")
    
    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80)
    print(f"  ✓ {len(doc_files_created)} documentation files")
    print(f"  ✓ Changelog updated")
    print(f"  ✓ PR comment generated")
    if breaking_changes_detected:
        print(f"  ⚠️  {len(all_breaking_changes)} breaking changes detected")

def update_changelog(entries):
    """Update or create CHANGELOG.md"""
    changelog_path = Path('CHANGELOG.md')
    
    # Read existing changelog
    if changelog_path.exists():
        with open(changelog_path, 'r') as f:
            existing = f.read()
    else:
        existing = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
    
    # Create new entry
    today = datetime.now().strftime('%Y-%m-%d')
    new_entry = f"## [{today}]\n\n"
    
    for entry in entries:
        new_entry += f"### {entry['file']}\n\n"
        new_entry += entry['content'] + "\n\n"
    
    # Insert after header
    lines = existing.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('## '):
            header_end = i
            break
    
    if header_end == 0:
        # No existing entries
        updated = existing + "\n" + new_entry
    else:
        # Insert before first entry
        updated = '\n'.join(lines[:header_end]) + '\n' + new_entry + '\n'.join(lines[header_end:])
    
    with open(changelog_path, 'w') as f:
        f.write(updated)
    
    print(f"  ✓ CHANGELOG.md updated with {len(entries)} entries")

def generate_smart_pr_comment(code_files, doc_files, breaking_changes, impacts, changelog_entries):
    """Generate comprehensive PR comment"""
    
    comment = "## 🤖 Auto-Generated Documentation & Analysis\n\n"
    
    # Breaking changes warning
    if breaking_changes:
        comment += "### ⚠️ BREAKING CHANGES DETECTED\n\n"
        comment += "This PR contains breaking changes that may affect users:\n\n"
        for change in breaking_changes:
            comment += f"- **{change['symbol']}**: {change['message']}\n"
            if 'old' in change and 'new' in change:
                comment += f"  ```diff\n  - {change['old']}\n  + {change['new']}\n  ```\n"
        comment += "\n"
    
    # Changed files summary
    comment += f"### 📝 Files Changed ({len(code_files)})\n\n"
    for file in code_files:
        comment += f"- `{Path(file).name}`\n"
    comment += "\n"
    
    # Changelog preview
    if changelog_entries:
        comment += "### 📋 Changelog Entries\n\n"
        for entry in changelog_entries:
            comment += f"**{entry['file']}**\n\n"
            comment += entry['content'] + "\n\n"
    
    # Impact analysis
    if impacts:
        comment += "### 🔗 Cross-File Impact Analysis\n\n"
        comment += f"These changes may affect {len(impacts)} other file(s):\n\n"
        
        by_changed = {}
        for imp in impacts:
            if imp['changed_file'] not in by_changed:
                by_changed[imp['changed_file']] = []
            by_changed[imp['changed_file']].append(imp)
        
        for changed_file, file_impacts in list(by_changed.items())[:3]:
            comment += f"**{changed_file}**\n"
            for imp in file_impacts[:5]:
                comment += f"- Uses `{imp['symbol']}` from `{imp['affects_file']}`\n"
            if len(file_impacts) > 5:
                comment += f"- ... and {len(file_impacts) - 5} more\n"
            comment += "\n"
    
    # Documentation links
    comment += "### 📚 Documentation Generated\n\n"
    for doc_file in doc_files:
        comment += f"- [`{Path(doc_file).name}`]({doc_file})\n"
    comment += "\n"
    
    # Actions required
    comment += "### ✅ Recommended Actions\n\n"
    if breaking_changes:
        comment += "- [ ] Update major version number\n"
        comment += "- [ ] Create migration guide\n"
        comment += "- [ ] Notify users of breaking changes\n"
    else:
        comment += "- [ ] Review generated documentation\n"
        comment += "- [ ] Update CHANGELOG.md if needed\n"
    
    if impacts:
        comment += "- [ ] Test affected files for regressions\n"
    
    comment += "\n---\n\n"
    comment += "*Documentation automatically generated. Ask questions about these changes below!*\n"
    
    return comment

if __name__ == '__main__':
    main()
