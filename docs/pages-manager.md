# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# 📄 `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR** – A Python script that automatically reads your source‑code documentation, decides where it belongs in a GitHub Pages site, and creates/updates Markdown pages accordingly. It uses an LLM (via `llm.get_client()`) to make intelligent decisions and to merge content.

---

## 1. Overview

`pages-manager.py` is a CI‑driven helper that keeps a GitHub Pages documentation site in sync with your codebase.  
Key responsibilities:

| Responsibility | What it does |
|----------------|--------------|
| **LLM‑powered decision making** | Determines whether a new page should be created, an existing page appended to, or an existing page modified. |
| **Page scanning** | Reads all existing Markdown files in `docs-site/` to build a context for the LLM. |
| **Page creation / modification** | Generates front‑matter, writes new pages, appends sections, or merges updates. |
| **Index generation** | Builds `index.md` and sub‑index pages (`api/index.md`, `modules/index.md`, `features/index.md`) automatically. |
| **Mapping persistence** | Stores a JSON mapping (`.github/pages-mapping.json`) that tracks which source file maps to which page, when it was last updated, etc. |
| **CLI entry point** | Reads a list of changed source files (`changed_files.txt`), finds corresponding Markdown docs in `docs/`, and runs the whole pipeline. |

> **Why use it?**  
> *No manual page creation.*  
> *Consistent, AI‑driven structure.*  
> *Automatic index updates.*  
> *Audit trail via the mapping file.*

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | Class | Core engine that handles mapping, LLM decisions, and file operations. |
| `process_docs_to_pages(doc_files: List[str])` | Function | High‑level helper that processes a list of Markdown docs and updates the site. |
| `if __name__ == "__main__":` | Script entry point | Reads `changed_files.txt`, maps to docs, and calls `process_docs_to_pages`. |

> **Note** – The script also imports `get_client` from `llm`, but that is a dependency, not an export of this file.

---

## 3. Usage Examples

### 3.1 Using the `PagesManager` directly

```python
from pathlib import Path
from pages_manager import PagesManager

# Instantiate
manager = PagesManager()

# Example: decide where a new doc should go
source_file = "src/authentication.ts"
doc_content = "# Authentication\n\nDetails about auth..."

page_path, action, reasoning = manager.make_intelligent_decision(source_file, doc_content)
print(page_path, action, reasoning)

# Apply the decision
manager.apply_documentation_change(page_path, action, doc_content)

# Persist mapping
manager.save_mapping()
```

### 3.2 Running the full pipeline from the command line

```bash
# 1. Ensure changed files list exists
echo "src/authentication.ts" > changed_files.txt

# 2. Run the script
python3 .github/scripts/pages-manager.py
```

The script will:

1. Read `changed_files.txt`.
2. Find corresponding Markdown docs in `docs/`.
3. Use the LLM to decide placement.
4. Create/append/modify pages in `docs-site/`.
5. Generate index pages.
6. Write a summary to `pages_summary.md`.

---

## 4. Parameters & Return Values

### 4.1 `PagesManager.__init__()`

| Parameter | Type | Description |
|-----------|------|-------------|
| – | – | Initializes mapping and scans existing pages. |

| Return | Type | Description |
|--------|------|-------------|
| – | – | None (initializes instance attributes). |

---

### 4.2 `PagesManager.load_mapping() -> Dict`

| Parameter | Type | Description |
|-----------|------|-------------|
| – | – | Reads `.github/pages-mapping.json` if present. |

| Return | Type | Description |
|--------|------|-------------|
| `Dict` | Mapping structure with keys: `version`, `last_updated`, `file_to_page`, `page_metadata`, `site_structure`. |

---

### 4.3 `PagesManager.save_mapping() -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| – | – | Writes the current mapping to `.github/pages-mapping.json`. |

| Return | Type | Description |
|--------|------|-------------|
| – | – | None. |

---

### 4.4 `PagesManager.scan_existing_pages() -> Dict[str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| – | – | Scans `docs-site/` for `.md` files. |

| Return | Type | Description |
|--------|------|-------------|
| `Dict[str, str]` | Mapping of relative file path → file content. |

---

### 4.5 `PagesManager.make_intelligent_decision(source_file: str, doc_content: str) -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Name of the source file (e.g., `authentication.ts`). |
| `doc_content` | `str` | Markdown content of the documentation. |

| Return | Type | Description |
|--------|------|-------------|
| `Tuple[str, str, str]` | `(page_path, action, reasoning)` |
| `page_path` | `str` | Target Markdown file relative to `docs-site/`. |
| `action` | `str` | One of `"create"`, `"append"`, `"modify"`. |
| `reasoning` | `str` | Short explanation from the LLM. |

---

### 4.6 `PagesManager._fallback_decision(source_file: str) -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Source file name. |

| Return | Type | Description |
|--------|------|-------------|
| `Tuple[str, str, str]` | Fallback `(page_path, action, reasoning)` when the LLM fails. |

---

### 4.7 `PagesManager.apply_documentation_change(page_path: str, action: str, doc_content: str, section_title: str = None) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `page_path` | `str` | Target file path relative to `docs-site/`. |
| `action` | `str` | `"create"`, `"append"`, or `"modify"`. |
| `doc_content` | `str` | Markdown content to apply. |
| `section_title` | `str` | Optional section title for append/modify. |

| Return | Type | Description |
|--------|------|-------------|
| `bool` | `True` if file operation succeeded, otherwise `False`. |

---

### 4.8 `PagesManager._create_page(path: Path, content: str) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Full file path. |
| `content` | `str` | Markdown body. |

| Return | Type | Description |
|--------|------|-------------|
| `bool` | `True` on success. |

---

### 4.9 `PagesManager._append_to_page(path: Path, content: str, section_title: str) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Full file path. |
| `content` | `str` | Markdown to append. |
| `section