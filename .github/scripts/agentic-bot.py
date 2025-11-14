#!/usr/bin/env python3
"""
Agentic PR Bot - Make Code Changes

Responds to action requests in PR comments and makes code changes.
Only works for PR author and assignees.
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
COMMENT_BODY = os.environ.get('COMMENT_BODY', '')
COMMENT_USER = os.environ.get('COMMENT_USER', 'user')
PR_AUTHOR = os.environ.get('PR_AUTHOR', '')
PR_ASSIGNEES = os.environ.get('PR_ASSIGNEES', '')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'openai/gpt-oss-120b'

def is_authorized(user):
    """Check if user is authorized to trigger actions"""
    if user == PR_AUTHOR:
        return True
    
    assignees = [a.strip() for a in PR_ASSIGNEES.split(',') if a.strip()]
    return user in assignees

def classify_intent(comment_text):
    """Classify if this is an action request and how confident we are"""
    
    prompt = f"""Classify this PR comment into one of three categories:

Comment: "{comment_text}"

Categories:
1. CLEAR_ACTION - User clearly wants code changes (e.g., "add comments to file.ts", "fix the bug in auth.ts")
2. POSSIBLE_ACTION - Might want changes but ambiguous (e.g., "this needs comments", "could use error handling")
3. QUESTION_ONLY - Just asking a question, no action requested

Also extract what action they want if it's an action request.

Respond ONLY with JSON:
{{
  "category": "CLEAR_ACTION|POSSIBLE_ACTION|QUESTION_ONLY",
  "action": "description of what to do (if applicable)",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}}"""

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
                    {'role': 'system', 'content': 'You are a PR intent classifier. Respond only with valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.1,
                'max_tokens': 200
            },
            timeout=30
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
    except:
        pass
    
    # Fallback
    return {'category': 'QUESTION_ONLY', 'action': None, 'confidence': 0}

def load_changed_files():
    """Load PR's changed files"""
    if not os.path.exists('pr_files.txt'):
        return []
    
    with open('pr_files.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def generate_code_changes(action_description, files):
    """Use LLM to generate code changes"""
    
    # Build context from changed files
    context = "PR Files:\n\n"
    file_contents = {}
    
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py'}
    
    for file_path in files:
        if Path(file_path).suffix not in code_extensions:
            continue
        
        if not os.path.exists(file_path):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_contents[file_path] = content
            context += f"## {file_path}\n```\n{content}\n```\n\n"
        except:
            continue
    
    if not file_contents:
        return None
    
    prompt = f"""You are a code editor bot. Make the requested changes to the code files.

{context}

User request: {action_description}

Generate the COMPLETE modified files. For each file you modify, output:

FILE: <filepath>
```
<complete file content with changes>
```

CHANGES:
- Brief description of what you changed

Only output files that need changes. Keep the same style and formatting as original code."""

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
                    {'role': 'system', 'content': 'You are a helpful code editing assistant. Make the requested changes and output complete modified files.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.2,
                'max_tokens': 4000
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"ERROR generating changes: {e}")
    
    return None

def parse_and_apply_changes(llm_output, original_files):
    """Parse LLM output and apply changes to files"""
    changes_made = []
    
    # Parse FILE: blocks
    file_blocks = re.finditer(r'FILE:\s*([^\n]+)\n```[^\n]*\n(.*?)```', llm_output, re.DOTALL)
    
    for match in file_blocks:
        file_path = match.group(1).strip()
        new_content = match.group(2)
        
        # Security: only modify PR files
        if file_path not in original_files:
            print(f"  SKIP: {file_path} (not in PR)")
            continue
        
        # Apply changes
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            changes_made.append(file_path)
            print(f"  ✓ Modified: {file_path}")
        except Exception as e:
            print(f"  ERROR modifying {file_path}: {e}")
    
    return changes_made

def commit_changes(files_changed, action_description):
    """Commit the changes"""
    if not files_changed:
        return None
    
    try:
        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
        
        # Add changed files
        for file_path in files_changed:
            subprocess.run(['git', 'add', file_path], check=True)
        
        # Commit
        commit_msg = f"bot: {action_description[:100]}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Push
        subprocess.run(['git', 'push'], check=True)
        
        # Get commit hash
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        commit_hash = result.stdout.strip()[:7]
        
        return commit_hash
    except Exception as e:
        print(f"ERROR committing: {e}")
        return None

def main():
    print("Agentic PR Bot - Code Change Agent")
    print("="*80)
    
    print(f"Comment from @{COMMENT_USER}:")
    print(f"  {COMMENT_BODY[:200]}")
    
    # Check authorization
    if not is_authorized(COMMENT_USER):
        print(f"\n⚠️  User @{COMMENT_USER} not authorized")
        print(f"   PR Author: {PR_AUTHOR}")
        print(f"   Assignees: {PR_ASSIGNEES}")
        
        response = f"""## 🔒 Authorization Required

@{COMMENT_USER}, only the PR author (@{PR_AUTHOR}) or assignees can request code changes.

If you'd like to suggest changes, please comment your suggestions and the author can implement them."""
        
        with open('bot_response.md', 'w') as f:
            f.write(response)
        
        sys.exit(0)
    
    print(f"✓ User authorized")
    
    # Classify intent
    print("\nClassifying intent...")
    intent = classify_intent(COMMENT_BODY)
    
    print(f"  Category: {intent['category']}")
    print(f"  Confidence: {intent.get('confidence', 0):.2f}")
    print(f"  Action: {intent.get('action', 'N/A')}")
    
    if intent['category'] == 'QUESTION_ONLY':
        print("\nNo action requested, skipping")
        sys.exit(0)
    
    # Get changed files
    changed_files = load_changed_files()
    print(f"\nPR has {len(changed_files)} files")
    
    if not changed_files:
        print("No files to modify")
        sys.exit(0)
    
    # If ambiguous, ask for confirmation
    if intent['category'] == 'POSSIBLE_ACTION':
        response = f"""## 🤔 Confirmation Needed

@{COMMENT_USER}, I think you want me to: **{intent['action']}**

Is this correct? If so, reply with:
- "yes" or "do it" to proceed
- "no" or "nevermind" to cancel

I'll wait for your confirmation before making changes."""
        
        with open('bot_response.md', 'w') as f:
            f.write(response)
        
        # Save pending action for next comment
        with open('pending_action.json', 'w') as f:
            json.dump({
                'action': intent['action'],
                'files': changed_files,
                'requested_by': COMMENT_USER
            }, f)
        
        print("\n⏳ Asking for confirmation")
        sys.exit(0)
    
    # Check for pending confirmation
    if os.path.exists('pending_action.json'):
        with open('pending_action.json', 'r') as f:
            pending = json.load(f)
        
        # Check if this is a confirmation
        confirmation_words = ['yes', 'do it', 'go ahead', 'proceed', 'confirm', 'ok', 'yeah']
        cancel_words = ['no', 'nevermind', 'cancel', 'stop']
        
        comment_lower = COMMENT_BODY.lower().strip()
        
        if any(word in comment_lower for word in cancel_words):
            os.remove('pending_action.json')
            response = f"## ❌ Cancelled\n\n@{COMMENT_USER}, action cancelled."
            with open('bot_response.md', 'w') as f:
                f.write(response)
            sys.exit(0)
        
        if any(word in comment_lower for word in confirmation_words):
            # Use the pending action
            intent['action'] = pending['action']
            changed_files = pending['files']
            os.remove('pending_action.json')
            print(f"\n✓ Confirmed action: {intent['action']}")
        else:
            # Not a clear confirmation, skip
            sys.exit(0)
    
    # Execute the action
    print("\n" + "="*80)
    print("GENERATING CODE CHANGES")
    print("="*80)
    
    llm_output = generate_code_changes(intent['action'], changed_files)
    
    if not llm_output:
        response = f"""## ❌ Failed to Generate Changes

@{COMMENT_USER}, I couldn't generate the requested changes. Please try rephrasing your request or make the changes manually."""
        
        with open('bot_response.md', 'w') as f:
            f.write(response)
        
        sys.exit(0)
    
    print("\nLLM Output Preview:")
    print(llm_output[:500] + "...")
    
    # Load original file contents for security check
    original_files = {}
    for file_path in changed_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                original_files[file_path] = f.read()
    
    # Apply changes
    print("\n" + "="*80)
    print("APPLYING CHANGES")
    print("="*80)
    
    files_modified = parse_and_apply_changes(llm_output, original_files)
    
    if not files_modified:
        response = f"""## ⚠️ No Changes Applied

@{COMMENT_USER}, I couldn't parse the generated changes. The LLM might have misunderstood the request."""
        
        with open('bot_response.md', 'w') as f:
            f.write(response)
        
        sys.exit(0)
    
    # Commit changes
    print("\n" + "="*80)
    print("COMMITTING CHANGES")
    print("="*80)
    
    commit_hash = commit_changes(files_modified, intent['action'])
    
    if commit_hash:
        # Generate success response
        response = f"""## ✅ Changes Applied

@{COMMENT_USER}, I made the requested changes: **{intent['action']}**

### Files Modified ({len(files_modified)})
{chr(10).join(f'- `{Path(f).name}`' for f in files_modified)}

### Commit
[{commit_hash}](../../commit/{commit_hash})

### What Changed
{llm_output.split('CHANGES:')[1] if 'CHANGES:' in llm_output else 'See commit for details'}

---

*If these changes aren't what you wanted, you can always revert this commit or ask me to modify them further.*"""
        
        print(f"\n✓ Committed as {commit_hash}")
    else:
        response = f"""## ❌ Commit Failed

@{COMMENT_USER}, I made the changes but couldn't commit them. Please check the action logs."""
    
    with open('bot_response.md', 'w') as f:
        f.write(response)
    
    print("\n✓ Response saved")

if __name__ == '__main__':
    main()
