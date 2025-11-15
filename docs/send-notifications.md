# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

Notification Service API Documentation
=====================================

### Overview

This module provides a notification service that sends updates to Discord and Slack. It handles character limits and formats messages beautifully. The service is designed to be used in a GitHub Actions workflow to notify teams about changes to documentation.

### Exports

The following functions and classes are exported by this module:

* `NotificationService`: A class that provides methods for sending notifications to Discord and Slack.
* `load_workflow_data`: A function that loads data from workflow artifacts.
* `main`: The main entry point of the module.

### Usage Examples

#### Creating a Notification Service

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

#### `NotificationService` Class

* `__init__`: Initializes the notification service.
	+ `self.repo`: The GitHub repository name.
	+ `self.commit_sha`: The commit SHA.
	+ `self.commit_message`: The commit message.
	+ `self.actor`: The GitHub actor.
	+ `self.run_url`: The URL of the workflow run.

#### `send_discord` Method

* `changed_files`: A list of changed files.
* `breaking_changes`: A list of breaking changes.
* `changelog_entries`: A list of changelog entries.
* `wiki_pages`: A list of wiki pages.

#### `send_slack` Method

* `changed_files`: A list of changed files.
* `breaking_changes`: A list of breaking changes.
* `changelog_entries`: A list of changelog entries.
* `wiki_pages`: A list of wiki pages.

#### `load_workflow_data` Function

* No parameters.

#### `main` Function

* No parameters.

### Return Values

#### `send_discord` Method

* `bool`: Whether the notification was sent successfully.

#### `send_slack` Method

* `bool`: Whether the notification was sent successfully.

#### `load_workflow_data` Function

* `dict`: A dictionary containing the loaded data.

#### `main` Function

* No return value.

### Environment Variables

The following environment variables are used by this module:

* `DISCORD_WEBHOOK_URL`: The URL of the Discord webhook.
* `SLACK_WEBHOOK_URL`: The URL of the Slack webhook.
* `GITHUB_REPOSITORY`: The GitHub repository name.
* `GITHUB_SHA`: The commit SHA.
* `GITHUB_ACTOR`: The GitHub actor.
* `GITHUB_RUN_ID`: The ID of the workflow run.
* `COMMIT_MESSAGE`: The commit message.