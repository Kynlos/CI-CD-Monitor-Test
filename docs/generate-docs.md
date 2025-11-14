# generate-docs.py

*Auto-generated from `.github/scripts/generate-docs.py`*

API Documentation
================

Overview
--------

This module is an Advanced Auto Documentation Generator for CI/CD. It features:

* Breaking change detection with auto-labeling
* Changelog generation
* Diff-aware documentation (only changed code)
* Cross-file impact analysis
* Smart PR comments

Exports
-------

### Functions

* `extract_symbols_detailed(content)`: Extract symbols with detailed information from a given code content.
* `detect_breaking_changes(old_content, new_content)`: Detect breaking changes between two versions of code content.
* `get_git_diff(file_path)`: Get git diff for a file.
* `analyze_cross_file_impact(files_data)`: Analyze cross-file dependencies and impacts.
* `generate_changelog_entry(file_path, old_content, new_content, breaking_info)`: Generate changelog entry for a change.
* `generate_documentation(file_context, file_path)`: Generate documentation using Groq API.
* `generate_impact_analysis(impacts, file_list)`: Generate cross-file impact analysis.
* `update_changelog(entries)`: Update or create CHANGELOG.md.
* `generate_smart_pr_comment(code_files, doc_files, breaking_changes, impacts, changelog_entries)`: Generate comprehensive PR comment.

### Classes

* None

### Interfaces

* None

Usage Examples
-------------

### Extracting Symbols

```python
content = """
export function add(a: number, b: number): number {
  return a + b;
}
"""
symbols = extract_symbols_detailed(content)
print(symbols)  # Output: [{'type': 'function', 'name': 'add', 'params': 'a: number, b: number', 'returns': 'number', 'exported': True, 'signature': 'export function add(a: number, b: number): number'}]
```

### Detecting Breaking Changes

```python
old_content = """
export function add(a: number, b: number): number {
  return a + b;
}
"""
new_content = """
export function add(a: number, b: number, c: number): number {
  return a + b + c;
}
"""
breaking_info = detect_breaking_changes(old_content, new_content)
print(breaking_info)  # Output: {'has_breaking': True, 'changes': [{'type': 'signature_change', 'symbol': 'add', 'severity': 'BREAKING', 'message': 'Modified signature of add', 'old': 'export function add(a: number, b: number): number', 'new': 'export function add(a: number, b: number, c: number): number'}]}
```

### Generating Changelog Entry

```python
file_path = 'path/to/file.ts'
old_content = """
export function add(a: number, b: number): number {
  return a + b;
}
"""
new_content = """
export function add(a: number, b: number, c: number): number {
  return a + b + c;
}
"""
breaking_info = detect_breaking_changes(old_content, new_content)
changelog_entry = generate_changelog_entry(file_path, old_content, new_content, breaking_info)
print(changelog_entry)  # Output: '### ⚠️ BREAKING CHANGES\n- **add**: Modified signature of add\n  - Before: `export function add(a: number, b: number): number`\n  - After: `export function add(a: number, b: number, c: number): number`'
```

Parameters
----------

### extract_symbols_detailed

* `content`: The code content to extract symbols from.

### detect_breaking_changes

* `old_content`: The old version of the code content.
* `new_content`: The new version of the code content.

### get_git_diff

* `file_path`: The path to the file to get the git diff for.

### analyze_cross_file_impact

* `files_data`: A dictionary of file paths to their corresponding code content.

### generate_changelog_entry

* `file_path`: The path to the file that changed.
* `old_content`: The old version of the code content.
* `new_content`: The new version of the code content.
* `breaking_info`: The breaking change information.

### generate_documentation

* `file_context`: The context of the file to generate documentation for.
* `file_path`: The path to the file to generate documentation for.

### generate_impact_analysis

* `impacts`: A list of cross-file impact analysis results.
* `file_list`: A list of file paths.

### update_changelog

* `entries`: A list of changelog entries to update the changelog with.

### generate_smart_pr_comment

* `code_files`: A list of code files that changed.
* `doc_files`: A list of documentation files generated.
* `breaking_changes`: A list of breaking changes detected.
* `impacts`: A list of cross-file impact analysis results.
* `changelog_entries`: A list of changelog entries.

Return Values
--------------

### extract_symbols_detailed

* A list of symbol objects with detailed information.

### detect_breaking_changes

* A dictionary with a boolean `has_breaking` and a list of breaking change objects.

### get_git_diff

* The git diff for the file as a string.

### analyze_cross_file_impact

* A list of cross-file impact analysis results.

### generate_changelog_entry

* The changelog entry as a string.

### generate_documentation

* The generated documentation as a string.

### generate_impact_analysis

* The cross-file impact analysis as a string.

### update_changelog

* None

### generate_smart_pr_comment

* The generated PR comment as a string.