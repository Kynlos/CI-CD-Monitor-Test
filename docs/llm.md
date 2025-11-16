# llm.py

*Auto-generated from `.github/scripts/llm.py`*

# llm.py – LLM Client Library

> **Centralized LLM client with retries, caching, and JSON coercion**  
> This module provides a single, reusable client for calling the Groq (OpenAI‑compatible) API.  
> It handles:
> * Automatic retries with exponential back‑off
> * Local caching of responses (optional)
> * Robust JSON extraction / sanitisation
> * Code‑fence stripping
> * Simple singleton access

> **Why this module?**  
> Many of the repository’s scripts need to call an LLM. Instead of duplicating retry logic, cache handling, and JSON parsing in each script, this module centralises that logic in one place.

---

## 1. Overview

`llm.py` exposes a lightweight wrapper around the Groq API.  
The wrapper is designed for:

| Feature | Description |
|---------|-------------|
| **Retries** | 3 attempts with exponential back‑off (1 s, 2 s, 4 s). Retries on 429, 5xx, and timeouts. |
| **Caching** | Responses are cached to `./.llm-cache/<hash>.txt`. Cache key is derived from the request payload. |
| **JSON Coercion** | If `response_format='json'`, the client attempts to parse the response as JSON, stripping code fences, extracting balanced JSON, and sanitising common LLM output errors (smart quotes, trailing commas, multiline strings). |
| **Singleton** | `get_client()` returns a shared `LLMClient` instance, so you don’t need to instantiate it yourself. |

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `LLMClient` | Class | Main client for interacting with the LLM. |
| `get_client` | Function | Returns a singleton `LLMClient` instance. |
| `GROQ_API_KEY` | Constant | Environment variable key used to fetch the API key. |
| `GROQ_API_URL` | Constant | Default endpoint for Groq chat completions. |
| `CACHE_DIR` | Constant | Path to the local cache directory (`./.llm-cache`). |

---

## 3. Usage Examples

> **Prerequisites**  
> ```bash
> export GROQ_API_KEY="sk-xxxx"
> pip install requests
> ```

### 3.1 Basic Text Completion

```python
from .llm import get_client

client = get_client()

response = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello, world!"}],
    temperature=0.2,
    max_tokens=50,
)

print(response)  # e.g. "Hello, world!"
```

### 3.2 JSON‑Formatted Response

```python
from .llm import get_client

client = get_client()

json_resp = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Return a JSON object with a greeting."}],
    response_format="json",
)

print(json_resp)  # e.g. '{"greeting": "Hello, world!"}'
```

### 3.3 Using Cache

```python
from .llm import get_client

client = get_client()

# First call writes to cache
client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    use_cache=True,
)

# Subsequent call retrieves from cache
cached = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    use_cache=True,
)
print(cached)  # "4"
```

### 3.4 Clearing the Cache

```python
from .llm import get_client

client = get_client()
client.clear_cache()          # Delete all cache files
client.clear_cache("2+2")     # Delete cache files containing "2+2" in the filename
```

---

## 4. API Reference

### 4.1 `LLMClient`

#### `__init__(self, api_key: str = None)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` | Groq API key. If omitted, the client reads `GROQ_API_KEY` from the environment. |

#### `call_chat(self, *, model: str, messages: List[Dict], temperature: float = 0.3, max_tokens: int = 2000, response_format: str = 'text', timeout: int = 30, use_cache: bool = True) -> Optional[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | Model name (e.g., `"gpt-4o-mini"`). |
| `messages` | `List[Dict]` | Chat history. Each dict must have `"role"` and `"content"`. |
| `temperature` | `float` | Sampling temperature. |
| `max_tokens` | `int` | Maximum tokens to generate. |
| `response_format` | `'text'` or `'json'` | If `'json'`, the method will attempt to coerce the response into valid JSON. |
| `timeout` | `int` | Request timeout in seconds. |
| `use_cache` | `bool` | Whether to read/write from the local cache. |

**Return Value**  
`Optional[str]` – The raw or JSON‑coerced response text. Returns `None` on failure.

**Behaviour**  
1. **Cache lookup** – If `use_cache` is `True`, a SHA‑256 hash of the request is computed. If a cached file exists, its contents are returned immediately.  
2. **HTTP request** – Sends a POST to `GROQ_API_URL` with the supplied payload.  
3. **Retries** – Up to 3 attempts with exponential back‑off on 429, 5xx, or timeouts.  
4. **JSON coercion** – If `response_format='json'`, the response is processed by `_coerce_to_json`.  
5. **Cache write** – Successful responses are written to the cache file.

#### `_strip_code_fences(self, text: str) -> str`

Removes triple‑backtick fences (` ``` `) optionally followed by `json`.

#### `_extract_balanced_json(self, text: str) -> Optional[str]`

Finds the first balanced JSON object or array in `text`. Returns the snippet or `None`.

#### `_sanitize_json_like(self, s: str) -> str`

* Normalises smart quotes (`“ ” ’`) to ASCII (`" '`).  
* Removes zero‑width spaces.  
* Escapes newlines that appear inside quoted strings (common LLM bug).  
* Removes trailing commas before `}` or `]`.

#### `_coerce_to_json(self, text: str) -> str`

Attempts to produce a valid JSON string from LLM output:

1. Strip code fences.  
2. Try `json.loads` directly.  
3. Extract balanced JSON.  
4. Sanitize and try again.  
5. If all fail, returns the original snippet and prints a warning.

#### `_fix_json_errors(self, text: str) -> str`

Legacy helper (unused by `call_chat`) that attempts to close unterminated strings and remove stray commas.

#### `clear_cache(self, pattern: str = None)`

Deletes cached files.  
* If `pattern` is `None`, deletes all `.txt` files in `CACHE_DIR`.  
* Otherwise, deletes files whose names contain `pattern`.

---

### 4.2 `get_client() -> LLMClient`

Returns a singleton `LLMClient`. Subsequent calls return the same instance.

---

## 5. Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `GROQ_API_KEY` | `os.environ.get('GROQ_API_KEY')` | Environment variable name for the API key. |
| `GROQ_API_URL` | `'https://api.groq.com/openai/v1/chat/completions'` | Default endpoint. |
| `CACHE_DIR` | `Path('.llm-cache')` | Directory where cached responses are stored. |

---

## 6. Notes & Best Practices

| Topic | Recommendation |
|-------|----------------|
| **API Key** | Store in `GROQ_API_KEY` env var or pass explicitly to `LLMClient`. |
| **Cache Size** | Cached files are plain text; clean up with `clear_cache()` if disk space becomes an issue. |
| **JSON Coercion** | The `response_format='json'` flag is optional. If you trust the model’s output, you can skip coercion for speed. |
| **Error Handling** | `call_chat` prints warnings to stdout. In production, redirect logs or raise custom exceptions. |
| **Rate Limits** | The retry logic