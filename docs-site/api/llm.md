---
title: Llm
layout: default
---

# llm.py

*Auto-generated from `.github/scripts/llm.py`*

# llm.py – Centralized LLM Client

## Overview
`llm.py` provides a **single, reusable LLM client** that handles:

- **API calls** to the Groq OpenAI‑compatible endpoint
- **Retries** with exponential back‑off for rate‑limit or server errors
- **Local caching** of responses to avoid duplicate calls
- **JSON coercion** – automatically extracts, sanitises and validates JSON from LLM replies
- **Cache management** – clear cached responses by pattern or all

The module is designed to be imported from any script in the repository, ensuring consistent behaviour across all LLM‑powered utilities.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `LLMClient` | Class | Core client for interacting with the LLM. |
| `get_client` | Function | Returns a singleton `LLMClient` instance. |
| `GROQ_API_KEY` | Constant | Environment variable key for the Groq API token. |
| `GROQ_API_URL` | Constant | Default endpoint URL. |
| `CACHE_DIR` | Constant | Path to the local cache directory. |

---

## Usage Examples

### 1. Basic Text Completion

```python
from .llm import get_client

client = get_client()
response = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello, world!"}]
)

print(response)  # → "Hello, world!"
```

### 2. JSON‑Formatted Response

```python
response = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Return a JSON object with a greeting."}],
    response_format="json"
)

print(response)  # → {"greeting": "Hello!"}
```

### 3. Using the Cache

```python
# First call – will hit the API
client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    use_cache=True
)

# Second call – will use the cached response
client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    use_cache=True
)
```

### 4. Clearing the Cache

```python
# Remove all cached responses
client.clear_cache()

# Remove only those containing “math”
client.clear_cache(pattern="math")
```

---

## Class `LLMClient`

### Constructor
```python
LLMClient(api_key: str | None = None)
```
| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str | None` | Groq API key. If omitted, the client reads `GROQ_API_KEY` from the environment. |

### `call_chat`
```python
call_chat(
    model: str,
    messages: List[Dict],
    temperature: float = 0.3,
    max_tokens: int = 2000,
    response_format: str = 'text',
    timeout: int = 30,
    use_cache: bool = True
) -> Optional[str]
```
| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | LLM model name (e.g., `"gpt-4o-mini"`). |
| `messages` | `List[Dict]` | Chat history in OpenAI format. |
| `temperature` | `float` | Sampling temperature. |
| `max_tokens` | `int` | Max tokens to generate. |
| `response_format` | `'text' | 'json'` | If `'json'`, the client attempts to coerce the reply into valid JSON. |
| `timeout` | `int` | Request timeout in seconds. |
| `use_cache` | `bool` | Whether to read/write the local cache. |

**Return Value**  
`Optional[str]` – The LLM response (plain text or JSON string). Returns `None` on failure.

### `_strip_code_fences`
```python
_strip_code_fences(text: str) -> str
```
Removes Markdown code fences (` ``` `) from the supplied text.

### `_extract_balanced_json`
```python
_extract_balanced_json(text: str) -> Optional[str]
```
Scans the string for the first `{` or `[` and returns the smallest balanced JSON block found.

### `_sanitize_json_like`
```python
_sanitize_json_like(s: str) -> str
```
Normalises smart quotes, removes zero‑width spaces, and strips trailing commas.

### `_coerce_to_json`
```python
_coerce_to_json(text: str) -> str
```
Attempts to turn an arbitrary LLM reply into a valid JSON string by:
1. Stripping code fences
2. Parsing directly
3. Extracting a balanced JSON block
4. Sanitising and re‑parsing

If all attempts fail, it returns the original snippet and logs a warning.

### `_fix_json_errors`
```python
_fix_json_errors(text: str) -> str
```
A helper that attempts to patch common JSON mistakes (e.g., unterminated strings). Not used by the public API but available for debugging.

### `clear_cache`
```python
clear_cache(pattern: str | None = None) -> None
```
Deletes cached files. If `pattern` is supplied, only files whose names contain the pattern are removed.

---

## Function `get_client`
```python
get_client() -> LLMClient
```
Returns a **singleton** instance of `LLMClient`. Subsequent calls return the same object, ensuring consistent caching and configuration across the codebase.

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `GROQ_API_KEY` | `os.environ.get('GROQ_API_KEY')` | The environment variable holding the Groq API key. |
| `GROQ_API_URL` | `"https://api.groq.com/openai/v1/chat/completions"` | Default endpoint for chat completions. |
| `CACHE_DIR` | `Path('.llm-cache')` | Directory where cached responses are stored. |

---

## Notes & Best Practices

- **API Key**: Set `GROQ_API_KEY` in your environment or pass it explicitly to `LLMClient`.  
- **Caching**: The cache key is a SHA‑256 hash of the request parameters. Changing any parameter invalidates the cache.  
- **JSON Coercion**: The `response_format='json'` option is forgiving but not perfect. If the LLM returns malformed JSON, the client will still return the best‑effort snippet and log a warning.  
- **Error Handling**: All network errors are retried up to 3 times with exponential back‑off. After exhausting retries, `None` is returned.  
- **Thread‑Safety**: The singleton pattern is not thread‑safe. For multi‑threaded use, instantiate `LLMClient` directly.

---
