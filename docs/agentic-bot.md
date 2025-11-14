# agentic-bot.py

*Auto-generated from `.github/scripts/agentic-bot.py`*

Agentic PR Bot API Documentation
================================

### Overview

The Agentic PR Bot is a Python module designed to respond to action requests in PR comments and make code changes. It utilizes a large language model (LLM) to generate code changes based on user requests. The module is intended for use in GitHub Actions workflows.

### Exports

The following functions are exported by the module:

* `is_authorized(user)`: Checks if a user is authorized to trigger actions.
* `classify_intent(comment_text)`: Classifies the intent of a PR comment.
* `load_changed_files()`: Loads the changed files in a PR.
* `generate_code_changes(action_description, files)`: Generates code changes using an LLM.
* `parse_and_apply_changes(llm_output, original_files)`: Parses LLM output and applies changes to files.
* `commit_changes(files_changed, action_description)`: Commits changes to a repository.

### Usage Examples

#### Checking Authorization

```python
if is_authorized("github_username"):
    print("User is authorized")
else:
    print("User is not authorized")
```

#### Classifying Intent

```python
intent = classify_intent("Please add comments to file.ts")
print(intent["category"])  # Output: CLEAR_ACTION
print(intent["action"])  # Output: add comments to file.ts
```

#### Loading Changed Files

```python
changed_files = load_changed_files()
print(changed_files)  # Output: ["file1.ts", "file2.js"]
```

#### Generating Code Changes

```python
llm_output = generate_code_changes("add comments to file.ts", ["file1.ts", "file2.js"])
print(llm_output)  # Output: LLM output containing modified file contents
```

#### Parsing and Applying Changes

```python
original_files = {"file1.ts": "original content"}
files_modified = parse_and_apply_changes(llm_output, original_files)
print(files_modified)  # Output: ["file1.ts"]
```

#### Committing Changes

```python
commit_hash = commit_changes(["file1.ts"], "add comments to file.ts")
print(commit_hash)  # Output: commit hash
```

### Parameters

* `is_authorized(user)`: `user` (str) - The GitHub username to check for authorization.
* `classify_intent(comment_text)`: `comment_text` (str) - The PR comment text to classify.
* `load_changed_files()`: No parameters.
* `generate_code_changes(action_description, files)`: 
	+ `action_description` (str) - The description of the action to generate code changes for.
	+ `files` (list[str]) - The list of files to generate code changes for.
* `parse_and_apply_changes(llm_output, original_files)`: 
	+ `llm_output` (str) - The LLM output containing modified file contents.
	+ `original_files` (dict[str, str]) - The original file contents for security checking.
* `commit_changes(files_changed, action_description)`: 
	+ `files_changed` (list[str]) - The list of files that have been modified.
	+ `action_description` (str) - The description of the action that was performed.

### Return Values

* `is_authorized(user)`: `bool` - Whether the user is authorized to trigger actions.
* `classify_intent(comment_text)`: `dict` - A dictionary containing the classified intent, including the category, action, confidence, and reasoning.
* `load_changed_files()`: `list[str]` - The list of changed files in the PR.
* `generate_code_changes(action_description, files)`: `str` - The LLM output containing modified file contents.
* `parse_and_apply_changes(llm_output, original_files)`: `list[str]` - The list of files that have been modified.
* `commit_changes(files_changed, action_description)`: `str` - The commit hash of the committed changes, or `None` if the commit failed.