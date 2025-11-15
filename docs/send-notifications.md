# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

# 📬 `send-notifications.py` – Notification Service

> **What it does**  
> A lightweight CI/CD helper that reads the results of a GitHub Actions run (changed files, breaking changes, changelog snippets, wiki updates, and static‑analysis metrics) and posts a nicely formatted summary to **Discord**, **Slack**, or **Pushbullet**.  
> The script is intended to be run as a final step in a workflow and relies on a handful of environment variables for configuration.

---

## 📦 Exports

| Export | Type | Description |
|--------|------|-------------|
| `NotificationService` | Class | Main helper that formats and sends notifications. |
| `load_workflow_data()` | Function | Reads artifact files produced earlier in the workflow and returns a dictionary of data. |
| `main()` | Function | Entry‑point that orchestrates data loading, prints a summary, and dispatches notifications. |

> **Note**: The module also defines a few module‑level constants (`DISCORD_WEBHOOK`, `SLACK_WEBHOOK`, `PUSHBULLET_TOKEN`, and Discord limits). They are not exported but are used internally.

---

## 🛠️ `NotificationService`

```python
class NotificationService:
    def __init__(self) -> None
    def _clean_commit_message(self, message: str) -> str
    def truncate(self, text: str, limit: int) -> str
    def send_discord(self,
                     changed_files: List[str],
                     breaking_changes: List[Dict],
                     changelog_entries: List[Dict],
                     wiki_pages: List[str],
                     analysis_summary: Optional[Dict] = None) -> bool
    def send_slack(self,
                   changed_files: List[str],
                   breaking_changes: List[Dict],
                   changelog_entries: List[Dict],
                   wiki_pages: List[str],
                   analysis_summary: Optional[Dict] = None) -> bool
    def send_pushbullet(self,
                        changed_files: List[str],
                        breaking_changes: List[Dict],
                        changelog_entries: List[Dict],
                        wiki_pages: List[str],
                        analysis_summary: Optional[Dict] = None) -> bool
```

### Constructor

```python
NotificationService()
```

*Initialises the service by reading the following environment variables:*

| Variable | Default | Meaning |
|----------|---------|---------|
| `GITHUB_REPOSITORY` | `'Unknown Repo'` | `owner/repo` |
| `GITHUB_SHA` | `'unknown'` | Full commit SHA (first 7 chars used) |
| `COMMIT_MESSAGE` | `'No message'` | Commit body |
| `GITHUB_ACTOR` | `'Unknown'` | User who triggered the run |
| `GITHUB_RUN_ID` | `''` | Run ID used to build the workflow‑run URL |

### `_clean_commit_message(message: str) -> str`

*Removes Amp‑specific metadata from a commit message.*

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Raw commit message |

**Returns**: `str` – cleaned commit message.

### `truncate(text: str, limit: int) -> str`

*Truncates a string to a maximum length, appending an ellipsis.*

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Text to truncate |
| `limit` | `int` | Maximum allowed length |

**Returns**: `str` – truncated string.

### `send_discord(...) -> bool`

Sends a Discord webhook payload.

| Parameter | Type | Description |
|-----------|------|-------------|
| `changed_files` | `List[str]` | Paths of files changed in the commit. |
| `breaking_changes` | `List[Dict]` | List of breaking‑change objects (`{'symbol': str, 'message': str}`). |
| `changelog_entries` | `List[Dict]` | List of changelog snippets (`{'file': str, 'content': str}`). |
| `wiki_pages` | `List[str]` | Names of wiki pages that were updated. |
| `analysis_summary` | `Optional[Dict]` | Summary of static‑analysis results. |

**Return**: `bool` – `True` if the webhook returned HTTP 204, otherwise `False`.

### `send_slack(...) -> bool`

Sends a Slack incoming‑webhook payload.

Parameters are identical to `send_discord`.  
**Return**: `bool` – `True` if the webhook returned HTTP 200, otherwise `False`.

### `send_pushbullet(...) -> bool`

Sends a Pushbullet link push.

Parameters are identical to `send_discord`.  
**Return**: `bool` – `True` if the Pushbullet API returned 200/201, otherwise `False`.

---

## 📂 `load_workflow_data() -> Dict`

Loads artifact files that were produced earlier in the workflow.

| File | What it provides |
|------|------------------|
| `changed_files.txt` | One file path per line. |
| `breaking_changes.txt` | Presence indicates breaking changes (default stub). |
| `wiki_summary.md` | Markdown containing a `## Updates Made` section; extracts page names. |
| `doc_output.md` | Optional detailed breaking‑change list. |
| `analysis_results.json` | Static‑analysis results; computes a summary. |

**Return**: `Dict` with keys:

| Key | Type | Description |
|-----|------|-------------|
| `changed_files` | `List[str]` |
| `breaking_changes` | `List[Dict]` |
| `changelog_entries` | `List[Dict]` |
| `wiki_pages` | `List[str]` |
| `analysis_summary` | `Optional[Dict]` |

---

## 🚀 `main()`

Entry‑point that:

1. Prints a header.
2. Reads the latest commit message via `git log`.
3. Calls `load_workflow_data()`.
4. Instantiates `NotificationService`.
5. Prints a quick analysis summary.
6. Dispatches notifications to any configured platform.
7. Prints a final status table.

**Return**: `None` (exits with `sys.exit(0)` implicitly).

---

## 📚 Usage Examples

### 1. Using the Service in a Workflow

```yaml
# .github/workflows/notify.yml
name: Notify

on:
  push:
    branches: [main]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ... earlier steps that generate artifacts ...

      - name: Run notification script
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
          PUSHBULLET: ${{ secrets.PUSHBULLET_TOKEN }}
        run: |
          python3 .github/scripts/send-notifications.py
```

### 2. Manual Invocation

```bash
# Set required env vars
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export PUSHBULLET="o.xxxxxxx"

# Run the script
python3 .github/scripts/send-notifications.py
```

### 3. Importing the Service in Python

```python
from send_notifications import NotificationService, load_workflow_data

data = load_workflow_data()
service = NotificationService()

service.send_discord(
    data['changed_files'],
    data['breaking_changes'],
    data['changelog_entries'],
    data['wiki_pages'],
    data.get('analysis_summary')
)
```

---

## 📦 Environment Variables

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `DISCORD_WEBHOOK_URL` | No | `https://discord.com/api/webhooks/...` | Discord webhook endpoint |
| `SLACK_WEBHOOK_URL` | No | `https://hooks.slack.com/services/...` | Slack incoming webhook |
| `PUSHBULLET` | No | `o.xxxxxxx` | Pushbullet access token |
| `GITHUB_REPOSITORY` | Yes (GitHub Action) |