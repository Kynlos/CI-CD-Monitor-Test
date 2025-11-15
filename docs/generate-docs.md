# generate-docs.py

*Auto-generated from `.github/scripts/generate-docs.py`*

# Advanced Auto‑Documentation Generator

> **File:** `.github/scripts/generate‑docs.py`  
> **Language:** Python 3  
> **Purpose:**  
> Automates the creation of API documentation, changelog entries, and PR comments for a codebase that has changed in a pull request.  
> It analyses TypeScript/JavaScript, Python, Go, Rust, Java, C/C++ files, detects breaking changes, cross‑file impacts, and then uses the Groq API to generate human‑readable Markdown documentation for each changed file.

---

## 1. Overview

The script is a CI‑friendly tool that:

1. **Detects changed files** (via a pre‑generated `changed_files.txt`).
2. **Filters code files** by extension (`.ts`, `.js`, `.tsx`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cpp`, `.cc`, `.c`, `.h`, `.hpp`).
3. **Compares the current and previous versions** of each file to find:
   * Removed or added exports
   * Signature changes (parameters, return types)
   * Cross‑file references that may be affected
4. **Generates a changelog** entry for each file.
5. **Creates Markdown documentation** for each file using the Groq LLM.
6. **Builds a PR comment** summarizing breaking changes, impacted files, and links to the generated docs.
7. **Writes a `breaking_changes.txt` flag** if any breaking changes are detected (used by CI to auto‑label PRs).

The script is intended to be run in a GitHub Actions workflow or locally before a PR is merged.

---

## 2. Exports

| Function | Description |
|----------|-------------|
| `extract_symbols_detailed(content: str) -> List[Dict]` | Parses a source file and returns a list of exported symbols (functions, classes, interfaces) with detailed metadata. |
| `detect_breaking_changes(old_content: str, new_content: str) -> Dict` | Compares two versions of a file and returns a dict indicating whether breaking changes exist and a list of those changes. |
| `get_git_diff(file_path: str) -> str` | Returns the `git diff` between the last two commits for a given file. |
| `analyze_cross_file_impact(files_data: Dict[str, str]) -> List[Dict]` | Detects references to changed symbols across the entire set of changed files. |
| `generate_changelog_entry(file_path: str, old_content: str, new_content: str, breaking_info: Dict) -> Optional[str]` | Builds a Markdown snippet for the changelog for a single file. |
| `generate_documentation(file_context: str, file_path: str) -> str` | Calls the Groq API to generate comprehensive documentation for a file. |
| `generate_impact_analysis(impacts: List[Dict], file_list: List[str]) -> str` | Creates a Markdown section describing cross‑file impacts. |
| `update_changelog(entries: List[Dict]) -> None` | Inserts new changelog entries into `CHANGELOG.md`. |
| `generate_smart_pr_comment(code_files: List[str], doc_files: List[str], breaking_changes: List[Dict], impacts: List[Dict], changelog_entries: List[Dict]) -> str` | Builds a PR comment summarizing everything. |
| `main() -> None` | Orchestrates the entire workflow. |

---

## 3. Usage Examples

### 3.1 `extract_symbols_detailed`

```python
source = """
export async function fetchData(url: string): Promise<Data> {
  // ...
}

export class User {
  constructor(public name: string) {}
}
"""

symbols = extract_symbols_detailed(source)
print(symbols)
# [
#   {'type': 'function', 'name': 'fetchData', 'params': 'url: string', 'returns': 'Promise<Data>', 'exported': True, 'signature': 'export async function fetchData(url: string): Promise<Data>'},
#   {'type': 'class', 'name': 'User', 'exported': True, 'signature': 'export class User'}
# ]
```

### 3.2 `detect_breaking_changes`

```python
old = "export function foo(a: number): number { return a; }"
new = "export function foo(a: number, b: number): number { return a + b; }"

info = detect_breaking_changes(old, new)
print(info['has_breaking'])  # True
print(info['changes'])
# [{'type': 'signature_change', 'symbol': 'foo', 'severity': 'BREAKING', 'message': 'Modified signature of foo', 'old': 'export function foo(a: number): number', 'new': 'export function foo(a: number, b: number): number'}]
```

### 3.3 `get_git_diff`

```python
diff = get_git_diff('src/utils/helpers.ts')
print(diff)  # Shows the diff between HEAD~1 and HEAD
```

### 3.4 `analyze_cross_file_impact`

```python
files = {
    'src/a.ts': 'export function foo() {}',
    'src/b.ts': 'import { foo } from "./a"; foo();'
}
impacts = analyze_cross_file_impact(files)
print(impacts)
# [{'changed_file': 'a.ts', 'affects_file': 'b.ts', 'symbol': 'foo', 'type': 'function'}]
```

### 3.5 `generate_changelog_entry`

```python
entry = generate_changelog_entry(
    'src/foo.ts',
    old_content="export function bar() {}",
    new_content="export function bar() {} export function baz() {}",
    breaking_info={'has_breaking': False, 'changes': []}
)
print(entry)
# ### ✨ Added
# - `baz` (function)
```

### 3.6 `generate_documentation`

```python
doc = generate_documentation(
    file_context="export function add(a: number, b: number): number { return a + b; }",
    file_path="src/math.ts"
)
print(doc)  # Markdown generated by Groq
```

### 3.7 `generate_impact_analysis`

```python
analysis = generate_impact_analysis(
    impacts=[{'changed_file': 'a.ts', 'affects_file': 'b.ts', 'symbol': 'foo', 'type': 'function'}],
    file_list=['src/a.ts', 'src/b.ts']
)
print(analysis)
# ## 🔗 Cross-File Impact Analysis
#
# These changes may affect other parts of the codebase:
#
# ### a.ts
# - References `foo` from `b.ts`
```

### 3.8 `generate_smart_pr_comment`

```python
comment = generate_smart_pr_comment(
    code_files=['src/a.ts'],
    doc_files=['docs/a.md'],
    breaking_changes=[{'symbol': 'foo', 'message': 'Removed exported function foo'}],
    impacts=[{'changed_file': 'a.ts', 'affects_file': 'b.ts', 'symbol': 'foo', 'type': 'function'}],
    changelog_entries=[{'file': 'a.ts', 'content': '### ✨ Added\n- `bar` (function)'}]
)
print(comment)
# (Markdown PR comment)
```

---

## 4. Parameters & Return Values

| Function | Parameters | Return Type | Description |
|----------|------------|-------------|-------------|
| `extract_symbols_detailed` | `content: str` | `List[Dict]` | List of symbol dicts: `{'type', 'name', 'params', 'returns', 'exported', 'signature'}`. |
| `detect_breaking_changes` | `old_content: str`, `new_content: str` | `Dict` | `{'has_breaking': bool, 'changes': List[Dict]}`. Each change dict contains `type`, `symbol`, `severity`, `message`, and optionally `old`/`new`. |
| `get_git_diff` | `file_path: str` | `str` | Diff string or empty if error. |
| `analyze_cross_file_impact` | `files_data: Dict[str, str]` | `List[Dict]` | Each dict: `{'changed_file', 'affects_file', 'symbol', 'type'}`. |
| `generate_changelog_entry`