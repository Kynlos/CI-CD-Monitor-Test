---
title: Llm
layout: default
---

# llm.py

*Auto-generated from `.github/scripts/llm.py`*

# llm.py – Centralized LLM Client

> **TL;DR** – A lightweight, retry‑enabled wrapper around the Groq OpenAI‑compatible API that automatically caches responses, coerces text into valid JSON, and exposes a convenient singleton helper.

---

## 1. Overview

`llm.py` provides a **single, reusable LLM client** that:

| Feature | What it does |
|---------|--------------|
| **Retries** | Automatic exponential back‑off on 429 / 5xx responses and timeouts (3 attempts by default). |
| **Caching** | Stores successful responses in a local `.llm-cache` directory keyed by a hash of the request. Subsequent identical calls hit the cache instantly. |
| **JSON coercion** | When `response_format='json'`, the client attempts to parse the LLM’s raw output into a *valid* JSON string. It strips code fences, extracts balanced blocks, normalises smart quotes, removes trailing commas, and even escapes newlines inside strings. |
| **Singleton helper** | `get_client()` returns a global `LLMClient` instance, so you can call `get_client().call_chat(...)` from anywhere in your repo. |
| **Cache cleanup** | `LLMClient.clear_cache()` removes cached files, optionally filtered by a pattern. |

The module is intentionally lightweight (no external dependencies beyond `requests`) and is designed to be dropped into any Python script or GitHub Action that needs to talk to Groq.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `GROQ_API_KEY` | `str` | The Groq API key read from the environment (`GROQ_API_KEY`). |
| `GROQ_API_URL` | `str` | The endpoint (`https://api.groq.com/openai/v1/chat/completions`). |
| `CACHE_DIR` | `Path` | Default cache directory (`.llm-cache`). |
| `LLMClient` | class | The main client with caching, retries, and JSON handling. |
| `get_client` | function | Returns a singleton `LLMClient` instance. |

---

## 3. Usage Examples

> **Tip** – All examples assume you have `GROQ_API_KEY` set in your environment.

### 3.1. Basic chat call

```python
from .llm import get_client

client = get_client()

response = client.call_chat(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "What is the capital of France?"}
    ],
    temperature=0.2,
    max_tokens=150,
    response_format="text"   # or "json"
)

print(response)
```

### 3.2. Request JSON and auto‑coerce

```python
json_resp = client.call_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Return a JSON list of 3 colors."}],
    response_format="json"
)

# `json_resp` is a *string* containing valid JSON
import json
data = json.loads(json_resp)
print(data)  # e.g. ['red', 'green', 'blue']
```

### 3.3. Using the singleton helper

```python
# Anywhere in your code
from .llm import get_client

def ask(question: str) -> str:
    return get_client().call_chat(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        response_format="text"
    )
```

### 3.4. Clearing the cache

```python
client = get_client()
client.clear_cache()          # delete all cached responses
client.clear_cache("color")   # delete only files containing "color" in the filename
```

---

## 4. Parameters & Return Values

### 4.1. `LLMClient.__init__(api_key: str | None = None)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` or `None` | Groq API key. If omitted, the constructor falls back to the `GROQ_API_KEY` environment variable. |

**Return** – `None` (initialises the instance).

---

### 4.2. `LLMClient.call_chat(...)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | Model name (e.g., `"gpt-4o-mini"`). |
| `messages` | `List[Dict]` | Chat history in the OpenAI format. |
| `temperature` | `float` | Sampling temperature (default `0.3`). |
| `max_tokens` | `int` | Max tokens to generate (default `2000`). |
| `response_format` | `"text"` or `"json"` | If `"json"`, the client attempts to coerce the output into a valid JSON string. |
| `timeout` | `int` | Request timeout in seconds (default `30`). |
| `use_cache` | `bool` | Whether to read/write from the cache (default `True`). |

**Return** – `Optional[str]` – the LLM’s content as a string, or `None` on failure.

---

### 4.3. `LLMClient._strip_code_fences(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

**Return** – `str` – the input with any ``` or ```json fences removed.

---

### 4.4. `LLMClient._extract_balanced_json(text: str) -> Optional[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

**Return** – `Optional[str]` – the first balanced JSON object/array found, or `None`.

---

### 4.5. `LLMClient._sanitize_json_like(s: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `s` | `str` | Candidate JSON string. |

**Return** – `str` – a cleaned‑up version with smart quotes normalised, newlines escaped inside strings, and trailing commas removed.

---

### 4.6. `LLMClient._coerce_to_json(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

**Return** – `str` – a *valid* JSON string if coercion succeeded; otherwise the best‑attempt snippet (may still be invalid).

---

### 4.7. `LLMClient._fix_json_errors(text: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw LLM output. |

**Return** – `str` – a slightly more robust JSON snippet (used internally by `_coerce_to_json`).

---

### 4.8. `LLMClient.clear_cache(pattern: str | None = None)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | `str` or `None` | If provided, only cache files whose names contain this substring are removed. |

**Return** – `None`.

---

### 4.9. `get_client() -> LLMClient`

**Return** – The singleton `LLMClient` instance (creates it on first call).

---

## 5. Notes & Gotchas

- **Environment** – The module expects `GROQ_API_KEY` to be set. If you pass an explicit key to `LLMClient`, it overrides the env var.
- **Cache size** – Cached responses are plain text files. They grow with the number of unique prompts. Clean them with `clear_cache()` if disk space becomes an issue.
- **JSON coercion** – The helper is *heuristic*. If the LLM returns malformed JSON, the returned string may still be invalid. Always `json.loads()` and handle `JSONDecodeError` in your code.
- **Thread‑safety** – The singleton pattern is *not* thread‑safe. If you need concurrent
