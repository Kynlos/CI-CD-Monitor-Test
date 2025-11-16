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
                response = requests.post(
                    GROQ_API_URL,
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': model,
                        'messages': messages,
                        'temperature': temperature,
                        'max_tokens': max_tokens
                    },
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
    
    def _coerce_to_json(self, text: str) -> str:
        """Extract and validate JSON from LLM response"""
        # Strip code fences
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        
        if text.endswith('```'):
            text = text[:-3]
        
        text = text.strip()
        
        # Try to parse as JSON
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError as e:
            # Try to extract JSON block with better pattern
            match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
            if match:
                try:
                    json.loads(match.group(0))
                    return match.group(0)
                except:
                    pass
            
            # Try to fix common issues
            fixed_text = self._fix_json_errors(text)
            try:
                json.loads(fixed_text)
                return fixed_text
            except:
                print("  ⚠️  Could not coerce to valid JSON")
                return text
    
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
