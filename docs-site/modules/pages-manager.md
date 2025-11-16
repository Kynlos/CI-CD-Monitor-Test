```markdown
---
title: Pages Manager
layout: default
last_updated: 2025-11-16
---

# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# `pages-manager.py`

> **Intelligent GitHub Pages Documentation Manager**  
> A Python script that automatically reads your source‑code documentation, decides how to best organize it into a GitHub Pages site, and writes the resulting Markdown files.  
> It uses an LLM (via the `llm` wrapper) to make agentic decisions about whether to create, append, or modify pages, and it keeps a persistent mapping of source files to generated pages.

---

## 1. Overview

The module is a **CI‑driven documentation generator**.  
When a set of Markdown files (typically one per TypeScript source file) is passed to the script, it:

1. **Scans** the existing `docs-site/` directory for current pages.  
2. **Analyzes** each source file’s documentation to decide which *perspectives* (API, Module, Feature) are relevant.  
3. **Uses an LLM** to decide whether to create a new page, append to an existing one, or modify an existing page.  
4. **Writes** the new/updated Markdown files, preserving front‑matter and timestamps.  
5. **Generates** index pages (`api/index.md`, `modules/index.md`, `features/index.md`, and the root `index.md`).  
6. **Persists** a mapping (`.github/pages-mapping.json`) that tracks which source file produced which page(s) and when.

The script is intended to be run in a CI job whenever source files change.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | **class** | Core class that handles scanning, decision‑making, and file manipulation. |
| `process_docs_to_pages(doc_files: List[str])` | **function** | High‑level entry point that processes a list of Markdown files and updates the GitHub Pages site. |
| `PAGES_DIR` | **Path** | Directory where the generated site lives (`docs-site/`). |
| `MAPPING_FILE` | **Path** | Path to the JSON file that stores the mapping (`.github/pages-mapping.json`). |
| `MODEL` | **str** | LLM model identifier (e.g., `gpt-4o`). |
```