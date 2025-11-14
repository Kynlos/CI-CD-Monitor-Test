# agentic-bot.py

*Auto-generated from `.github/scripts/agentic-bot.py`*

Agentic PR Bot API Documentation
================================

### Overview

The Agentic PR Bot is a Python module designed to respond to action requests in PR comments and make code changes. It utilizes a large language model (LLM) to generate code changes based on user requests. The bot only works for PR authors and assignees.

### Exports

The following functions are exported by the module:

* `is_authorized(user)`: Checks if a user is authorized to trigger actions.
* `classify_intent(comment_text)`: Classifies the intent of a PR comment and extracts the action requested.
* `load_changed_files()`: Loads the changed files in a PR.
* `generate_code_changes(action_description, files)`: Generates code changes using an LLM.
* `parse_and_apply_changes(llm_output, original_files)`: Parses the LLM output and applies the changes to the files.
* `commit_changes(files_changed, action_description)`: Commits the changes made to the files.

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
intent = classify_intent("Please add comments to this file")
print(intent["category"])  # Output: CLEAR_ACTION
print(intent["action"])  # Output: add comments to this file
```

#### Loading Changed Files

```python
changed_files = load_changed_files()
print(changed_files)  # Output: ["file1.py", "file2.py"]
```

#### Generating Code Changes

```python
llm_output = generate_code_changes("add comments to this file", ["file1.py", "file2.py"])
print(llm_output)  # Output: LLM output with generated code changes
```

#### Parsing and Applying Changes

```python
files_modified = parse_and_apply_changes(llm_output, {"file1.py": "original content"})
print(files_modified)  # Output: ["file1.py"]
```

#### Committing Changes

```python
commit_hash = commit_changes(["file1.py"], "add comments to this file")
print(commit_hash)  # Output: commit hash
```

### Parameters

* `is_authorized(user)`: `user` (str) - The GitHub username to check for authorization.
* `classify_intent(comment_text)`: `comment_text` (str) - The text of the PR comment to classify.
* `load_changed_files()`: No parameters.
* `generate_code_changes(action_description, files)`: 
  * `action_description` (str) - The description of the action to generate code changes for.
  * `files` (list) - A list of file paths to generate code changes for.
* `parse_and_apply_changes(llm_output, original_files)`: 
  * `llm_output` (str) - The output of the LLM with generated code changes.
  * `original_files` (dict) - A dictionary of file paths to their original contents.
* `commit_changes(files_changed, action_description)`: 
  * `files_changed` (list) - A list of file paths that were modified.
  * `action_description` (str) - The description of the action that was performed.

### Return Values

* `is_authorized(user)`: `bool` - Whether the user is authorized or not.
* `classify_intent(comment_text)`: `dict` - A dictionary with the classified intent, including the category, action, confidence, and reasoning.
* `load_changed_files()`: `list` - A list of file paths that were changed in the PR.
* `generate_code_changes(action_description, files)`: `str` - The output of the LLM with generated code changes.
* `parse_and_apply_changes(llm_output, original_files)`: `list` - A list of file paths that were modified.
* `commit_changes(files_changed, action_description)`: `str` - The commit hash of the committed changes, or `None` if the commit failed.