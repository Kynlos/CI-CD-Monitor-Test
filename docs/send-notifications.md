# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

API Documentation for Notification Service
==============================================

### Overview

This module provides a notification service that sends updates to Discord, Slack, and Pushbullet. It handles character limits and formats messages beautifully. The service is designed to be used in a GitHub Actions workflow to notify teams about changes, breaking changes, and updates to wiki pages.

### Exports

* `NotificationService` class: Handles sending notifications to Discord, Slack, and Pushbullet.
* `load_workflow_data` function: Loads data from workflow artifacts.
* `main` function: The entry point of the script.

### Usage Examples

#### Sending Notifications

```python
service = NotificationService()
data = load_workflow_data()

# Send Discord notification
service.send_discord(
    data['changed_files'],
    data['breaking_changes'],
    data['changelog_entries'],
    data['wiki_pages']
)

# Send Slack notification
service.send_slack(
    data['changed_files'],
    data['breaking_changes'],
    data['changelog_entries'],
    data['wiki_pages']
)

# Send Pushbullet notification
service.send_pushbullet(
    data['changed_files'],
    data['breaking_changes'],
    data['changelog_entries'],
    data['wiki_pages']
)
```

#### Loading Workflow Data

```python
data = load_workflow_data()
print(data['changed_files'])  # List of changed files
print(data['breaking_changes'])  # List of breaking changes
print(data['changelog_entries'])  # List of changelog entries
print(data['wiki_pages'])  # List of wiki pages
```

### Parameters

#### `NotificationService` class

* `changed_files`: List of changed files.
* `breaking_changes`: List of breaking changes.
* `changelog_entries`: List of changelog entries.
* `wiki_pages`: List of wiki pages.

#### `load_workflow_data` function

* No parameters.

#### `send_discord` method

* `changed_files`: List of changed files.
* `breaking_changes`: List of breaking changes.
* `changelog_entries`: List of changelog entries.
* `wiki_pages`: List of wiki pages.

#### `send_slack` method

* `changed_files`: List of changed files.
* `breaking_changes`: List of breaking changes.
* `changelog_entries`: List of changelog entries.
* `wiki_pages`: List of wiki pages.

#### `send_pushbullet` method

* `changed_files`: List of changed files.
* `breaking_changes`: List of breaking changes.
* `changelog_entries`: List of changelog entries.
* `wiki_pages`: List of wiki pages.

### Return Values

#### `send_discord` method

* `bool`: Whether the notification was sent successfully.

#### `send_slack` method

* `bool`: Whether the notification was sent successfully.

#### `send_pushbullet` method

* `bool`: Whether the notification was sent successfully.

#### `load_workflow_data` function

* `dict`: A dictionary containing the loaded data.

### Environment Variables

The following environment variables are required:

* `DISCORD_WEBHOOK_URL`: The Discord webhook URL.
* `SLACK_WEBHOOK_URL`: The Slack webhook URL.
* `PUSHBULLET_TOKEN`: The Pushbullet token.
* `GITHUB_REPOSITORY`: The GitHub repository name.
* `GITHUB_SHA`: The GitHub commit SHA.
* `GITHUB_ACTOR`: The GitHub actor name.
* `GITHUB_RUN_ID`: The GitHub run ID.
* `COMMIT_MESSAGE`: The commit message.