#!/usr/bin/env python3
"""
Centralized LLM client with retries, caching, and JSON coercion
Reduces duplication and adds robustness across all scripts
"""

import os
import re
import json
import time
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict, List, Any

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
CACHE_DIR = Path('.llm-cache')


class LLMClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GROQ_API_KEY
        self.cache_dir = CACHE_DIR
        self.cache_dir.mkdir(exist_ok=True)
    
    def call_chat(self,
                  model: str,
                  messages: List[Dict],
                  temperature: float = 0.3,
                  max_tokens: int = 2000,
                  response_format: str = 'text',  # 'text' or 'json'
                  timeout: int = 30,
                  use_cache: bool = True) -> Optional[str]:
        """
        Call LLM with retries, caching, and JSON coercion
        
        Returns:
            Response text or None on failure
        """
        if not self.api_key:
            print("⚠️  No API key configured")
            return None
        
        # Generate cache key
        cache_key = None
        if use_cache:
            prompt_hash = hashlib.sha256(
                f"{model}:{json.dumps(messages)}:{temperature}:{max_tokens}".encode()
            ).hexdigest()[:16]
            cache_key = self.cache_dir / f"{prompt_hash}.txt"
            
            if cache_key.exists():
                try:
                    with open(cache_key, 'r') as f:
                        cached = f.read()
                    print(f"  ✓ Using cached response ({prompt_hash})")
                    return cached
                except:
                    pass
        
        # Retry logic
        max_retries = 3
        backoff = 1
        
        for attempt in range(max_retries):
            try:
                # Build request payload
                payload = {
                    'model': model,
                    'messages': messages,
                    'temperature': temperature,
                    'max_tokens': max_tokens
                }
                
                # Add response_format if JSON is requested (CRITICAL for valid JSON)
                if response_format == 'json':
                    payload['response_format'] = {'type': 'json_object'}
                
                response = requests.post(
                    GROQ_API_URL,
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content'].strip()
                    
                    # JSON coercion if requested
                    if response_format == 'json':
                        result = self._coerce_to_json(result)
                    
                    # Cache successful response
                    if cache_key:
                        try:
                            with open(cache_key, 'w') as f:
                                f.write(result)
                        except:
                            pass
                    
                    return result
                
                elif response.status_code == 429 or response.status_code >= 500:
                    # Retry on rate limit or server errors
                    if attempt < max_retries - 1:
                        wait_time = backoff * (2 ** attempt)
                        print(f"  ⚠️  {response.status_code}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"  ❌ Failed after {max_retries} retries: {response.status_code}")
                        return None
                else:
                    print(f"  ❌ API error: {response.status_code}")
                    return None
            
            except requests.Timeout:
                if attempt < max_retries - 1:
                    wait_time = backoff * (2 ** attempt)
                    print(f"  ⚠️  Timeout, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"  ❌ Timeout after {max_retries} retries")
                    return None
            
            except Exception as e:
                print(f"  ❌ Error calling LLM: {e}")
                return None
        
        return None
    
    def _strip_code_fences(self, text: str) -> str:
        """Remove code fences from text"""
        return re.sub(r'```(?:json)?|```', '', text).strip()
    
    def _extract_balanced_json(self, text: str) -> Optional[str]:
        """Extract a balanced JSON object or array"""
        start = None
        for i, ch in enumerate(text):
            if ch in '{[':
                start = i
                break
        if start is None:
            return None
        
        stack = []
        for j in range(start, len(text)):
            if text[j] in '{[':
                stack.append(text[j])
            elif text[j] in '}]':
                if not stack:
                    return None
                open_ch = stack.pop()
                if (open_ch == '{' and text[j] != '}') or (open_ch == '[' and text[j] != ']'):
                    return None
                if not stack:
                    return text[start:j+1]
        return None
    
    def _sanitize_json_like(self, s: str) -> str:
        """Normalize smart quotes, fix multiline strings, and remove trailing commas"""
        # Normalize smart quotes
        s = s.replace('\u201c', '"').replace('\u201d', '"').replace('\u2019', "'")
        s = s.replace('\u200b', '')  # zero-width space
        
        # Fix unterminated strings by escaping newlines inside quoted strings
        # This handles the common LLM error of putting literal newlines in JSON strings
        lines = s.split('\n')
        fixed_lines = []
        in_string = False
        
        for i, line in enumerate(lines):
            # Count unescaped quotes in this line
            quote_count = 0
            j = 0
            while j < len(line):
                if line[j] == '"' and (j == 0 or line[j-1] != '\\'):
                    quote_count += 1
                j += 1
            
            # If odd number of quotes, we're starting or ending a string
            if quote_count % 2 == 1:
                in_string = not in_string
            
            # If we're in a string and this isn't the last line, escape the newline
            if in_string and i < len(lines) - 1:
                fixed_lines.append(line.rstrip() + '\\n')
            else:
                fixed_lines.append(line)
        
        s = ''.join(fixed_lines)
        
        # Remove trailing commas before } or ]
        s = re.sub(r',\s*([}\]])', r'\1', s)
        return s
    
    def _coerce_to_json(self, text: str) -> str:
        """Extract and validate JSON from LLM response"""
        text = self._strip_code_fences(text)
        
        # Try to parse as-is
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            pass
        
        # Try balanced block extraction
        snippet = self._extract_balanced_json(text) or text
        
        try:
            json.loads(snippet)
            return snippet
        except json.JSONDecodeError:
            pass
        
        # Sanitize and try again
        sanitized = self._sanitize_json_like(snippet)
        try:
            json.loads(sanitized)
            return sanitized
        except json.JSONDecodeError:
            print("  ⚠️  Could not coerce to valid JSON")
            return snippet
    
    def _fix_json_errors(self, text: str) -> str:
        """Attempt to fix common JSON errors"""
        # Find the first { and last }
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        
        if first_brace == -1 or last_brace == -1:
            return text
        
        json_text = text[first_brace:last_brace + 1]
        
        # Fix unterminated strings by finding quotes
        lines = json_text.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Count quotes
            quote_count = line.count('"')
            # If odd number of quotes and line doesn't end with comma or brace, add closing quote
            if quote_count % 2 == 1 and not line.rstrip().endswith((',', '{', '}')):
                line = line.rstrip() + '"'
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def clear_cache(self, pattern: str = None):
        """Clear LLM cache (optionally by pattern)"""
        if pattern:
            for cache_file in self.cache_dir.glob(f"*{pattern}*"):
                cache_file.unlink()
        else:
            for cache_file in self.cache_dir.glob("*.txt"):
                cache_file.unlink()


# Singleton instance
_client = None

def get_client() -> LLMClient:
    """Get or create LLM client singleton"""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
