# wiki-manager.py

*Auto-generated from `.github/scripts/wiki-manager.py`*

# 📚 `wiki-manager.py` – Smart Wiki Manager

> A lightweight, LLM‑powered helper that automatically routes documentation files to the appropriate GitHub Wiki pages, keeps a persistent mapping, and generates a concise summary of the wiki organization.

---

## 1️⃣ Overview

| Feature | What it does |
|---------|--------------|
| **Persistent mapping** | Stores a JSON file (`.github/wiki-mapping.json`) that remembers which source file belongs to which wiki page. |
| **Intelligent routing** | Uses a Groq LLM to decide the best wiki page for a given source file, based on existing pages and previous mappings. |
| **Wiki updates** | Generates Markdown files in `wiki_updates/` that a CI workflow can commit to the GitHub Wiki. |
| **Consistency checks** | Verifies that the mapping and metadata are in sync. |
| **Summary report** | Creates `wiki_summary.md` with a high‑level view of the wiki structure. |

> **Why use it?**  
> When you add or change a source file, you usually also update its documentation. This script automates the tedious part of deciding *where* that documentation should live in the Wiki, so you can focus on writing great docs.

---

## 2️⃣ Exports

| Export | Type | Description |
|--------|------|-------------|
| `WikiManager` | Class | Core engine that handles mapping, LLM calls, page updates, and consistency checks. |
| `process_documentation_to_wiki(doc_files: List[str]) -> List[Dict]` | Function | Entry‑point that processes a list of Markdown docs, updates the wiki, and returns a list of updates. |
| `__main__` block | Script | Reads `changed_files.txt`, finds corresponding docs, and runs `process_documentation_to_wiki`. |

> The module does **not** expose any other public API. All internal helpers are prefixed with an underscore.

---

## 3️⃣ Usage Examples

### 3.1 Running the script manually

```bash
# 1️⃣ Set required environment variables
export GROQ_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."
export GITHUB_REPOSITORY="owner/repo"

# 2️⃣ Create a list of changed source files
echo "src/auth.ts" > changed_files.txt
echo "src/database.ts" >> changed_files.txt

# 3️⃣ Run the script
python .github/scripts/wiki-manager.py
```

> The script will:
> 1. Read `changed_files.txt`.
> 2. Find the corresponding Markdown docs in `docs/`.
> 3. Use the LLM to decide the wiki page for each doc.
> 4. Write updated Markdown files to `wiki_updates/`.
> 5. Persist the mapping to `.github/wiki-mapping.json`.
> 6. Generate `wiki_summary.md`.

### 3.2 Using the API from another Python module

```python
from .github_scripts.wiki_manager import process_documentation_to_wiki

# Suppose you already have a list of Markdown docs
docs = ["docs/auth.md", "docs/database.md"]

updates = process_documentation_to_wiki(docs)

print(f"Updated {len(updates)} wiki pages.")
```

> The function returns a list of dictionaries:

```json
[
  {"file": "src/auth.ts", "page": "Authentication-API"},
  {"file": "src/database.ts", "page": "Database-Layer"}
]
```

---

## 4️⃣ Detailed API Reference

### 4.1 `WikiManager`

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__()` | – | – | Loads the persistent mapping and fetches existing wiki pages. |
| `load_mapping() -> Dict` | – | Mapping dictionary | Reads `.github/wiki-mapping.json` or creates a fresh structure. |
| `save_mapping() -> None` | – | – | Writes the current mapping to disk and updates `last_updated`. |
| `fetch_wiki_pages() -> List[str]` | – | List of page titles | Calls the GitHub Wiki API; returns an empty list if credentials are missing or the wiki is uninitialized. |
| `determine_wiki_page(file_path: str, file_content: str) -> str` | `file_path`: path to the source file.<br>`file_content`: raw source code | Wiki page name | 1. Returns existing mapping if present.<br>2. Otherwise queries the Groq LLM with a prompt that includes existing pages and previous mappings.<br>3. Falls back to deterministic heuristics if the LLM fails. |
| `_fallback_page_name(file_path: str) -> str` | – | Wiki page name | Heuristic mapping based on directory names and file patterns. |
| `update_wiki_page(page_name: str, content: str) -> bool` | `page_name`: target wiki page.<br>`content`: Markdown content to write | `True` if the file was written successfully, `False` otherwise | Writes a Markdown file to `wiki_updates/<page_name>.md`. If the file already exists, it merges the new content. |
| `_merge_wiki_content(existing: str, new: str, page_name: str) -> str` | – | Merged Markdown string | Adds a header, updates the timestamp, and appends new content. |
| `record_mapping(file_path: str, page_name: str) -> None` | – | – | Updates the in‑memory mapping and page metadata. |
| `verify_consistency() -> bool` | – | `True` if mapping is consistent, `False` otherwise | Checks for duplicate mappings, missing metadata, and mismatched file lists. |
| `generate_summary() -> str` | – | Markdown string | Returns a human‑readable summary of all wiki pages, including file counts and recent updates. |

#### Example

```python
manager = WikiManager()
page = manager.determine_wiki_page("src/auth.ts", "export function login() {}")
manager.update_wiki_page(page, "# Auth API\n\nDetails...")
manager.record_mapping("src/auth.ts", page)
manager.save_mapping()
```

---

### 4.2 `process_documentation_to_wiki(doc_files: List[str]) -> List[Dict]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `doc_files` | `List[str]` | Paths to Markdown documentation files (e.g., `docs/auth.md`). |

| Return | Description |
|--------|-------------|
| `List[Dict]` | Each dict contains `file` (source file path) and `page` (wiki page name). |

#### Flow

1. **Instantiate** `WikiManager`.
2. **Iterate** over each Markdown file:
   - Read the file.
   - Infer the corresponding source file (`<name>.ts`, `<name>.js`, `<name>.py`, or `src/<name>.ts`).
   - Call `determine_wiki_page` to get the target page.
   - Call `update_wiki_page` to write the Markdown to `wiki_updates/`.
   - Record the mapping.
3. **Persist** mapping, verify consistency, and generate a summary.
4. **Return** the list of updates.

#### Example

```python
updates = process_documentation_to_wiki(["docs/auth.md", "docs/database.md"])
# updates → [{'file': 'src/auth.ts', 'page': 'Authentication-API'}, ...]
```

---

### 4.3 `__main__` block

The script expects the following files/structure:

| Item | What it is | How it is used |
|------|------------|----------------|
| `changed_files.txt` | Text file listing changed source files (one per line). | The script reads this to determine which docs to process. |
| `docs/` | Directory containing Markdown docs. | Each doc is named `<source_stem>.md`. |
| `wiki_updates/` | Temporary output folder. | The script writes updated Markdown files here; a CI workflow can commit them to the GitHub Wiki. |
| `.github/wiki-mapping.json` | Persistent mapping file. | Updated automatically. |
| `wiki_summary.md` | Summary of wiki organization. | Generated at the end of the run. |

> **Tip:** Add a GitHub Actions workflow that runs this script on every push to `main` or on a schedule, then commits the `wiki_updates/` folder to the Wiki.

---

## 5️⃣ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ | – | API key for