# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR** – A Python script that automatically turns Markdown documentation files into a well‑structured GitHub Pages site.  
> It uses an LLM (Groq) to decide whether to create, append, or modify pages, merges content intelligently, and keeps a persistent mapping of source files to page paths.

---

## 1. Overview

`pages-manager.py` is a CI‑driven tool that:

| Feature | What it does |
|---------|--------------|
| **LLM‑powered decision making** | Sends the source file name and its Markdown content to Groq’s LLM to decide *where* the documentation should live. |
| **Smart page handling** | Creates new pages, appends to existing ones, or modifies pages while preserving front‑matter and timestamps. |
| **Index generation** | Builds a main `index.md` and per‑section index pages (e.g. `api/index.md`). |
| **Persistent mapping** | Stores a JSON mapping (`.github/pages-mapping.json`) that tracks which source file maps to which page and metadata. |
| **CI integration** | Reads a `changed_files.txt` list, looks up corresponding Markdown docs in `docs/`, and updates the GitHub Pages site in `docs-site/`. |
| **Security & audit** | Uses environment variables for the Groq API key and logs all actions to the console. |

> **Why use it?**  
> When you add or modify TypeScript/JavaScript source files, you usually also update the Markdown docs. This script automates the tedious part of moving those docs into the right place on your GitHub Pages site, ensuring consistency and reducing human error.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | Class | Core engine that scans existing pages, makes LLM decisions, applies changes, and generates indexes. |
| `process_docs_to_pages(doc_files: List[str])` | Function | High‑level entry point that processes a list of Markdown files, updates the site, and writes a summary. |
| `GROQ_API_KEY` | `str` | Environment variable holding the Groq API key. |
| `GROQ_API_URL` | `str` | Endpoint for the Groq chat completions API. |
| `MODEL` | `str` | LLM model name (`openai/gpt-oss-120b`). |
| `PAGES_DIR` | `Path` | Directory where the generated GitHub Pages site lives (`docs-site/`). |
| `MAPPING_FILE` | `str` | Path to the persistent JSON mapping (`.github/pages-mapping.json`). |

> **Note** – The script also contains a `__main__` block that can be executed directly.

---

## 3. Usage Examples

### 3.1 Running the script from the command line

```bash
# 1. Ensure the Groq API key is set
export GROQ_API_KEY="sk-..."

# 2. Create a list of changed source files (e.g. from a CI job)
echo "src/auth.ts" > changed_files.txt
echo "src/payment.ts" >> changed_files.txt

# 3. Run the manager
python .github/scripts/pages-manager.py
```

The script will:

1. Read `changed_files.txt`.
2. Find corresponding Markdown docs in `docs/`.
3. Use the LLM to decide where to place each doc.
4. Create/append/modify pages under `docs-site/`.
5. Generate `index.md` and section indexes.
6. Write a `pages_summary.md` and update `.github/pages-mapping.json`.

### 3.2 Using `PagesManager` programmatically

```python
from pathlib import Path
from pages_manager import PagesManager

# Instantiate the manager
manager = PagesManager()

# Example: create a new page
page_path = "api/new-feature.md"
content = "# New Feature\n\nDetails about the new feature."
manager.apply_documentation_change(page_path, "create", content)

# Example: append to an existing page
section_title = "New Functionality"
new_section = "## New Functionality\n\nDescription of the new function."
manager.apply_documentation_change("api/old-module.md", "append", new_section, section_title)

# Generate indexes after changes
manager.generate_index_page()
```

### 3.3 Using `process_docs_to_pages`

```python
from pages_manager import process_docs_to_pages

# Suppose you have a list of Markdown docs to process
docs = [
    "docs/auth.md",
    "docs/payment.md",
    "docs/notifications.md",
]

process_docs_to_pages(docs)
```

---

## 4. Parameters & Return Values

### 4.1 `PagesManager.__init__(self)`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | – | Initializes `self.mapping` and `self.existing_pages`. |

**Return** – `None` (constructor).

---

### 4.2 `PagesManager.load_mapping(self) -> Dict`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | – | Loads mapping from `MAPPING_FILE` if it exists. |

**Return** – A dictionary with keys: `version`, `last_updated`, `file_to_page`, `page_metadata`, `site_structure`.

---

### 4.3 `PagesManager.save_mapping(self) -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | – | Writes `self.mapping` to `MAPPING_FILE`. |

**Return** – `None`.

---

### 4.4 `PagesManager.scan_existing_pages(self) -> Dict[str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | – | Scans `PAGES_DIR` for all `.md` files and reads their content. |

**Return** – Dictionary mapping relative file paths to file contents.

---

### 4.5 `PagesManager.make_intelligent_decision(self, source_file: str, doc_content: str) -> Tuple[str, str, str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_file` | `str` | Name of the source file (e.g. `auth.ts`). |
| `doc_content` | `str` | Markdown content of the documentation. |

**Return** – `(page_path, action, reasoning)` where:
- `page_path` – Target Markdown file path (relative to `PAGES_DIR`).
- `action` – One of