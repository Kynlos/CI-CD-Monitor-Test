```markdown
---
title: Pages Manager
layout: default
---

# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR**  
> A Python script that automatically reads your source‑code documentation, decides whether to create, append or modify pages, and keeps a GitHub‑Pages site in sync with your codebase. It uses an LLM (currently `openai/gpt-oss-120b`) to make “agentic” decisions and can generate multiple documentation perspectives (API, Modules, Features) for a single source file.

**Last updated:** 2025-11-16

---

## 1. Overview

`pages-manager.py` is a CI‑driven tool that:

| Feature | Description |
|---------|-------------|
| **LLM‑powered decision making** | Uses a large language model to decide the best action (`create`, `append`, `modify`) for each documentation file. |
| **Multi‑perspective docs** | Generates separate pages for API reference, module architecture, and feature guides from a single source file. |
| **Automatic index generation** | Builds `index.md` files for each section (`api/`, `modules/`, `features/`) and a global home page. |
| **Mapping persistence** | Stores a JSON mapping (`.github/pages-mapping.json`) that tracks which source file maps to which page(s) and metadata. |
| **Cache‑friendly** | LLM calls are cached where appropriate to speed up repeated runs. |
| **Extensible** | All logic is encapsulated in the `PagesManager` class; you can import and use it in other scripts. |

The script is intended to be run as part of a GitHub Actions workflow whenever source files change. It reads the corresponding Markdown docs from the `docs/` directory, decides how to integrate them into the GitHub Pages site, writes the files under `docs-site/`, updates the mapping, and finally generates a summary.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | Class | Main orchestrator for scanning, decision making, and file manipulation. |
| `process_docs_to_pages(doc_files: List[str])` | Function | High‑level entry point that processes a list of Markdown files and updates the site. |
| `GROQ_API_KEY` | `str` | Environment variable that holds the Groq API key. |
| `MODEL` | `str` | The LLM model identifier (`openai/gpt-oss-120b`). |
| `PAGES_DIR` | `Path` | Root directory for generated GitHub Pages files (`docs-site`). |
| `MAPPING_FILE` | `str` | Path to the JSON mapping file (`.github/pages-mapping.json`). |

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
from pages_manager import PagesManager

# Instantiate
manager = PagesManager()

# Read a documentation file
doc_path = Path('docs/my_component.md')
doc_content = doc_path.read_text()

# Process it
manager.process_doc(doc_path, doc_content)
```

--- 

*End of page*  
```