#!/usr/bin/env python3
"""
Interactive PR Bot - Answer Questions

Responds to questions in PR comments using code context.
"""

import os
import sys
import re
from pathlib import Path
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
COMMENT_BODY = os.environ.get('COMMENT_BODY', '')
COMMENT_USER = os.environ.get('COMMENT_USER', 'user')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'openai/gpt-oss-20b'

def should_respond(comment_text):
    """Check if this comment is asking the bot a question"""
    # Ignore if it's the bot's own comment
    if comment_text.startswith('## 🤖'):
        return False
    
    # Check for question indicators
    question_indicators = [
        '?',  # Has a question mark
        '@bot',  # Mentions bot
        'explain',
        'what',
        'how',
        'why',
        'show me',
        'tell me'
    ]
    
    comment_lower = comment_text.lower()
    return any(indicator in comment_lower for indicator in question_indicators)

def load_changed_files():
    """Load the PR's changed files"""
    if not os.path.exists('pr_files.txt'):
        return []
    
    with open('pr_files.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def build_code_context(files):
    """Build code context from changed files"""
    context = "Code changes in this PR:\n\n"
    
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py'}
    
    for file_path in files:
        if not Path(file_path).suffix in code_extensions:
            continue
        
        if not os.path.exists(file_path):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limit file size to prevent token overflow
            if len(content) > 10000:
                lines = content.split('\n')[:200]
                content = '\n'.join(lines) + '\n... (file truncated)'
            
            context += f"## {Path(file_path).name}\n"
            context += f"```{Path(file_path).suffix[1:]}\n{content}\n```\n\n"
        except:
            continue
    
    return context

def answer_question(question, code_context):
    """Use Groq to answer the question"""
    if not GROQ_API_KEY:
        return "❌ Bot configuration error: No API key"
    
    prompt = f"""You are a helpful code review assistant. A developer asked a question about changes in a pull request.

{code_context}

Question from @{COMMENT_USER}:
{question}

Provide a clear, helpful answer based on the code shown above. If the question asks about something not visible in the code, say so. Be concise but thorough."""

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
                    {
                        'role': 'system',
                        'content': 'You are a helpful code review assistant. Answer questions about code changes clearly and concisely.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.3,
                'max_tokens': 1500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ Error generating response: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

def main():
    print("Interactive PR Bot - Answer Question")
    print("="*80)
    
    # Check if we should respond
    if not should_respond(COMMENT_BODY):
        print("Comment doesn't appear to be a question, skipping")
        sys.exit(0)
    
    print(f"Question from @{COMMENT_USER}:")
    print(f"  {COMMENT_BODY[:100]}...")
    
    # Load changed files
    changed_files = load_changed_files()
    print(f"\nPR has {len(changed_files)} changed files")
    
    if not changed_files:
        print("No files to analyze")
        sys.exit(0)
    
    # Build context
    print("Building code context...")
    code_context = build_code_context(changed_files)
    
    # Answer question
    print("Generating answer via Groq API...")
    answer = answer_question(COMMENT_BODY, code_context)
    
    # Format response
    response = f"""## 🤖 Bot Response

@{COMMENT_USER} asked:
> {COMMENT_BODY}

{answer}

---

*I'm an AI assistant analyzing the code changes in this PR. My responses are based on the changed files and may not have full context.*
"""
    
    # Save response
    with open('bot_response.md', 'w') as f:
        f.write(response)
    
    print("\n✓ Response generated")
    print("="*80)
    print(answer[:200] + "...")
    print("="*80)

if __name__ == '__main__':
    main()
