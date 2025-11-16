# llm.py

*Auto-generated from `.github/scripts/llm.py`*

# llm.py – Centralized LLM Client

> **TL;DR**  
> A lightweight, retry‑enabled wrapper around the Groq/OpenAI chat API.  
> It automatically caches responses, coerces LLM output to valid JSON, and exposes a simple singleton API for use across your repository.

---

## 1. Overview

`llm.py` implements a **single, reusable LLM client** that:

| Feature | What it does |
|---------|--------------|
| **Retries** | Automatic exponential back‑off on rate‑limit (`429`) or server errors (`5xx`). |
| **Caching** | Stores successful responses in `.llm-cache/` keyed by a hash of the request. |
| **JSON coercion** | Attempts to parse, extract, and sanitize LLM output into a valid JSON string. |
| **Singleton** | `get_client()` returns a shared `LLMClient` instance, so you never need to instantiate it yourself. |
| **Convenience helpers** | `clear_cache()` removes cached files, optionally by pattern. |

> **Why Groq?**  
> The module is configured to hit `https://api.groq.com/openai/v1/chat/completions`, but you can swap the URL or key by setting `GROQ_API_KEY` / `GROQ_API_URL` environment variables.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `LLMClient` | Class | Main client with retry, cache, and JSON handling. |
| `get_client` | Function | Returns a singleton `LLMClient` instance. |
| `CACHE_DIR` | `Path` | Default cache directory (`.llm-cache`). |

---

## 3. Usage Examples

> **Prerequisites**  
> ```bash
> export GROQ_API_KEY="sk-…"
> ```

### 3.1 Basic Chat Call

```python
from .llm import get_client

client = get_client()

response = client.call_chat(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.2,
    max_tokens=100,
    response_format="text"  # or "json"
)

print(response)  # "Paris"
```

### 3.2 Requesting JSON Output

```python
response_json = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Return a JSON object with name and age."}],
    response_format="json"
)

# `response_json` is a *string* that contains valid JSON
import json
data = json.loads(response_json)
print(data)  # {'name': 'Alice', 'age': 30}
```

### 3.3 Using the Cache

```python
# First call – will hit the API
client.call_chat(...)

# Second call – will read from cache
client.call_chat(...)
```

### 3.4 Clearing the Cache

```python
# Delete all cached responses
client.clear_cache()

# Delete only those that contain "weather" in the filename
client.clear_cache(pattern="weather")
```

### 3.5 Accessing Internal Helpers (for debugging)

```python
raw = client._coerce_to_json('{"foo": "bar",')
print(raw)  # prints a sanitized JSON string or the original snippet
```

> **Tip** – All helper methods are prefixed with an underscore; they are meant for internal use but are exposed for advanced debugging.

---

## 4. Parameters & Return Values

### 4.1 `LLMClient.__init__(api_key: Optional[str] = None)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str | None` | Groq API key. If omitted, the module reads `GROQ_API_KEY` from the environment. |

> **Return** – `None` (initializes the instance).

---

### 4.2 `LLMClient.call_chat(...)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | Model name (e.g., `"gpt-4o-mini"`). |
| `messages` | `List[Dict]` | Chat history, each dict containing `"role"` and `"content"`. |
| `temperature` | `float` | Creativity level (default `0.3`). |
| `max_tokens` | `int` | Max tokens to generate (default `2000`). |
| `response_format` | `str` | `"text"` (default) or `"json"` – forces the API to return a JSON object. |
| `timeout` | `int` | HTTP timeout in seconds (default `30`). |
| `use_cache` | `bool` | If `True`, read/write cache (default `True`). |

> **Return** – `Optional[str]`  
> * `str` – The LLM response (plain text or JSON string).  
> * `None` – On failure after all retries.

---

### 4.3 `LLMClient._strip_code_fences(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

> **Return** – `str` – Input with any surrounding triple‑backtick fences removed.

---

### 4.4 `LLMClient._extract_balanced_json(text: str) -> Optional[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

> **Return** – `Optional[str]` – The first balanced `{…}` or `[…]` block, or `None` if none found.

---

### 4.5 `LLMClient._sanitize_json_like(s: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `s` | `str` | JSON‑like string that may contain smart quotes, zero‑width spaces, or trailing commas. |

> **Return** – `str` – Normalized string ready for `json.loads()`.

---

### 4.6 `LLMClient._coerce_to_json(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

> **Return** – `str` – A *valid* JSON string if coercion succeeded; otherwise the best‑attempt snippet.

---

### 4.7 `LLMClient._fix_json_errors(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

> **Return** – `str` – A repaired JSON string (used internally by `_coerce_to_json`).

---

### 4.8 `LLMClient.clear_cache(pattern: Optional[str] = None) -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | `str | None` | If provided, only delete cache files whose names contain this substring. |

> **Return** – `None`.  
> Side‑effect: removes files from `.llm-cache/`.

---

### 4.9 `get_client() -> LLMClient`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | | |

> **Return** – `LLMClient` – The singleton instance.  
> Subsequent calls return the same object.

---

## 5. Design Notes

| Feature | Implementation Detail |
|---------|-----------------------|
| **Cache key** | SHA‑256 of `model:messages:temperature:max_tokens` (first 16 hex chars). |
| **Retry policy** | 3 attempts, exponential back‑off (`1, 2, 4` seconds). |
| **JSON coercion** | 1️⃣ Try raw JSON 2️⃣ Extract balanced block 3️⃣ Sanitize (smart quotes, trailing commas, unterminated strings). |
| **Error handling** | Prints human‑readable messages to `stdout`; returns `None` on unrecoverable errors. |
| **Thread safety** | Not explicitly thread‑safe; use a single instance per process. |

---

## 6. Quick Reference

```python
from .llm import get_client

client = get_client()

# 1. Simple text response
text = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)

# 2. JSON response
json_str = client.call_chat(
    model="gpt-4