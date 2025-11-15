# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

# `send-notifications.py` – API Documentation

> **Author**: Amp Team  
> **Version**: 1.0.0  
> **Last updated**: 2025‑11‑15  

---

## 1. Overview

`send-notifications.py` is a self‑contained Python script that aggregates CI/CD workflow data (changed files, breaking changes, wiki updates, and code‑analysis results) and posts a nicely formatted notification to one or more of the following channels:

| Channel | Webhook / Token | Typical Use‑Case |
|---------|-----------------|------------------|
| **Discord** | `DISCORD_WEBHOOK_URL` | Team chat, real‑time alerts |
| **Slack**   | `SLACK_WEBHOOK_URL`   | Team chat, integration with other tools |
| **Pushbullet** | `PUSHBULLET` | Mobile push notifications |

The script is designed to be executed as part of a GitHub Actions workflow. It reads artifacts produced by earlier steps (e.g. `changed_files.txt`, `analysis_results.json`) and sends a concise, emoji‑rich summary to the configured destinations.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `NotificationService` | Class | Main service that builds and sends notifications. |
| `load_workflow_data()` | Function | Loads workflow artifacts and returns a dictionary with all required data. |
| `main()` | Function | Entry point that orchestrates data loading, service creation, and notification dispatch. |

> **Note**: The script is intended to be run directly (`python send-notifications.py`). The `main()` function is called under the `if __name__ == "__main__":` guard.

---

## 3. Usage Examples

### 3.1. Running the Script Manually

```bash
# Set required environment variables
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export PUSHBULLET="YOUR_PUSHBULLET_TOKEN"

# Run the notification script
python .github/scripts/send-notifications.py
```

### 3.2. Using the Service Programmatically

```python
from send_notifications import NotificationService, load_workflow_data

# Load data from artifacts
data = load_workflow_data()

# Create the service
service = NotificationService()

# Send to Discord only
service.send_discord(
    changed_files=data['changed_files'],
    breaking_changes=data['breaking_changes'],
    changelog_entries=data['changelog_entries'],
    wiki_pages=data['wiki_pages'],
    analysis_summary=data.get('analysis_summary')
)
```

---

## 4. Detailed API

### 4.1. `NotificationService`

| Method | Parameters | Return Value | Description |
|--------|------------|--------------|-------------|
| `__init__(self)` | – | `None` | Initializes the service by reading environment variables: `GITHUB_REPOSITORY`, `GITHUB_SHA`, `COMMIT_MESSAGE`, `GITHUB_ACTOR`, `GITHUB_RUN_ID`. |
| `_clean_commit_message(self, message: str) -> str` | `message` – raw commit message | `str` – cleaned message | Removes Amp‑specific metadata lines (`Amp-Thread-ID`, `Co‑authored‑by: Amp`). |
| `truncate(self, text: str, limit: int) -> str` | `text`, `limit` | `str` – truncated text | Truncates `text` to `limit` characters, appending `…` if truncated. |
| `_get_commit_emoji(self, breaking_changes: List[Dict]) -> str` | `breaking_changes` – list of breaking‑change dicts | `str` – emoji | Chooses an emoji based on commit type or presence of breaking changes. |
| `_build_discord_embed_base(self, emoji: str) -> Dict` | `emoji` – emoji string | `dict` – Discord embed base | Builds the base embed (title, description, color, timestamp, footer). |
| `_add_breaking_changes_field(self, embed: Dict, breaking_changes: List[Dict]) -> None` | `embed`, `breaking_changes` | `None` | Adds a “Breaking Changes” field to the embed if any. |
| `_add_files_field(self, embed: Dict, changed_files: List[str]) -> None` | `embed`, `changed_files` | `None` | Adds a “Files Changed” field. |
| `_add_wiki_field(self, embed: Dict, wiki_pages: List[str]) -> None` | `embed`, `wiki_pages` | `None` | Adds a “Wiki Pages Updated” field. |
| `_add_analysis_field(self, embed: Dict, analysis_summary: Optional[Dict]) -> None` | `embed`, `analysis_summary` | `None` | Adds a “Code Analysis” field if analysis data is present. |
| `send_discord(self, changed_files: List[str], breaking_changes: List[Dict], changelog_entries: List[Dict], wiki_pages: List[str], analysis_summary: Optional[Dict] = None) -> bool` | *All data lists/dicts* | `bool` – `True` if the request succeeded (HTTP 204) | Builds the embed, sends it to the Discord webhook, and prints status. |
| `send_slack(self, changed_files: List[str], breaking_changes: List[Dict], changelog_entries: List[Dict], wiki_pages: List[str], analysis_summary: Optional[Dict] = None) -> bool` | *All data lists/dicts* | `bool` – `True` if the request succeeded (HTTP 200) | Builds Slack blocks, posts to the Slack webhook, and prints status. |
| `_build_slack_blocks(self, emoji: str, commit_title: str, breaking_changes: List[Dict], changed_files: List[str], wiki_pages: List[str], analysis_summary: Optional[Dict]) -> List[Dict]` | `emoji`, `commit_title`, `breaking_changes`, `changed_files`, `wiki_pages`, `analysis_summary` | `List[Dict]` – Slack block payload | Constructs the block kit structure for Slack. |
| `send_pushbullet(self, changed_files: List[str], breaking_changes: List[Dict], changelog_entries: List[Dict], wiki_pages: List[str], analysis_summary: Optional[Dict] = None) -> bool` | *All data lists/dicts* | `bool` – `True` if the request succeeded (HTTP 200/201) | Builds a Pushbullet link push and sends it. |

#### Example: Sending a Discord Notification

```python
service = NotificationService()
service.send_discord(
    changed_files=['src/main.py', 'README.md'],
    breaking_changes=[{'symbol': 'API', 'message': 'Removed public endpoint'}],
    changelog_entries=[],
    wiki_pages=['Getting Started'],
    analysis_summary={
        'avg_quality_score': 92.5,
        'total_vulnerabilities': 1,
        'total_performance_issues': 0
    }
)
```

---

### 4.2. `load_workflow_data()`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | – | – |

| Return Value | Type | Description |
|--------------|------|-------------|
| `dict` | Dictionary containing: |
| `changed_files` | `List[str]` | Paths of files changed in the commit. |
| `breaking_changes` | `List[Dict]` | Each dict contains `symbol` and `message`. |
| `changelog_entries` | `List[Dict]` | (Not used in this script, placeholder for future use). |
| `wiki_pages` | `List[str]` | Names of wiki pages that were updated. |
| `analysis_summary` | `Optional[Dict]` | Summary of code‑analysis results (average quality, vulnerabilities, performance issues). |

**How it works**

1. Reads `changed_files.txt` → list of changed file paths.  
2. Detects breaking changes via `breaking_changes.txt` or `doc_output.md`.  
3. Parses `wiki_summary.md` for updated wiki pages.  
4. Loads `analysis_results.json` and computes a summary.  

---

### 4.3. `main()`

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | – | – |

| Return Value | Type | Description |
|--------------|------|-------------|
| `None` | – | Executes the notification workflow: loads data, prints a summary, and dispatches notifications to any configured channel. |

**Typical usage**

```bash
# In a GitHub Actions job
- name: Run Notification Service
  run: python .github/scripts/send-notifications.py
```

---

## 5. Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
