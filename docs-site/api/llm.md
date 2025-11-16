---
title: Llm
layout: default
---

# llm.py

*Auto-generated from `.github/scripts/llm.py`*

# llm.py – Centralized LLM Client

`llm.py` provides a lightweight, retry‑friendly wrapper around the Groq (OpenAI‑compatible) chat API.  
It adds:

* **Automatic caching** – repeat queries are served from disk, saving API calls and time.
* **JSON coercion** – LLM responses that look like JSON are extracted and validated.
* **Retry logic** – exponential back‑off for rate‑limit or transient errors.
* **Convenient singleton** – `get_client()` gives you a single shared instance.

The module is designed for use in CI/CD pipelines (e.g., GitHub Actions) but works just as well in local scripts.

---

## 1. Overview

| Feature | What it does |
|---------|--------------|
| **Caching** | Stores responses in `./.llm-cache/*.txt`. Subsequent identical calls return the cached text. |
| **Retries** | Up to 3 attempts with exponential back‑off (1 s, 2 s, 4 s). Retries on 429, 5xx, or timeouts. |
| **JSON Coercion** | Strips code fences, extracts the first JSON block, and attempts to fix common syntax errors. |
| **Singleton** | `get_client()` returns a single `LLMClient` instance, so you don’t need to instantiate it yourself. |
| **Environment** | Reads `GROQ_API_KEY` from the environment; can also be passed explicitly. |

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `LLMClient` | Class | Main client for calling the Groq chat API. |
| `get_client` | Function | Returns a singleton `LLMClient` instance. |
| `GROQ_API_KEY` | Constant | API key read from `os.environ`. |
| `GROQ_API_URL` | Constant | Default endpoint (`https://api.groq.com/openai/v1/chat/completions`). |
| `CACHE_DIR` | Constant | Path to the cache directory (`.llm-cache`). |

---

## 3. Usage Examples

### 3.1 Basic Text Response

```python
from .github.scripts.llm import get_client

client = get_client()

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

response = client.call_chat(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.2,
    max_tokens=50,
    response_format="text"
)

print(response)  # → "The capital of France is Paris."
```

### 3.2 JSON Response (Coercion)

```python
response = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give me a JSON list of 3 colors."}],
    response_format="json"   # triggers JSON coercion
)

print(response)  # → '{"colors": ["red", "green", "blue"]}'
```

### 3.3 Using the Cache

```python
# First call – will hit the API
client.call_chat(..., use_cache=True)

# Subsequent call – will read from .llm-cache
client.call_chat(..., use_cache=True)
```

### 3.4 Clearing the Cache

```python
client.clear_cache()          # deletes all cache files
client.clear_cache("red")     # deletes files matching *red*.txt
```

### 3.5 Custom API Key

```python
client = LLMClient(api_key="sk-…")  # bypasses environment variable
```

---

## 4. Parameters & Return Values

### 4.1 `LLMClient.__init__(api_key: Optional[str] = None)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str | None` | `None` | Groq API key. If omitted, the module reads `GROQ_API_KEY` from the environment. |

**Return**: `LLMClient` instance (constructor).

---

### 4.2 `LLMClient.call_chat(...)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | – | Model name (e.g., `"gpt-4o-mini"`). |
| `messages` | `List[Dict]` | – | Chat history. Each dict must contain `"role"` and `"content"`. |
| `temperature` | `float` | `0.3` | Sampling temperature. |
| `max_tokens` | `int` | `2000` | Max tokens to generate. |
| `response_format` | `str` | `"text"` | `"text"` (raw) or `"json"` (coerce to JSON). |
| `timeout` | `int` | `30` | Seconds before request times out. |
| `use_cache` | `bool` | `True` | Whether to read/write from the cache. |

**Return**: `Optional[str]` – the response text (or JSON string) or `None` on failure.

**Behavior**:

1. **Cache lookup** – if `use_cache` and a cached file exists, returns it immediately.
2. **API call** – sends a POST to `GROQ_API_URL` with the supplied parameters.
3. **Retry** – up to 3 attempts with exponential back‑off on 429, 5xx, or timeouts.
4. **JSON coercion** – if `response_format == "json"`, the raw text is passed to `_coerce_to_json`.

