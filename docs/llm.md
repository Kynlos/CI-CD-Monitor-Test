# llm.py

*Auto-generated from `.github/scripts/llm.py`*

# llm.py – Centralized LLM Client

The `llm.py` module provides a lightweight, retry‑enabled, cache‑aware wrapper around the Groq (OpenAI‑compatible) chat API.  
It is designed to be dropped into any script that needs to call an LLM, reducing boilerplate and ensuring consistent error handling, caching, and optional JSON coercion.

---

## 1. Overview

* **Retry logic** – Automatic retries on rate‑limit (429) or server errors (5xx) with exponential back‑off.
* **Caching** – Optional file‑based cache keyed by a hash of the request. Cached responses are reused to avoid duplicate calls.
* **JSON coercion** – When `response_format='json'`, the client attempts to extract a valid JSON object from the LLM’s raw text.
* **Singleton helper** – `get_client()` returns a single shared `LLMClient` instance, simplifying usage across modules.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `LLMClient` | Class | Main client for interacting with the LLM. |
| `get_client` | Function | Returns a singleton `LLMClient` instance. |
| `GROQ_API_KEY` | Constant | Environment variable name for the API key. |
| `GROQ_API_URL` | Constant | Default API endpoint. |
| `CACHE_DIR` | Constant | Default directory for cached responses. |

---

## 3. Usage Examples

### 3.1 Basic Text Response

```python
from llm import get_client

client = get_client()

response = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    temperature=0.2,
    max_tokens=50
)

print(response)  # "Paris."
```

### 3.2 JSON Response (Coercion)

```python
response = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Return a JSON object with the current date and time."}],
    response_format="json"
)

print(response)  # '{"date": "2025-11-15", "time": "14:30:00"}'
```

### 3.3 Using the Cache

```python
# First call – will hit the API
client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
    use_cache=True
)

# Second call – will read from cache
client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
    use_cache=True
)
```

### 3.4 Clearing the Cache

```python
# Clear all cached responses
client.clear_cache()

# Clear only cache files containing "gpt-4o-mini"
client.clear_cache(pattern="gpt-4o-mini")
```

### 3.5 Setting the API Key

```bash
export GROQ_API_KEY="sk-xxxxxx"
```

or pass it explicitly:

```python
client = LLMClient(api_key="sk-xxxxxx")
```

---

## 4. Parameters & Return Values

### 4.1 `LLMClient.__init__(api_key: Optional[str] = None)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str | None` | `None` | API key for authentication. If omitted, the module reads `GROQ_API_KEY` from the environment. |

**Return** – `None` (initializes the instance).

---

### 4.2 `LLMClient.call_chat(...)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | – | Model name (e.g., `"gpt-4o-mini"`). |
| `messages` | `List[Dict]` | – | List of message objects (`{"role": "...", "content": "..."}`). |
| `temperature` | `float` | `0.3` | Controls randomness. |
| `max_tokens` | `int` | `2000` | Max tokens to generate. |
| `response_format` | `str` | `"text"` | `"text"` (raw) or `"json"` (attempt to parse). |
| `timeout` | `int` | `30` | Request timeout in seconds. |
| `use_cache` | `bool` | `True` | Whether to read/write from the cache. |

**Return** – `Optional[str]`  
* The LLM’s response text (or JSON string if `response_format='json'`).  
* `None` if the request fails after all retries or if the API key is missing.

---

### 4.3 `LLMClient._coerce_to_json(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

**Return** – `str`  
* A cleaned JSON string if parsing succeeds.  
* The original text with a warning if JSON extraction fails.

---

### 4.4 `LLMClient.clear_cache(pattern: Optional[str] = None) -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | `str | None`