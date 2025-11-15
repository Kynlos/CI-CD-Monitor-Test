---
title: Wiki Manager
layout: default
---

# wiki-manager.py

*Auto-generated from `.github/scripts/wiki-manager.py`*

# 📚 `wiki-manager.py` – Smart Wiki Manager

> **TL;DR** – A Python helper that automatically routes documentation files to the correct GitHub Wiki pages, using LLM‑powered categorization, intelligent merging, and a persistent mapping file.

---

## 1. Overview

`wiki-manager.py` is a self‑contained script that:

| Feature | What it does |
|---------|--------------|
| **Persistent mapping** | Keeps a JSON file (`.github/wiki-mapping.json`) that remembers which source file maps to which wiki page. |
| **Wiki introspection** | Pulls the current list of wiki pages from the GitHub API. |
| **LLM‑powered routing** | Calls the Groq API to decide the best wiki page for a file. |
| **Smart merging** | Uses the LLM to merge new documentation into existing pages, preserving structure and timestamps. |
| **Consistency checks** | Validates that the mapping file matches the actual wiki state. |
| **Summary generation** | Produces a Markdown summary (`wiki_summary.md`) that lists all pages, their files, and last‑updated timestamps. |
| **CLI entry point** | Can be run directly; it reads `changed_files.txt` to determine which docs to process. |

The script is designed for **GitHub Actions** or local CI pipelines that generate documentation (e.g., from TypeScript, JavaScript, or Python source files).

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `WikiManager` | Class | Core engine that handles mapping, LLM calls, and GitHub Wiki interactions. |
| `process_documentation_to_wiki(doc_files: List[str]) -> List[Dict]` | Function | High‑level helper that processes a list of Markdown docs and updates the wiki. |
| `GROQ_API_KEY`, `GITHUB_TOKEN`, `GITHUB_REPO`, `GROQ_API_URL`, `MODEL`, `MAPPING_FILE` | Constants | Environment‑driven configuration values. |

> **Note** – All other functions/methods are internal helpers and are not part of the public API.

---

## 3. Usage Examples

### 3.1 Running the Script Directly

```bash
# 1️⃣  Set required environment variables
export GROQ_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."
export GITHUB_REPOSITORY="owner/repo"

# 2️⃣  Create a list of changed source files (e.g., from a CI job)
echo "src/auth.ts" > changed_files.txt
echo "src/database.ts" >> changed_files.txt

# 3️⃣  Run the manager
python .github/scripts/wiki-manager.py
```

The script will:

1. Read `changed_files.txt`.
2. Find the corresponding Markdown docs in `docs/`.
3. Route each doc to the correct wiki page.
4. Update the mapping file and generate `wiki_summary.md`.

### 3.2 Using the API in Your Own Code

```python
from pathlib import Path
from typing import List
from .wiki_manager import WikiManager, process_documentation_to_wiki

# Example: manually process a single doc
doc_path = Path("docs/auth.md")
updates = process_documentation_to_wiki([str(doc_path)])
print(f"Updated {len(updates)} wiki pages")

# Example: instantiate the manager directly
manager = WikiManager()
page = manager.determine_wiki_page("src/auth.ts", "export function login() {}")
print(f"Doc should go to: {page}")

# Update a page manually
manager.update_wiki_page(page, "# Authentication\n\nDetails...")
manager.record_mapping("src/auth.ts", page)
manager.save_mapping()
```

---

## 4. Parameters & Return Values

### 4.1 `WikiManager`

| Method | Parameters | Return Value | Description |
|--------|------------|--------------|-------------|
| `__init__()` | – | `None` | Loads mapping and fetches existing wiki pages. |
| `load_mapping() -> Dict` | – | Mapping dictionary | Reads `.github/wiki-mapping.json` or creates a fresh structure. |
| `save_mapping() -> None` | – | `None` | Persists the mapping to disk. |
| `fetch_wiki_pages() -> List[str]` | – | List of page titles | Calls GitHub API to list wiki pages. |
| `determine_wiki_page(file_path: str, file_content: str) -> str` | `file_path`, `file_content` | Page title | Uses LLM or fallback to decide the best wiki page. |
| `_fallback_page_name(file_path: str) -> str` | `file_path` | Page title | Simple heuristic when LLM fails. |
| `update_wiki_page(page_name: str, content: str) -> bool` | `page_name`, `content` | `True`/`False` | Writes merged content to `wiki_updates/<page_name>.md`. |
| `_merge_wiki_content(existing: str, new: str, page_name: str) -> str` | `existing`, `new`, `page_name` | Markdown string | LLM‑based merge of new docs into existing page. |
| `_simple_merge(existing: str, new: str) -> str` | `existing`, `new` | Markdown string | Fallback merge (append + timestamp). |
| `record_mapping(file_path: str, page_name: str) -> None` | `file_path`, `page_name` | `None` | Updates internal mapping structures. |
| `verify_consistency() -> bool` | – | `True`/`False` | Checks mapping integrity; prints issues. |
| `generate_summary() -> str` | – | Markdown string | Summary of all wiki pages and their files. |

### 4.2 `process_documentation_to_wiki(doc_files: List[str]) -> List[Dict]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `doc_files` | `List[str]` | Paths to Markdown documentation files that need to be routed. |

| Return Value | Type | Description |
|--------------|------|-------------|
| `List[Dict]` | List of dictionaries | Each dict contains `file` (source file path) and `page` (wiki page title) for every successful update. |

---

## 5. Configuration & Environment

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `GROQ_API_KEY` | ✅ | – | API key for the Groq LLM endpoint. |
| `GITHUB_TOKEN` | ✅ | – | Personal access token with `repo` scope to read/write wiki. |
| `GITHUB_REPOSITORY` | ✅ | – | Format: `owner/repo`. |
| `GROQ_API_URL` | – | `https://api.groq.com/openai/v1/chat/completions` | Endpoint for LLM calls. |
| `MODEL` | – | `openai/gpt-oss-120b` | Model used for routing and merging. |
| `MAPPING_FILE` | – | `.github/wiki-mapping.json` | Path to persistent mapping. |

> **Tip** – Store these variables in a `.env` file and load them with `dotenv` in your CI workflow.

---

## 6. Common Patterns

### 6.1 Determining the Source File

The script assumes a convention: a doc file `docs/<name>.md` corresponds to a source file `<name>.ts` (or `.js`/`.py`). If the source file is missing, the script falls back to the doc filename.

### 6.2 LLM Prompt Structure

- **Routing Prompt** – Provides file content, existing pages, and previous mappings. The LLM returns *only* the page title.
- **Merge Prompt** – Gives the existing page and new documentation, instructs the LLM to add/update sections, and updates the timestamp.

### 6.3 Fallback Logic

If the LLM call fails or returns an invalid page name, `_fallback_page_name` uses simple heuristics (e.g., `auth.ts` → `Authentication-API`).

---

## 7. Extending the Manager

| Extension | How |
|-----------|-----|
| **Custom prompt** | Override `det
