# wiki-manager.py

*Auto-generated from `.github/scripts/wiki-manager.py`*

Wiki Manager API Documentation
==============================

### Overview

The Wiki Manager is a Python module designed to intelligently route documentation to GitHub Wiki pages. It features persistent mapping, smart routing decisions, LLM-powered categorization, verification, and consistency checks.

### Exports

The Wiki Manager module exports the following functions and classes:

* `WikiManager` class: The main class responsible for managing wiki pages and mappings.
* `process_documentation_to_wiki` function: The main function that processes documentation files and routes them to wiki pages.

### Usage Examples

#### Creating a Wiki Manager Instance

```python
manager = WikiManager()
```

#### Processing Documentation Files

```python
doc_files = ['docs/auth.md', 'docs/database.md']
process_documentation_to_wiki(doc_files)
```

#### Determining Wiki Page for a File

```python
file_path = 'src/auth.ts'
file_content = '...file content...'
page_name = manager.determine_wiki_page(file_path, file_content)
print(page_name)  # Output: Authentication-API
```

### Parameters

#### `WikiManager` Class

* `None`: The `WikiManager` class does not take any parameters.

#### `process_documentation_to_wiki` Function

* `doc_files`: A list of documentation file paths to process.

#### `determine_wiki_page` Method

* `file_path`: The path to the file for which to determine the wiki page.
* `file_content`: The content of the file.

#### `update_wiki_page` Method

* `page_name`: The name of the wiki page to update.
* `content`: The content to update the wiki page with.

### Return Values

#### `process_documentation_to_wiki` Function

* A list of updates made to the wiki pages.

#### `determine_wiki_page` Method

* The name of the wiki page determined for the file.

#### `update_wiki_page` Method

* A boolean indicating whether the update was successful.

### WikiManager Class Methods

#### `load_mapping`

* Loads the persistent wiki mapping from disk.
* Returns: The loaded mapping.

#### `save_mapping`

* Saves the wiki mapping to disk.
* Returns: None

#### `fetch_wiki_pages`

* Fetches all existing wiki page names from GitHub.
* Returns: A list of wiki page names.

#### `record_mapping`

* Records the file-to-page mapping.
* Returns: None

#### `verify_consistency`

* Verifies the consistency of the mapping.
* Returns: A boolean indicating whether the mapping is consistent.

#### `generate_summary`

* Generates a summary of the wiki organization.
* Returns: The summary as a string.

### Notes

* The `WikiManager` class uses environment variables to store GitHub credentials and other configuration.
* The `process_documentation_to_wiki` function assumes that the documentation files are in the `docs` directory.
* The `determine_wiki_page` method uses a LLM to determine the wiki page for a file. If the LLM fails, it falls back to a simple naming convention.