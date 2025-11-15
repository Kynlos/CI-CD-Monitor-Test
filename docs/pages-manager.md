# pages-manager.py

*Auto-generated from `.github/scripts/pages-manager.py`*

# `pages-manager.py` – API Documentation

> **Intelligent GitHub Pages Documentation Manager**  
> Automates the creation, updating, and organization of Markdown documentation for a GitHub‑Pages site using an LLM (Groq) to decide where each piece of documentation belongs.

---

## Overview

`pages-manager.py` is a self‑contained Python module that:

1. **Scans** the existing documentation site (`docs-site/`) and builds an in‑memory map of pages.
2. **Decides**—via a Groq LLM—whether a new Markdown file should be created, appended to an existing page, or modified.
3. **Applies** the chosen action, handling front‑matter, section insertion, and intelligent merging.
4. **Generates** an updated `index.md` with navigation links.
5. **Persists** a mapping file (`.github/pages-mapping.json`) that tracks which source file maps to which documentation page.
6. **Produces** a summary (`pages_summary.md`) of all changes made during a run.

The module is designed to be run as a CI/CD step or locally after a set of source files have changed. It expects:

| File | Purpose |
|------|---------|
| `changed_files.txt` | List of changed source files (one per line). |
| `docs/` | Directory containing Markdown docs that correspond to the source files. |
| `docs-site/` | Target directory for the generated GitHub‑Pages site. |
| `.github/pages-mapping.json` | Persistent mapping between source files and generated pages. |

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PagesManager` | **class** | Core class that encapsulates all page‑management logic. |
| `process_docs_to_pages(doc_files: List[str])` | **function** | High‑level helper that processes a list of Markdown files and updates the site. |

> **Note**: The module also defines several constants (`GROQ_API_KEY`, `GROQ_API_URL`, `MODEL`, `PAGES_DIR`, `MAPPING_FILE`) that are used internally.

---

## `PagesManager` Class

| Method | Parameters | Return Value | Description |
|--------|------------|--------------|-------------|
| `__init__(self)` | – | – | Loads the mapping file and scans existing pages. |
| `load_mapping(self) -> Dict` | – | `dict` | Reads `.github/pages-mapping.json` or returns a fresh mapping structure. |
| `save_mapping(self) -> None` | – | – | Writes the current mapping to disk and updates the `last_updated` timestamp. |
| `scan_existing_pages(self) -> Dict[str, str]` | – | `dict` | Walks `docs-site/` and returns `{relative_path: content}` for every Markdown file. |
| `make_intelligent_decision(self, source_file: str, doc_content: str) -> Tuple[str, str, str]` | `source_file` – name of the source file (e.g., `auth.ts`)<br>`doc_content` – Markdown content to be added | `(page_path, action, reasoning)`<br>`page_path` – target Markdown file (relative to `docs-site/`).<br>`action` – `"create" | "append" | "modify"`. | Calls the Groq LLM to decide where the content should go. Falls back to heuristics if the LLM fails. |
| `_fallback_decision(self, source_file: str) -> Tuple[str, str, str]` | `source_file` | Same as above | Heuristic decision when the LLM is unreachable. |
| `apply_documentation_change(self, page_path: str, action: str, doc_content: str, section_title: str = None) -> bool` | `page_path` – target file<br>`action` – `"create" | "append" | "modify"`<br>`doc_content` – Markdown to apply<br>`section_title` – optional section header for append/modify | `bool` – `True` if the file was written/updated successfully. | Dispatches to the appropriate helper (`_create_page`, `_append_to_page`, `_modify_page`). |
| `_create_page(self, path: Path, content: str) -> bool` | `path` – full file path<br>`content` – Markdown body | `bool` | Creates a new file with front‑matter. |
| `_append_to_page(self, path: Path, content: str, section_title: str) -> bool` | `path` – full file path<br>`content` – Markdown to append<br>`section_title` – header for the new section | `bool` | Adds a new section to an existing page. |
| `_modify_page(self, path: Path, new_content: str, section_title: str) -> bool` | `path` – full file path<br>`new_content` – Markdown to merge<br>`section_title` – header for the section to modify | `bool` | Uses the LLM to intelligently merge or replace content. |
| `_intelligent_merge(self, existing: str, new_content: str, section_title: str, page_name: str) -> str` | `existing` – current page content<br>`new_content` – new Markdown<br>`section_title` – target section<br>`page_name` – file name (for context) | `str` – merged Markdown | Calls the LLM to produce a merged page. |
| `generate_index_page(self) -> None` | – | – | Builds or updates `docs-site/index.md` with navigation links to all pages. |

---

## `process_docs_to_pages(doc_files: List[str])`

| Parameter | Type | Description |
|-----------|------|-------------|
| `doc_files` | `List[str]` | Paths to Markdown files that should be processed. |

| Return Value | Description |
|--------------|-------------|
| `None` | The function writes files to disk, updates the mapping, and creates a summary. |

**Behaviour**  
1. Instantiates `PagesManager`.  
2. For each Markdown file