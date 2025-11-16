# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# 📄 `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR**  
> A Python script that automatically reads your source‑code documentation, decides whether to create, append or modify GitHub Pages files, and keeps the site structure up‑to‑date. It uses an LLM (Groq/OpenAI) to make “agentic” decisions and can generate multiple documentation perspectives (API, Modules, Features) for a single source file.

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
doc_content = doc_path.read_text(encoding='utf-8')

# Generate decisions for all perspectives
perspectives = manager.generate_multi_perspective_docs(
    source_file='my_component.ts',
    doc_content=doc_content
)

# Apply each decision
for page_path, action, reasoning in perspectives:
    manager.apply_documentation_change(
        page_path=page_path,
        action=action,
        doc_content=doc_content
    )
```

### 3.3. Using the high‑level helper

```python
from pages_manager import process_docs_to_pages

# Process a list of Markdown files
process_docs_to_pages([
    'docs/foo.md',
    'docs/bar.md',
])
```

---

## 4. Detailed API

Below is a concise reference for each public method and function, including parameters and return values.

### 4.1. `PagesManager`

| Method | Parameters | Return Value | Description |
|--------|------------|--------------|-------------|
| `__init__(self)` | – | – | Loads the mapping and scans existing pages. |
| `load_mapping(self) -> Dict` | – | Mapping dictionary | Reads `.github/pages-mapping.json` or creates a fresh structure. |
| `save_mapping(self) -> None` | – | – | Persists the mapping to disk. |
| `scan_existing_pages(self) -> Dict[str, str]` | – | `{relative_path: content}` | Recursively reads all `.md` files under `PAGES_DIR`. |
| `generate_multi_perspective_docs(self, source_file: str, doc_content: str) -> List[Tuple[str, str, str]]` | `source_file`: file name without extension (e.g., `foo.ts`) <br> `doc_content`: Markdown content of the source file | `[(page_path, action, reasoning), …]` | Uses the LLM to decide which documentation perspectives (API, Module, Feature) to generate, then calls `make_intelligent_decision` for each. |
| `make_intelligent_decision(self, source_file: str, doc_content: str, perspective: str = 'api') -> Tuple[str, str, str]` | `source_file`, `doc_content`, `perspective` (`'api' | 'module' | 'feature'`) | `(page_path, action, reasoning)` | LLM decides whether to create, append, or modify a page. |
| `_fallback_decision(self, source_file: str, perspective: str = 'api') -> Tuple[str, str, str]` | `source_file`, `perspective` | `(page_path, action, reasoning)` | Simple heuristic fallback if the LLM fails. |
| `apply_documentation_change(self, page_path: str, action: str, doc_content: str, section_title: str = None) -> bool` | `page_path`: relative path under `PAGES_DIR` <br> `action`: `'create' | 'append' | 'modify'` <br> `doc_content`: Markdown to write <br> `section_title`: optional title for appended/modified sections | `True` if the file was written/updated, `False` otherwise | Dispatches to `_create_page`, `_append_to_page`, or `_modify_page`. |
| `_create_page(self, path: Path, content: str) -> bool` | `path`: full file path <br> `content`: Markdown body | `True` on success | Writes a new file with front‑matter. |
| `_append_to_page(self, path: Path, content: str, section_title: str) -> bool` | `path`, `content`, `section_title` | `True` on success | Adds a new section to an existing file. |
| `_modify_page(self, path: Path, new_content: str, section_title: str) -> bool` | `path`, `new_content`, `section_title` | `True` on success | Calls `_intelligent_merge` to merge content. |
| `_intelligent_merge(self, existing: str, new_content: str, section_title: str, page_name: str) -> str` | `existing`: current file content <br> `new_content`: new Markdown <br> `section_title`: section to target <br> `page_name`: file name | `merged_content` | Uses the LLM to produce a merged Markdown document. |
| `generate_index_page(self) -> None` | – | – | Builds `index.md` files for `api/`, `modules/`, `features/`, and the root `index.md`. |

### 4.2. `process_docs_to_pages(doc_files: List[str]) -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| `doc_files` | `List[str]` | Paths to Markdown files under the `docs/` directory that need to be processed. |

| Return | Description |
|--------|-------------|
| `None` | The function writes files to `docs-site/`, updates the mapping, and creates a `pages_summary.md`. |

---

## 5. Parameter & Return Value Details

### 5.1. `PagesManager.generate_multi_perspective_docs`

| Parameter | Type | Notes |
|-----------|------|-------|
| `source_file` | `str` | e.g., `"