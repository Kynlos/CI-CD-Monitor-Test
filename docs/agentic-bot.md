# agentic-bot.py

*Auto-generated from `.github/scripts/agentic-bot.py`*

Agentic PR Bot API Documentation
================================

### Overview

The Agentic PR Bot is a Python module designed to respond to action requests in PR comments and make code changes. It utilizes a large language model (LLM) to generate code changes based on user requests. The bot only works for PR authors and assignees.

### Exports

The following functions are exported by the module:

* `is_authorized(user)`: Checks if a user is authorized to trigger actions.
* `classify_intent(comment_text)`: Classifies the intent of a PR comment into one of three categories: CLEAR_ACTION, POSSIBLE_ACTION, or QUESTION_ONLY.
* `load_changed_files()`: Loads the PR's changed files.
* `generate_code_changes(action_description, files)`: Uses an LLM to generate code changes based on a user's request.
* `parse_and_apply_changes(llm_output, original_files)`: Parses the LLM output and applies the changes to the files.
* `commit_changes(files_changed, action_description)`: Commits the changes made by the bot.

### Usage Examples

#### Checking Authorization

```python
if is_authorized("johnDoe"):
    print("User is authorized")
else:
    print("User is not authorized")
```

#### Classifying Intent

```python
intent = classify_intent("Please add comments to this file")
print(intent["category"])  # Output: CLEAR_ACTION
print(intent["action"])  # Output: Add comments to this file
```

#### Loading Changed Files

```python
changed_files = load_changed_files()
print(changed_files)  # Output: List of changed files
```

#### Generating Code Changes

```python
llm_output = generate_code_changes("Add comments to this file", ["file1.py", "file2.py"])
print(llm_output)  # Output: LLM output containing the generated code changes
```

#### Parsing and Applying Changes

```python
files_modified = parse_and_apply_changes(llm_output, {"file1.py": "original content", "file2.py": "original content"})
print(files_modified)  # Output: List of files modified
```

#### Committing Changes

```python
commit_hash = commit_changes(["file1.py", "file2.py"], "Add comments to this file")
print(commit_hash)  # Output: Commit hash
```

### Parameters

* `is_authorized(user)`: `user` (str) - The username to check for authorization.
* `classify_intent(comment_text)`: `comment_text` (str) - The PR comment text to classify.
* `load_changed_files()`: No parameters.
* `generate_code_changes(action_description, files)`: 
	+ `action_description` (str) - The user's request.
	+ `files` (list) - List of files to modify.
* `parse_and_apply_changes(llm_output, original_files)`: 
	+ `llm_output` (str) - The LLM output containing the generated code changes.
	+ `original_files` (dict) - Dictionary of original file contents.
* `commit_changes(files_changed, action_description)`: 
	+ `files_changed` (list) - List of files modified.
	+ `action_description` (str) - The user's request.

### Return Values

* `is_authorized(user)`: `bool` - True if the user is authorized, False otherwise.
* `classify_intent(comment_text)`: `dict` - Dictionary containing the classified intent, action, confidence, and reasoning.
* `load_changed_files()`: `list` - List of changed files.
* `generate_code_changes(action_description, files)`: `str` - LLM output containing the generated code changes.
* `parse_and_apply_changes(llm_output, original_files)`: `list` - List of files modified.
* `commit_changes(files_changed, action_description)`: `str` - Commit hash if the changes are committed successfully, None otherwise.