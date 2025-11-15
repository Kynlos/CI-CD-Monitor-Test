# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

API Documentation for `send-notifications.py`
==============================================

### Overview

This module provides a notification service that sends updates to Discord and Slack. It handles character limits and formats messages beautifully. The service is designed to be used in a GitHub Actions workflow, where it can send notifications about changes, breaking changes, and wiki updates.

### Exports

The following functions and classes are exported by this module:

* `NotificationService`: A class that provides methods for sending notifications to Discord and Slack.
* `load_workflow_data`: A function that loads data from workflow artifacts.
* `main`: The main entry point of the module.

### Usage Examples

#### Sending a Discord Notification

```python
service = NotificationService()
changed_files = ['file1.txt', 'file2.txt']
breaking_changes = [{'symbol': 'API', 'message': 'Breaking changes detected'}]
changelog_entries = []
wiki_pages = []

success = service.send_discord(changed_files, breaking_changes, changelog_entries, wiki_pages)
```

#### Sending a Slack Notification

```python
service = NotificationService()
changed_files = ['file1.txt', 'file2.txt']
breaking_changes = [{'symbol': 'API', 'message': 'Breaking changes detected'}]
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

#### `NotificationService`

* `None`: The constructor takes no parameters.

#### `send_discord`

* `changed_files`: A list of files that have changed.
* `breaking_changes`: A list of breaking changes.
* `changelog_entries`: A list of changelog entries.
* `wiki_pages`: A list of wiki pages that have been updated.

#### `send_slack`

* `changed_files`: A list of files that have changed.
* `breaking_changes`: A list of breaking changes.
* `changelog_entries`: A list of changelog entries.
* `wiki_pages`: A list of wiki pages that have been updated.

#### `load_workflow_data`

* `None`: The function takes no parameters.

### Return Values

#### `send_discord`

* `bool`: Whether the notification was sent successfully.

#### `send_slack`

* `bool`: Whether the notification was sent successfully.

#### `load_workflow_data`

* `dict`: A dictionary containing the loaded data, with the following keys:
	+ `changed_files`: A list of files that have changed.
	+ `breaking_changes`: A list of breaking changes.
	+ `changelog_entries`: A list of changelog entries.
	+ `wiki_pages`: A list of wiki pages that have been updated.

#### `main`

* `None`: The function does not return a value.

### Classes

#### `NotificationService`

This class provides methods for sending notifications to Discord and Slack. It has the following attributes:

* `repo`: The name of the repository.
* `commit_sha`: The SHA of the commit.
* `commit_message`: The commit message.
* `actor`: The actor who made the commit.
* `run_url`: The URL of the workflow run.

The class has the following methods:

* `send_discord`: Sends a notification to Discord.
* `send_slack`: Sends a notification to Slack.
* `_clean_commit_message`: Cleans the commit message by removing Amp-specific lines.
* `truncate`: Truncates a string to fit within a limit.