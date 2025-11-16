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

## Overview

The module is a **CI‑driven documentation generator** that:

1. **Scans** the existing `docs-site/` directory for current pages.  
2. **Analyzes** each source file’s documentation to decide which *perspectives* (API, Module, Feature) are relevant.  
3. **Uses an LLM** to decide whether to create a new page, append to an existing one, or modify an existing page.  
4. **Writes** the new/updated Markdown files, preserving front‑matter and timestamps.  
5. **Generates** index pages (`api/index.md`, `modules/index.md`, `features/index.md`, and the root `index.md`).  
6. **Persists** a mapping (`.github/pages-mapping.json`) that tracks which source file produced which page(s) and when.

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
| `PagesManager` | **class** | Core manager that scans, decides, and writes pages. |
| `process_docs_to_pages(doc_files: List[str])` | **function** | High‑level helper that drives the whole pipeline. |
| `GROQ_API_KEY` | **constant** | API key for the LLM service. |
| `MODEL` | **constant** | LLM model identifier (e.g., `gpt-4o`). |
| `PAGES_DIR` | **constant** | Directory where the generated site lives (`docs-site/`). |
| `MAPPING_FILE` | **constant** | Path to the JSON file that stores the mapping (`.github/pages-mapping.json`). |

> **Note**: The script is intended to be executed directly (`python pages-manager.py`).  

---

## How It Works (Detailed Steps)

*(Retained from the original documentation for deeper insight)*  

- **Scanning** – Detects existing pages and their front‑matter.  
- **Analysis** – Parses source‑file documentation to extract API signatures, module relationships, and feature narratives.  
- **Decision Engine** – Calls the LLM with a prompt containing the existing page content and the new documentation fragment; the model returns an action (`create`, `append`, `modify`).  
- **Merging** – For `append`/`modify`, the LLM produces a merged Markdown block that respects existing headings and timestamps.  
- **Writing** – Files are written atomically; timestamps are updated only when content changes.  
- **Index Regeneration** – After all pages are processed, index files are regenerated to reflect the new structure.  
- **Mapping Update** – The JSON mapping is updated with the latest source‑to‑page relationships.

---

## CLI Usage

```bash
python pages-manager.py
```

The script reads `changed_files.txt`, resolves each changed TypeScript file to its corresponding Markdown documentation, and invokes `process_docs_to_pages` on the resulting list.

```text
# Example of changed_files.txt
src/components/button.ts
src/utils/helpers.ts
```

---

## Persistent Mapping Format

```json
{
  "src/components/button.ts": {
    "pages": ["api/button.md", "features/button.md"],
    "last_processed": "2025-11-16T12:34:56Z"
  }
}
```

The mapping enables incremental builds and avoids unnecessary re‑processing.