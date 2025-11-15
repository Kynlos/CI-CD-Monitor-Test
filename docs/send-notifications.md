# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

API Documentation for Notification Service
==============================================

### Overview

The Notification Service is a Python module designed to send updates to Discord and Slack. It handles character limits and formats messages beautifully. The module is intended for use in GitHub Actions workflows to notify teams of changes to documentation, including breaking changes, updated files, and wiki pages.

### Exports

The module exports the following functions and classes:

* `NotificationService` class:
	+ `__init__`: Initializes the notification service with environment variables.
	+ `truncate`: Truncates text to fit within a specified limit.
	+ `send_discord`: Sends a formatted notification to Discord.
	+ `send_slack`: Sends a formatted notification to Slack.
* `load_workflow_data`: Loads data from workflow artifacts.
* `main`: The main entry point of the module.

### Usage Examples

#### Initializing the Notification Service

```python
service = NotificationService()
```

#### Sending a Discord Notification

```python
changed_files = ['file1.txt', 'file2.txt']
breaking_changes = [{'symbol': 'API', 'message': 'Breaking change'}]
changelog_entries = []
wiki_pages = []

success = service.send_discord(changed_files, breaking_changes, changelog_entries, wiki_pages)
```

#### Sending a Slack Notification

```python
changed_files = ['file1.txt', 'file2.txt']
breaking_changes = [{'symbol': 'API', 'message': 'Breaking change'}]
changelog_entries = []
wiki_pages = []

success = service.send_slack(changed_files, breaking_changes, changelog_entries, wiki_pages)
```

#### Loading Workflow Data

```python
data = load_workflow_data()
print(data['changed_files'])
print(data['breaking_changes'])
print(data['wiki_pages'])
```

### Parameters

#### `NotificationService` class

* `__init__`: No parameters.
* `truncate`:
	+ `text` (str): The text to truncate.
	+ `limit` (int): The character limit.
* `send_discord`:
	+ `changed_files` (List[str]): A list of changed files.
	+ `breaking_changes` (List[Dict]): A list of breaking changes.
	+ `changelog_entries` (List[Dict]): A list of changelog entries.
	+ `wiki_pages` (List[str]): A list of updated wiki pages.
* `send_slack`:
	+ `changed_files` (List[str]): A list of changed files.
	+ `breaking_changes` (List[Dict]): A list of breaking changes.
	+ `changelog_entries` (List[Dict]): A list of changelog entries.
	+ `wiki_pages` (List[str]): A list of updated wiki pages.

#### `load_workflow_data` function

* No parameters.

#### `main` function

* No parameters.

### Return Values

#### `NotificationService` class

* `truncate`: The truncated text (str).
* `send_discord`: A boolean indicating whether the notification was sent successfully (bool).
* `send_slack`: A boolean indicating whether the notification was sent successfully (bool).

#### `load_workflow_data` function

* A dictionary containing the loaded data (Dict).

#### `main` function

* No return value.