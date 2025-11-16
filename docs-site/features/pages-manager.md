---
title: Pages Manager
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
> * Python 3.8+  
> * `GROQ_API_KEY` environment variable (or any key accepted by `llm.get_client`).  
> * A `docs/` directory containing Markdown docs that mirror your TypeScript source files.  
> * A `changed_files.txt` file listing the changed `.ts` files (one per line).

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | Class | Core manager that scans, decides, and writes pages. |
| `process_docs_to_pages(doc_files: List[str])` | Function | High‑level helper that drives the whole pipeline. |
| `GROQ_API_KEY`, `MODEL`, `PAGES_DIR`, `MAPPING_FILE` | Constants | Configuration values used throughout the script. |

> **Note**: The script is intended to be executed directly (`python pages-manager.py`).  

---

*Last updated: 2025-11-16*