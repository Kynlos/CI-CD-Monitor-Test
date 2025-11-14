#!/usr/bin/env python3
"""
Auto Documentation Generator for CI/CD

Reads changed files and sends to Groq API for documentation generation.
"""

import os
import sys
import json
import re
from pathlib import Path
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'llama-3.3-70b-versatile'  # Fast and capable



def build_file_context(files_data):
    """Build file context with full code"""
    context = "Code Files:\n\n"
    
    for file_path, content in files_data.items():
        context += f"## {Path(file_path).name}\n"
        context += f"```typescript\n{content}\n```\n\n"
    
    return context

def generate_documentation(file_context, file_list):
    """Call Groq API to generate documentation"""
    
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set")
        sys.exit(1)
    
    prompt = f"""Generate comprehensive API documentation for the following code files.

{file_context}

Files changed: {', '.join(file_list)}

Generate documentation that includes:
1. Overview of changes
2. All functions and classes
3. Usage examples for exports
4. Parameter descriptions
5. Return value documentation

Format as GitHub-flavored Markdown."""

    response = requests.post(
        GROQ_API_URL,
        headers={
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a technical documentation expert. Generate clear, comprehensive API documentation from code.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.3,
            'max_tokens': 2000
        }
    )
    
    if response.status_code != 200:
        print(f"ERROR: Groq API returned {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    data = response.json()
    return data['choices'][0]['message']['content']

def calculate_tokens(file_context):
    """Calculate token count"""
    total_tokens = len(file_context) // 4
    cost = total_tokens * (0.075 / 1_000_000)  # Groq pricing
    
    return {
        'tokens': total_tokens,
        'cost': cost
    }

def main():
    print("Auto Documentation Generator")
    print("="*80)
    
    # Read changed files
    if not os.path.exists('changed_files.txt'):
        print("No changed_files.txt found")
        sys.exit(0)
    
    with open('changed_files.txt', 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]
    
    # Filter to code files
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py'}
    code_files = [f for f in changed_files if Path(f).suffix in code_extensions]
    
    if not code_files:
        print("No code files changed")
        sys.exit(0)
    
    print(f"Processing {len(code_files)} changed files\n")
    
    # Read file contents
    files_data = {}
    
    for file_path in code_files:
        if not os.path.exists(file_path):
            print(f"  SKIP: {file_path} (deleted)")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            files_data[file_path] = content
            print(f"  OK: {file_path} ({len(content)} chars)")
        except Exception as e:
            print(f"  ERROR: {file_path} - {e}")
    
    if not files_data:
        print("\nNo files to process")
        sys.exit(0)
    
    # Build file context
    file_context = build_file_context(files_data)
    
    # Calculate tokens
    stats = calculate_tokens(file_context)
    print(f"\nToken Usage:")
    print(f"  Total: {stats['tokens']:,} tokens")
    print(f"  Cost: ${stats['cost']:.6f}")
    
    # Generate documentation
    print(f"\nGenerating documentation via Groq API ({MODEL})...")
    documentation = generate_documentation(file_context, code_files)
    
    print("\nGenerated Documentation:")
    print("="*80)
    print(documentation)
    print("="*80)
    
    # Create docs folder if it doesn't exist
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Save individual documentation files
    doc_files_created = []
    for file_path in code_files:
        if file_path in files_data:
            doc_filename = Path(file_path).stem + '.md'
            doc_path = docs_dir / doc_filename
            
            # Generate doc for this specific file
            file_doc = generate_documentation(
                f"## {Path(file_path).name}\n```typescript\n{files_data[file_path]}\n```",
                [file_path]
            )
            
            with open(doc_path, 'w') as f:
                f.write(f"# {Path(file_path).name} Documentation\n\n")
                f.write(f"*Auto-generated from {file_path}*\n\n")
                f.write(file_doc)
            
            doc_files_created.append(str(doc_path))
            print(f"  Created: {doc_path}")
    
    # Save for PR comment
    pr_comment = f"""## 🤖 Auto-Generated Documentation

**Changes detected in {len(code_files)} file(s)**

{documentation}

---

**Documentation files created:**
{chr(10).join(f'- `{Path(f).name}`' for f in doc_files_created)}

**Token Usage:**
- Total tokens: {stats['tokens']:,}
- Cost: ${stats['cost']:.6f}

*Documentation automatically generated from code changes.*
"""
    
    with open('doc_output.md', 'w') as f:
        f.write(pr_comment)
    
    print("\nDONE:")
    print("  - doc_output.md (for PR comment)")
    print(f"  - {len(doc_files_created)} files in docs/ folder")

if __name__ == '__main__':
    main()
