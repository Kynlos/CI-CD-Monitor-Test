# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# 📄 `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR**  
> A Python utility that automatically reads, analyzes, and updates a GitHub Pages site from your source‑code documentation.  
> It uses an LLM (Groq) to decide whether to create, append, or modify pages, keeps a persistent mapping, and auto‑generates index pages for API, modules, and features.

---

## 1. Overview

`pages-manager.py` is a CI‑driven script that:

| Feature | What it does |
|---------|--------------|
| **LLM‑powered decision making** | Uses Groq’s GPT‑OSS model to decide where a new piece of documentation belongs. |
| **Full site awareness** | Scans the existing `docs-site/` directory, builds a summary, and feeds it to the LLM. |
| **Smart page handling** | Creates new pages, appends new sections, or modifies existing ones based on LLM output. |
| **Index generation** | Auto‑generates `index.md` files for API, modules, and features. |
| **Persistent mapping** | Stores a JSON mapping (`.github/pages-mapping.json`) that tracks which source file maps to which page and when it was last updated. |
| **CLI‑friendly** | Can be run directly from the command line; it reads `changed_files.txt` and `docs/` to determine what to process. |

> **Why use it?**  
> When you add or change a TypeScript/JavaScript file, you typically update its Markdown documentation. This script automatically pushes those changes into a well‑structured GitHub Pages site without manual editing.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | Class | Core class that handles page mapping, LLM decisions, and file operations. |
| `process_docs_to_pages(doc_files: List[str])` | Function | High‑level entry point that processes a list of Markdown docs and updates the site. |
| `GROQ_API_KEY` | Constant | Environment variable used for authentication with Groq. |
| `MODEL` | Constant | The LLM model name (`openai/gpt-oss-120b`). |
| `PAGES_DIR` | Constant | Path to the output documentation site (`docs-site/`). |
| `MAPPING_FILE` | Constant | Path to the JSON mapping file (`.github/pages-mapping.json`). |

> **Note:** The script also imports `get_client` from `llm.py` (not exported here) but is only used internally for LLM calls.

---

## 3. Usage Examples

### 3.1. Running the script from the command line

```bash
# Ensure GROQ_API_KEY is set
export GROQ_API_KEY="sk-..."

# Create a list of changed source files
echo "src/auth.ts" >> changed_files.txt
echo "src/database.ts" >> changed_files.txt

# Run the manager
python .github/scripts/pages-manager.py
```

The script will:

1. Read `changed_files.txt`.
2. Map each source file to its Markdown counterpart in `docs/`.
3. Process each doc file, updating `docs-site/`.
4. Generate index pages and a summary `pages_summary.md`.

### 3.2. Using the API programmatically

```python
from pathlib import Path
from pages_manager import PagesManager, process_docs_to_pages

# 1. Instantiate the manager
manager = PagesManager()

# 2. Decide where to put a new doc
page_path, action, reasoning = manager.make_intelligent_decision(
    source_file="src/payment.ts",
    doc_content="# Payment API\n\nDetails..."
)

# 3. Apply the change
manager.apply_documentation_change(
    page_path=page_path,
    action=action,
    doc_content="# Payment API\n\nDetails...",
    section_title="Payment Processing"
)

# 4. Generate index pages after all changes
manager.generate_index_page()

# 5. Save the mapping
manager.save_mapping()
```

### 3.3. Batch processing a list of Markdown files

```python
doc_files = [
    "docs/auth.md",
    "docs/database.md",
    "docs/payment.md"
]
process_docs_to_pages(doc_files)
```

---

## 4. Parameters & Return Values

### 4.1. `PagesManager.__init__()`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Initializes mapping and scans existing pages. |

| Return | Type | Description |
|--------|------|-------------|
| *None* | | Sets `self.mapping` and `self.existing_pages`. |

---

### 4.2. `PagesManager.load_mapping() -> Dict`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Reads `.github/pages-mapping.json` if it exists. |

| Return | Type | Description |
|--------|------|-------------|
| `Dict` | | Mapping object with keys: `version`, `last_updated`, `file_to_page`, `page_metadata`, `site_structure`. |

---

### 4.3. `PagesManager.save_mapping() -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Writes `self.mapping` to `MAPPING_FILE`. |

| Return | Type | Description |
|--------|------|-------------|
| `None` | | Side‑effect: file written. |

---

### 4.4. `PagesManager.scan_existing_pages() -> Dict[str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | | Walks `PAGES_DIR` for `.md` files. |

| Return | Type | Description |
|--------|------|-------------|
| `Dict[str, str]` | | Mapping of relative file path → file content. |

---

### 4.5. `PagesManager.make_intelligent_decision(source_file: str, doc_content: str) -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Name of the source file (e.g., `auth.ts`). |
| `doc_content` | `str` | Markdown content of the documentation. |

| Return | Type | Description |
|--------|------|-------------|
| `Tuple[str, str, str]` | | `(page_path, action, reasoning)` where `action` ∈ `{create, append, modify}`. |

---

### 4.6. `PagesManager._fallback_decision(source_file: str) -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Source file name. |

| Return | Type | Description |
|--------|------|-------------|
| `Tuple[str, str, str]` | | Fallback `(page_path, action, reasoning)` if LLM fails. |

---

### 4.7. `PagesManager.apply_documentation_change(page_path: str, action: str, doc_content: str, section_title: str = None) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `page_path` | `str` | Relative path inside `PAGES_DIR` (e.g., `api/authentication.md`). |
| `action` | `str` | One of `create`, `append`, `modify`. |
| `doc_content` | `str` | Markdown content to apply. |
| `section_title` | `str` | Optional title for new section (used in `append`/`modify`). |

| Return | Type | Description |
|--------|------|-------------|
| `bool` | | `True` if file was written/modified, `False` otherwise. |

---

### 4.8. `PagesManager._create_page(path: Path, content: str) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `