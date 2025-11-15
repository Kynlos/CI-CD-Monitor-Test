# pr-bump-notify.py

*Auto-generated from `.github/scripts/pr-bump-notify.py`*

PR Bump Notification API
========================
## Overview
The PR Bump Notification module is designed to detect when a pull request (PR) is bumped by a user, typically by leaving a comment containing specific keywords. When a bump is detected, the module sends notifications to Discord and/or Slack using webhooks.

## Exports
The following functions are exported by this module:

* `is_bump_comment(comment: str) -> bool`: Checks if a comment contains bump keywords.
* `truncate(text: str, limit: int) -> str`: Truncates a text to fit within a specified limit.
* `send_discord_notification(comment: str, user: str) -> bool`: Sends a PR bump notification to Discord.
* `send_slack_notification(comment: str, user: str) -> bool`: Sends a PR bump notification to Slack.

## Usage Examples
### Checking for Bump Comments
```python
comment = "Please review this PR"
if is_bump_comment(comment):
    print("Bump comment detected")
```

### Truncating Text
```python
text = "This is a very long text that needs to be truncated"
truncated_text = truncate(text, 20)
print(truncated_text)  # Output: "This is a very..."
```

### Sending Discord Notifications
```python
comment = "Please review this PR"
user = "johnDoe"
if send_discord_notification(comment, user):
    print("Discord notification sent successfully")
```

### Sending Slack Notifications
```python
comment = "Please review this PR"
user = "johnDoe"
if send_slack_notification(comment, user):
    print("Slack notification sent successfully")
```

## Parameters
### `is_bump_comment`
* `comment`: The comment to check for bump keywords (string)

### `truncate`
* `text`: The text to truncate (string)
* `limit`: The maximum length of the truncated text (integer)

### `send_discord_notification`
* `comment`: The comment that triggered the notification (string)
* `user`: The user who made the comment (string)

### `send_slack_notification`
* `comment`: The comment that triggered the notification (string)
* `user`: The user who made the comment (string)

## Return Values
### `is_bump_comment`
* `bool`: True if the comment contains bump keywords, False otherwise

### `truncate`
* `str`: The truncated text

### `send_discord_notification`
* `bool`: True if the notification was sent successfully, False otherwise

### `send_slack_notification`
* `bool`: True if the notification was sent successfully, False otherwise

## Environment Variables
The following environment variables are required for this module to function:

* `DISCORD_WEBHOOK_URL`: The URL of the Discord webhook
* `SLACK_WEBHOOK_URL`: The URL of the Slack webhook
* `COMMENT_BODY`: The body of the comment that triggered the notification
* `COMMENT_USER`: The user who made the comment
* `PR_NUMBER`: The number of the pull request
* `PR_TITLE`: The title of the pull request
* `PR_URL`: The URL of the pull request
* `REPO_NAME`: The name of the repository