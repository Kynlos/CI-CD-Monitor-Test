# agentic-bot.py

*Auto-generated from `.github/scripts/agentic-bot.py`*

API Documentation for Agentic Bot
=====================================

### Overview

The Agentic Bot is a Python module designed to respond to action requests in PR comments and make code changes. It utilizes a large language model (LLM) to generate code changes based on user requests. The bot only works for PR authors and assignees.

### Exports

The following functions are exported by the Agentic Bot module:

* `is_authorized(user)`: Checks if a user is authorized to trigger actions.
* `classify_intent(comment_text)`: Classifies the intent of a PR comment and extracts the requested action.
* `load_changed_files()`: Loads the changed files of a PR.
* `generate_code_changes(action_description, files)`: Generates code changes using an LLM based on the requested action and changed files.
* `parse_and_apply_changes(llm_output, original_files)`: Parses the LLM output and applies the changes to the original files.
* `commit_changes(files_changed, action_description)`: Commits the changes to the repository.

### Usage Examples

#### Checking Authorization

```python
if is_authorized("username"):
    print("User is authorized")
else:
    print("User is not authorized")
```

#### Classifying Intent

```python
intent = classify_intent("Add comments to file.ts")
print(intent["category"])  # Output: CLEAR_ACTION
print(intent["action"])  # Output: Add comments to file.ts
```

#### Loading Changed Files

```python
changed_files = load_changed_files()
print(changed_files)  # Output: ["file1.ts", "file2.ts"]
```

#### Generating Code Changes

```python
llm_output = generate_code_changes("Add comments to file.ts", ["file1.ts", "file2.ts"])
print(llm_output)  # Output: LLM output containing the modified files
```

#### Parsing and Applying Changes

```python
original_files = {"file1.ts": "original content"}
files_modified = parse_and_apply_changes(llm_output, original_files)
print(files_modified)  # Output: ["file1.ts"]
```

#### Committing Changes

```python
commit_hash = commit_changes(["file1.ts"], "Add comments to file.ts")
print(commit_hash)  # Output: Commit hash
```

### Parameters

* `is_authorized(user)`: `user` (str) - The username to check for authorization.
* `classify_intent(comment_text)`: `comment_text` (str) - The PR comment text to classify.
* `load_changed_files()`: No parameters.
* `generate_code_changes(action_description, files)`: 
	+ `action_description` (str) - The requested action.
	+ `files` (list) - The changed files of the PR.
* `parse_and_apply_changes(llm_output, original_files)`: 
	+ `llm_output` (str) - The LLM output containing the modified files.
	+ `original_files` (dict) - The original file contents.
* `commit_changes(files_changed, action_description)`: 
	+ `files_changed` (list) - The files that have been modified.
	+ `action_description` (str) - The requested action.

### Return Values

* `is_authorized(user)`: `bool` - Whether the user is authorized.
* `classify_intent(comment_text)`: `dict` - The classified intent containing the category, action, confidence, and reasoning.
* `load_changed_files()`: `list` - The changed files of the PR.
* `generate_code_changes(action_description, files)`: `str` - The LLM output containing the modified files.
* `parse_and_apply_changes(llm_output, original_files)`: `list` - The files that have been modified.
* `commit_changes(files_changed, action_description)`: `str` - The commit hash or `None` if the commit failed.