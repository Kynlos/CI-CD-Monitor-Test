# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# 📄 `pages-manager.py` – Intelligent GitHub Pages Documentation Manager

> **TL;DR** – A Python script that automatically scans your codebase, uses an LLM to decide where each piece of documentation should live, and then creates/updates GitHub‑Pages‑ready Markdown files. It also generates index pages for APIs, modules, and features, and keeps a persistent mapping of source files to documentation pages.

---

## 1. Overview

`pages-manager.py` is a CI‑driven tool that:

| Feature | What it does |
|---------|--------------|
| **LLM‑powered decision making** | Calls the Groq API to decide whether a new page should be created, appended to an existing page, or modified. |
| **Automatic page generation** | Creates Markdown files with proper front‑matter, or appends/updates sections as needed. |
| **Index generation** | Builds `api/index.md`, `modules/index.md`, `features/index.md`, and a site‑wide `index.md`. |
| **Persistent mapping** | Stores a JSON mapping (`.github/pages-mapping.json`) that tracks which source file maps to which page, when it was last updated, and what actions were taken. |
| **Fallback logic** | If the LLM fails, a deterministic fallback decides a sensible page path. |
| **CLI‑friendly** | Can be run from the command line; it reads a list of changed source files (`changed_files.txt`) and processes the corresponding Markdown docs in `docs/`. |

> **Why use it?**  
> When you add or modify code, you often forget to update the docs. This script keeps your documentation in sync automatically, ensuring consistency, reducing manual effort, and keeping the site structure clean.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | **Class** | Core engine that scans existing pages, makes LLM decisions, applies changes, and generates index pages. |
| `process_docs_to_pages(doc_files: List[str])` | **Function** | High‑level entry point that processes a list of Markdown documentation files and orchestrates the whole workflow. |
| `GROQ_API_KEY`, `GROQ_API_URL`, `MODEL`, `PAGES_DIR`, `MAPPING_FILE` | **Constants** | Configuration values used by the script. |

> *Note:* The script is intended to be run as a script (`python pages-manager.py`). The `if __name__ == "__main__":` block handles CLI usage.

---

## 3. Usage Examples

### 3.1 Running the Script Manually

```bash
# 1. Ensure your environment variable is set
export GROQ_API_KEY="sk-..."

# 2. Create a list of changed source files
echo "src/auth.ts" >> changed_files.txt
echo "src/database.ts" >> changed_files.txt

# 3. Run the manager
python .github/scripts/pages-manager.py
```

The script will:

1. Read `changed_files.txt`.
2. Map each source file to its Markdown counterpart in `docs/`.
3. Use the LLM to decide where to place the docs.
4. Create/append/modify pages under `docs-site/`.
5. Generate index pages.
6. Write a summary to `pages_summary.md`.

### 3.2 Using the API in Your Own Code

```python
from pages_manager import PagesManager, process_docs_to_pages

# Create a manager instance
manager = PagesManager()

# Example: manually decide where to put a new doc
page_path, action, reasoning = manager.make_intelligent_decision(
    source_file="src/payment.ts",
    doc_content="## Payment API\n\nDetails..."
)

# Apply the decision
manager.apply_documentation_change(page_path, action, "## Payment API\n\nDetails...")

# Generate the index pages
manager.generate_index_page()

# Or process a batch of docs
process_docs_to_pages(["docs/payment.md", "docs/database.md"])
```

---

## 4. Parameters & Return Values

### 4.1 `PagesManager`

| Method | Parameters | Return Value | Description |
|--------|------------|--------------|-------------|
| `__init__()` | None | `None` | Loads mapping and scans existing pages. |
| `load_mapping() -> Dict` | None | Mapping dictionary | Reads `.github/pages-mapping.json` or creates a fresh mapping. |
| `save_mapping() -> None` | None | None | Persists the mapping to disk. |
| `scan_existing_pages() -> Dict[str, str]` | None | `{relative_path: content}` | Scans `docs-site/` for Markdown files. |
| `make_intelligent_decision(source_file: str, doc_content: str) -> Tuple[str, str, str]` | `source_file`: e.g. `"auth.ts"`<br>`doc_content`: Markdown string | `(page_path, action, reasoning)`<br>`page_path`: e.g. `"api/authentication.md"`<br>`action`: `"create" | "append" | "modify"`<br>`reasoning`: Short explanation | Calls the LLM (or fallback) to decide where to place the doc. |
| `apply_documentation_change(page_path: str, action: str, doc_content: str, section_title: str = None) -> bool` | `page_path`: target file path<br>`action`: as above<br>`doc_content`: Markdown to apply<br>`section_title`: optional section header | `True` if file written/updated, `False` otherwise | Delegates to `_create_page`, `_append_to_page`, or `_modify_page`. |
| `_create_page(path: Path, content: str) -> bool` | `path`: full file path<br>`content`: Markdown body | `True`/`False` | Creates a new file with front‑matter. |
| `_append_to_page(path: Path, content: str, section_title: str) -> bool` | `path`: full file path<br>`content`: Markdown to append<br>`section_title`: optional header | `True`/`False` | Adds a new section to an existing page. |
| `_modify_page(path: Path, new_content: str, section_title: str) -> bool` | `path`: full file path<br>`new_content`: Markdown to merge<br>`section_title`: optional header | `True`/`False` | Uses LLM to merge intelligently. |
| `_intelligent_merge(existing: str, new_content: str, section_title: str, page_name: str) -> str` | `existing`: current page content<br>`new_content`: new Markdown<br>`section_title`: optional header<br>`page_name`: file name | `merged_content`: full Markdown | LLM merges new content into existing page. |
| `generate_index_page() -> None` | None | None | Builds `api/index.md`, `modules/index.md`, `features/index.md`, and the root `index.md`. |

### 4.2 `process_docs_to_pages(doc_files: List[str])`

| Parameter | Type | Description |
|-----------|------|-------------|
| `doc_files` | `List[str]` | Paths to Markdown documentation files to process. |

| Return Value | Description |
|--------------|-------------|
| `None` | The function writes changes to disk, updates the mapping, and prints a summary. |

---

## 5. Key Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `GROQ_API_KEY` | `os.environ.get('GROQ_API_KEY')` | API key for Groq LLM. |
| `GROQ_API_URL` | `"https://api.groq.com/openai/v1/chat/completions"` | Endpoint for LLM calls. |
| `MODEL` | `"openai/gpt-oss-120b"` | Model used for decision making and merging. |
| `PAGES_DIR` | `Path('docs-site')` | Root directory where generated Markdown pages live. |
| `MAPPING_FILE` | `'.github/pages-mapping.json'` | JSON file that persists source‑to‑page mapping. |

---

## 6. How