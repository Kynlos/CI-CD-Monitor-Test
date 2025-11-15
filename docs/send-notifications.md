# send-notifications.py

*Auto-generated from `.github/scripts/send-notifications.py`*

# `send-notifications.py` – API Documentation

> **Location**: `.github/scripts/send-notifications.py`  
> **Purpose**: A lightweight CI/CD helper that reads workflow artifacts and posts a nicely‑formatted notification to Discord, Slack, and Pushbullet.  
> **Language**: Python 3.8+

---

## 1. Overview

The script is designed to run as part of a GitHub Actions workflow.  
It:

1. **Collects** data from artifacts produced earlier in the job  
   * changed files (`changed_files.txt`)  
   * breaking‑change flag (`breaking_changes.txt`)  
   * wiki summary