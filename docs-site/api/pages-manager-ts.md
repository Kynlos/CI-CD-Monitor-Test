---
title: Pages Manager Ts
layout: default
---

# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# `pages-manager.py`

> **Intelligent GitHub Pages Documentation Manager**  
> A Python script that automatically scans your codebase, decides where new documentation should live, and writes/updates Markdown pages in a GitHub‑Pages‑ready structure.  
> It uses an LLM (via the `llm` wrapper) to make agentic decisions about *what* to document, *where* to place it, and *how* to merge updates.

---

## Overview

| Feature | Description |
|---------|-------------|
| **LLM‑powered decision making** | Uses a large language model to decide whether to create, append, or modify a page. |
| **Multi‑perspective docs** | Generates API, module‑architecture, and feature‑guide docs from a single source file. |
| **Intelligent merge** | When updating an existing page, the LLM merges new content while preserving front‑matter and timestamps. |
| **Auto‑index generation** | Builds `index.md` pages for API, Modules, and Features sections. |
| **Persistent mapping** | Stores a JSON mapping of source files → pages, page metadata, and site structure. |
| **CLI entry point** | Reads `changed_files.txt`, maps to Markdown docs, and processes them. |

> **Prerequisites**  
> *Python 3.8+*  
> `GROQ_API_KEY` environment variable (or any key accepted by `llm.get_client`).  
> A `docs/` directory containing Markdown docs that mirror your TypeScript source files.  
> A `changed_files.txt` file listing the changed `.ts` files (one per line).

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | Class | Core manager that scans, decides, and writes pages. |
| `process_docs_to_pages(doc_files: List[str])` | Function | High‑level helper that drives the whole pipeline. |
| `GROQ_API_KEY`, `MODEL`, `PAGES_DIR`, `MAPPING_FILE` | Constants | Configuration values used throughout the script. |

> **Note**: The script is intended to be executed directly (`python pages-manager.py`).  
> The `if __name__ == "__main__":` block orchestrates the workflow.

---

## Class `PagesManager`

### Constructor

```python
PagesManager()
```

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Initializes mapping and scans existing pages. |

| Return | Type | Description |
|--------|------|-------------|
| *None* | | Side‑effects: `self.mapping`, `self.existing_pages`. |

---

### `load_mapping() -> Dict`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Reads `.github/pages-mapping.json` if present. |

| Return | Type | Description |
|--------|------|-------------|
| `Dict` | Mapping data structure (see `MAPPING_FILE` format). |

---

### `save_mapping() -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Writes `self.mapping` back to disk. |

| Return | Type | Description |
|--------|------|-------------|
| *None* | | Side‑effect: file written. |

---

### `scan_existing_pages() -> Dict[str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Walks `PAGES_DIR` for `.md` files. |

| Return | Type | Description |
|--------|------|-------------|
| `Dict[str, str]` | Mapping of relative path → file content. |

---

### `generate_multi_perspective_docs(source_file: str, doc_content: str) -> List[Tuple[str, str, str]]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Name of the TypeScript source file (e.g., `auth.ts`). |
| `doc_content` | `str` | Markdown content extracted from the source file. |

| Return | Type | Description |
|--------|------|-------------|
| `List[Tuple[str, str, str]]` | Each tuple: `(page_path, action, reasoning)` for API, module, and feature docs. |

> **Usage Example**

```python
manager = PagesManager()
perspectives = manager.generate_multi_perspective_docs(
    source_file="auth.ts",
    doc_content="# Authentication\n\n...documentation..."
)
# perspectives might be:
# [
#   ("api/authentication.md", "create", "API docs needed"),
#   ("modules/auth-system.md", "create", "Module architecture required"),
#   ("features/auth-guide.md", "create", "User guide for auth")
# ]
```

---

### `make_intelligent_decision(source_file: str, doc_content: str, perspective: str = 'api') -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Source file name. |
| `doc_content` | `str` | Markdown content. |
| `perspective` | `str` | One of `'api'`, `'module'`, `'feature'`. |

| Return | Type | Description |
|--------|------|-------------|
| `Tuple[str, str, str]` | `(page_path, action, reasoning)` |

> **Usage Example**

```python
page_path, action, reasoning = manager.make_intelligent_decision(
    source_file="payment.ts",
    doc_content="## Payment API\n\n...",
    perspective="api"
)
# page_path: "api/payments.md"
# action: "create"
# reasoning: "New payment API discovered"
```

---

### `_fallback_decision(source_file: str, perspective: str = 'api') -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Source file name. |
| `perspective` | `str` | One of `'api'`, `'module'`, `'feature'`. |

| Return | Type | Description |
|--------|------|-------------|
| `Tuple[str, str, str]` | `(page_path, action, reasoning)` | Used when the LLM fails. |

---

### `apply_documentation_change(page_path: str, action: str, doc_content: str, section_title: str = None) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `page_path` | `str` | Relative path inside `PAGES_DIR`. |
| `action` | `str` | `'create'`, `'append'`, or `'modify'`. |
| `doc_content` | `str` | Markdown to write. |
| `section_title` | `str` | Optional section header for append/modify. |

| Return | Type | Description |
|--------|------|-------------|
| `bool` | `True` if file written/updated, `False` otherwise. |

> **
