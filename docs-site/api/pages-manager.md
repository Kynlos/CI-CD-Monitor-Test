```markdown
---
title: Pages Manager
layout: default
---

# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR**  
> A Python script that automatically reads your source‑code documentation, decides the best way to organize it into a GitHub Pages site, and writes the resulting Markdown files.  
> It uses an LLM (via the `llm` wrapper) to make “agentic” decisions about whether to **create**, **append**, or **modify** pages, and it keeps a persistent mapping of source files to generated pages.

**Last updated:** 2025-11-16

---

## 1. Overview

`pages-manager.py` is a **CI‑driven documentation generator**. It:

| Feature | Description |
|---------|-------------|
| **LLM‑powered decision making** | Uses a large language model (`openai/gpt-oss-120b`) to decide the best action (`create`, `append`, `modify`) for each documentation file. |
| **Multi‑perspective docs** | Generates separate pages for API reference, module architecture, and feature guides from a single source file. |
| **Automatic index generation** | Builds `index.md` files for each section (`api/`, `modules/`, `features/`) and a global home page. |
| **Mapping persistence** | Stores a JSON mapping (`.github/pages-mapping.json`) that tracks which source file maps to which page(s) and metadata. |
| **Cache‑friendly** | LLM calls are cached where appropriate to speed up repeated runs. |
| **Extensible** | All logic is encapsulated in the `PagesManager` class; you can import and use it in other scripts. |

When a set of Markdown files (typically one per source file) is supplied, the script:

1. **Scans** the existing `docs-site/` directory for current pages.  
2. **Analyzes** each source file’s documentation to decide which *perspectives* (API, Module, Feature) are relevant.  
3. **Calls the LLM** (via the `llm` wrapper) to decide whether to create a new page, append to an existing one, or modify an existing page.  
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
| `GROQ_API_KEY` | **str** | Environment variable that holds the Groq API key (used by the `llm` wrapper). |
| `MODEL` | **str** | LLM model identifier (`openai/gpt-oss-120b`). |
| `PAGES_DIR` | **Path** | Root directory for generated GitHub Pages files (`docs-site`). |
| `MAPPING_FILE` | **Path** | Path to the JSON mapping file (`.github/pages-mapping.json`). |

---

## 3. Usage Examples

### 3.1. Running the script from the command line

```bash
# Ensure the environment variable is set
export GROQ_API_KEY="sk-..."

# Run the script (it will read `changed_files.txt` and `docs/` automatically)
python .github/scripts/pages-manager.py
```

### 3.2. Using the `PagesManager` class programmatically

```python
from pathlib import Path
from pages_manager import PagesManager, process_docs_to_pages

# Instantiate the manager
manager = PagesManager()

# Example: process a list of documentation files
doc_files = [
    Path("docs/module_a.md"),
    Path("docs/module_b.md"),
]

# Run the high‑level helper
process_docs_to_pages(doc_files)

# Or work with the manager directly
for doc_path in doc_files:
    manager.process_single_doc(doc_path)   # hypothetical method illustrating per‑file handling
```

---

## 4. Implementation Notes (optional)

- **LLM Wrapper**: The script relies on the `llm` Python package, which abstracts away the underlying provider (Groq, OpenAI, etc.).  
- **Caching**: Results from LLM calls are cached in `.cache/llm/` to avoid redundant requests during the same CI run.  
- **Mapping File Structure**: `.github/pages-mapping.json` follows the schema  

```json
{
  "source_file": "src/module_a.ts",
  "generated_pages": [
    {
      "path": "docs-site/api/module_a.md",
      "perspective": "api",
      "last_updated": "2025-11-16T12:34:56Z"
    }
  ]
}
```

- **Extensibility**: To add a new perspective (e.g., “Tutorials”), extend `PagesManager.PERSPECTIVES` and provide a corresponding Jinja template in `templates/`.

--- 

*End of merged documentation.*```