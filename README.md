# 🚀 Intelligent CI/CD Documentation System

> **Automated documentation, breaking change detection, and team notifications powered by AI**

A comprehensive GitHub Actions-based system that automatically generates documentation, detects breaking changes, manages wiki pages, and notifies your team across multiple platforms—all powered by LLM intelligence.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)](https://github.com/features/actions)
[![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Detailed Features](#detailed-features)
- [Setup Guide](#setup-guide)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [PR Bot Commands](#pr-bot-commands)
- [Notifications](#notifications)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Cost Analysis](#cost-analysis)
- [Contributing](#contributing)

---

## 🎯 Overview

This system revolutionizes code documentation by automatically:
- **Analyzing** every code change with AI
- **Generating** comprehensive documentation
- **Detecting** breaking changes and API modifications
- **Organizing** documentation into intelligent wiki pages
- **Notifying** your team across Discord, Slack, and Pushbullet
- **Assisting** with PR reviews through AI-powered Q&A and code modifications

**No manual documentation updates. No outdated docs. Just intelligent automation.**

---

## ✨ Key Features

### 🔍 **Automated Code Analysis**
- **Breaking Change Detection** - Identifies signature changes, removed exports, and API modifications
- **Cross-File Impact Analysis** - Detects how changes in one file affect others
- **Diff-Aware Processing** - Only processes what changed, not entire codebase
- **Smart Categorization** - Automatically groups changes as breaking, added, modified, or removed

### 📚 **Intelligent Documentation**
- **AI-Generated Docs** - LLM creates comprehensive documentation from your code
- **GitHub Wiki Integration** - Automatically routes docs to appropriate wiki pages
- **Persistent Mapping** - Never forgets where documentation belongs
- **Changelog Automation** - Auto-updates CHANGELOG.md with categorized changes
- **API Documentation** - Generates and maintains API-DOCS.md

### 💬 **PR Enhancement**
- **Smart PR Comments** - Detailed analysis posted on every pull request
- **Q&A Bot** - Ask questions about PR changes, get instant answers
- **Agentic Bot** - Make code changes via comments (`[auto] add tests`)
- **Review Assistance** - Highlights breaking changes and action items

### 🔔 **Multi-Platform Notifications**
- **Discord** - Rich embeds with color-coded alerts
- **Slack** - Professional blocks with action buttons
- **Pushbullet** - Mobile/desktop push notifications
- **PR Bump System** - Alert team with keywords like "bump", "review needed", "urgent"

### 🤖 **Advanced Automation**
- **Workflow Orchestration** - Coordinates multiple workflows seamlessly
- **Version Control** - All changes tracked in git history
- **Security** - Role-based permissions, audit trails
- **Extensibility** - Easy to add new platforms or features

---

## 🚀 Quick Start

### Prerequisites
- GitHub repository
- [Groq API key](https://console.groq.com) (free tier available)
- Optional: Discord/Slack webhooks, Pushbullet token

### 5-Minute Setup

```bash
# 1. Clone this repo
git clone https://github.com/Kynlos/CI-CD-Monitor-Test.git
cd CI-CD-Monitor-Test

# 2. Copy workflows to your repo
cp -r .github <your-repo>/

# 3. Add required secret
# Go to: https://github.com/<your-username>/<your-repo>/settings/secrets/actions
# Add: GROQ_API_KEY = <your-groq-api-key>

# 4. Push a code change and watch the magic! ✨
git add .
git commit -m "feat: Enable intelligent documentation"
git push
```

That's it! Your first documentation will be auto-generated on the next commit.

---

## 🎨 Detailed Features

### 1. 🔍 Breaking Change Detection

Automatically detects when your API changes in breaking ways:

**Detected Changes:**
- Function signature modifications
- Removed exported functions/classes
- Parameter changes (type, count, order)
- Return type changes

**Actions Taken:**
- Labels PR with `breaking-change`
- Highlights in PR comment (red color)
- Adds to CHANGELOG under "Breaking Changes"
- Sends urgent notifications (@here ping)

**Example:**
```typescript
// Before
export function validateToken(token: string): Promise<User>

// After
export function validateToken(token: string, options?: ValidateOptions): Promise<User>
```

**Detection Result:**
```
⚠️ BREAKING CHANGE DETECTED
- validateToken: Modified signature
  Before: validateToken(token: string): Promise<User>
  After:  validateToken(token: string, options?: ValidateOptions): Promise<User>
```

### 2. 📝 Changelog Generation

Maintains a comprehensive CHANGELOG.md with:

**Categories:**
- ⚠️ **Breaking Changes** - API modifications
- ✨ **Added** - New functions, classes, exports
- 🔄 **Changed** - Modified implementations
- 🗑️ **Removed** - Deleted exports

**Format:**
```markdown
## [2025-11-15]

### auth.ts

⚠️ BREAKING CHANGES
- Modified signature of validateToken

✨ Added
- `refreshSession` (function)
- `SessionManager` (class)

🔄 Changed
- `login` signature updated
```

### 3. 📚 Intelligent Wiki Routing

LLM-powered system that intelligently organizes documentation:

**How It Works:**
1. **Analyzes** file path and content
2. **Reads** existing wiki pages
3. **Decides** optimal wiki page (e.g., "Authentication-API")
4. **Remembers** decision in `.github/wiki-mapping.json`
5. **Stays consistent** - same files always go to same pages

**Examples:**
```
auth.ts           → Authentication-API
database.ts       → Database-Layer
api/users.ts      → API-Users
utils/format.ts   → Utilities
test/auth.test.ts → Testing-Guide
```

**Benefits:**
- No manual wiki organization needed
- Consistent placement across commits
- Smart domain grouping
- Full audit trail in git

### 4. 🔗 Cross-File Impact Analysis

Detects dependencies between files:

```
You modified `validateToken` in auth.ts which is called by:
- api/users.ts (line 45)
- middleware/auth.ts (line 23)
- services/session.ts (line 67)

⚠️ Consider testing these dependent files
```

### 5. 💬 Smart PR Comments

Every PR gets a comprehensive analysis:

```markdown
## 🤖 Auto-Generated Documentation & Analysis

### ⚠️ BREAKING CHANGES DETECTED
This PR contains breaking changes that may affect users:
- **validateToken**: Modified signature
  ```diff
  - validateToken(token: string): Promise<User>
  + validateToken(token: string, options?: ValidateOptions): Promise<User>
  ```

### 📄 Files Changed (3)
- `auth.ts`
- `database.ts`
- `utils/format.ts`

### 📋 Changelog Entries
**auth.ts**
⚠️ BREAKING CHANGES
- Modified signature of validateToken

✨ Added
- `refreshSession` (function)

### 🔗 Cross-File Impact Analysis
**auth.ts**
- References `DatabaseConnection` from `database.ts`
- Used by `middleware/auth.ts`, `api/users.ts`

### 📚 Documentation Generated
- [Authentication-API](https://github.com/your-repo/wiki/Authentication-API)
- [Database-Layer](https://github.com/your-repo/wiki/Database-Layer)

### ✅ Recommended Actions
- [ ] Update major version number
- [ ] Create migration guide
- [ ] Notify users of breaking changes
- [ ] Test affected files for regressions

---
*Documentation automatically generated. Ask questions about these changes below!*
```

### 6. 🤖 PR Bot Features

#### **Q&A Mode**

Ask questions about code changes:

```
You: What does the new validateToken function do?

Bot: The validateToken function validates JWT tokens and returns 
authenticated user objects. The new version accepts an optional 
ValidateOptions parameter that allows you to:
- Skip expiration checks
- Specify custom validation rules
- Enable debug mode

It returns a Promise<User> or throws an error if validation fails.
```

**Triggered by:** Any question with `?` or question words

#### **Agentic Mode**

Make code changes via comments:

```
You: [auto] add JSDoc comments to all functions in auth.ts

Bot: ✅ Changes applied! [commit abc123]

Modified files:
- auth.ts (added 5 JSDoc comments)

Summary:
- Added documentation for validateToken
- Added documentation for refreshSession
- Added documentation for login
- Added documentation for logout
- Added documentation for getSession
```

**Keywords:** `[auto]` prefix
**Authorization:** PR author or assignees only

**Examples:**
- `[auto] fix type errors in database.ts`
- `[auto] add tests for validateToken`
- `[auto] rename formatString to format`

### 7. 🔔 Multi-Platform Notifications

#### **Discord**

Rich embeds with:
- Color coding (🟢 normal, 🟠 changes, 🔴 breaking)
- Clickable links to PR/workflow
- File lists and wiki updates
- @here ping for urgent changes

**Example:**
```
🐛 fix: Handle edge case in token validation
CI-CD-Monitor-Test • a3f7d2c

⚠️ Breaking Changes (if any)
- validateToken: Modified signature

📄 Files Changed (2)
• auth.ts
• auth.test.ts

📚 Wiki Pages Updated (1)
• Authentication-API

🔗 Links
[View Workflow] [View Wiki]

by username
```

#### **Slack**

Professional blocks with:
- Header with commit message
- Collapsible sections
- Action buttons
- File and wiki lists

#### **Pushbullet**

Mobile/desktop notifications with:
- Commit title
- Repo and author
- Quick file summary
- Clickable workflow link

### 8. 🚨 PR Bump System

Get team attention on PRs:

**Keywords:**
- `bump` - General attention
- `review needed` / `PTAL` - Request review
- `urgent` / `blocked` / `priority` - High priority (pings @here)
- `help needed` - Request assistance

**Example:**
```
You: bump - this is blocked and needs urgent review!

[Discord notification sent]
🔔 PR Review Requested - #123
Add authentication system

💬 Comment
"bump - this is blocked and needs urgent review!"

⚠️ Urgency
This PR is marked as urgent/blocked/priority

@here
```

---

## 🛠️ Setup Guide

### Step 1: Add GitHub Secrets

Navigate to: `https://github.com/<owner>/<repo>/settings/secrets/actions`

**Required:**
```
GROQ_API_KEY = gsk_xxxxxxxxxxxxxxxxxxxxx
```
Get free key at: https://console.groq.com

**Optional (Notifications):**
```
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/...
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/...
PUSHBULLET = o.xxxxxxxxxxxxxxxxxxxxx
```

### Step 2: Copy Workflows

```bash
# Copy all workflow files
cp -r .github/workflows <your-repo>/.github/
cp -r .github/scripts <your-repo>/.github/
cp .github/wiki-mapping.json <your-repo>/.github/

# Set executable permissions
chmod +x .github/scripts/*.py
```

### Step 3: Initialize Wiki (Optional)

If using wiki features:
1. Go to `https://github.com/<owner>/<repo>/wiki`
2. Create first page (any content)
3. Wiki is now initialized for auto-updates

### Step 4: Commit and Test

```bash
git add .github/
git commit -m "feat: Add intelligent documentation system"
git push
```

Watch your first workflow run at: `https://github.com/<owner>/<repo>/actions`

---

## ⚙️ Configuration

### Change LLM Model

Edit `.github/scripts/generate-docs.py`:

```python
MODEL = 'llama-3.3-70b-versatile'  # Default (fast, cheap)
# MODEL = 'llama-3.1-70b-versatile'  # Alternative
# MODEL = 'mixtral-8x7b-32768'       # Mixtral option
```

### Customize Documentation Prompt

Edit prompt in `.github/scripts/generate-docs.py`:

```python
prompt = f"""Generate comprehensive API documentation.

Include:
1. Overview - What this module does
2. Exports - All exported functions, classes, interfaces
3. Usage Examples - Practical examples for each export  # <-- Add
4. Parameters - Describe each parameter
5. Return Values - What each function returns
6. Error Handling - What errors can be thrown  # <-- Add
"""
```

### Add/Remove File Types

Edit `.github/workflows/auto-docs.yml`:

```yaml
on:
  push:
    paths:
      - '**.ts'      # TypeScript
      - '**.tsx'     # TypeScript React
      - '**.js'      # JavaScript
      - '**.jsx'     # JavaScript React
      - '**.py'      # Python
      - '**.go'      # Add Go
      - '**.rs'      # Add Rust
      - '**.java'    # Add Java
```

### Customize Wiki Routing Logic

Edit `.github/scripts/wiki-manager.py` to add custom routing rules:

```python
def _fallback_page_name(self, file_path: str) -> str:
    """Fallback logic if LLM fails"""
    path = Path(file_path)
    
    # Add custom rules
    if 'payment' in file_path.lower():
        return 'Payment-Processing'
    elif 'email' in file_path.lower():
        return 'Email-Service'
    
    # ... existing logic
```

---

## 📖 Usage Examples

### Example 1: Add a New Feature

```bash
# Create new file
cat > payment.ts << EOF
export async function processPayment(amount: number): Promise<void> {
  // Process payment logic
}
EOF

git add payment.ts
git commit -m "feat: Add payment processing"
git push
```

**What Happens:**
1. ✅ Workflow detects `payment.ts` changed
2. ✅ Generates documentation using AI
3. ✅ Creates "Payment-Processing" wiki page
4. ✅ Updates CHANGELOG.md
5. ✅ Sends notifications to Discord/Slack/Pushbullet
6. ✅ Commits all changes automatically

### Example 2: Breaking Change

```bash
# Modify function signature
# Before: validateToken(token: string): Promise<User>
# After:  validateToken(token: string, skipExpiry: boolean): Promise<User>

git add auth.ts
git commit -m "feat: Add skip expiry option to validateToken"
git push
```

**What Happens:**
1. 🚨 Detects breaking change (signature modified)
2. 🏷️ Labels commit as breaking
3. ⚠️ Updates CHANGELOG under "Breaking Changes"
4. 📢 Sends urgent notification (@here ping on Discord)
5. 📝 Suggests version bump in PR comment

### Example 3: PR Review Workflow

```bash
# Create PR
git checkout -b feature/new-auth
# ... make changes ...
git push origin feature/new-auth
# Create PR on GitHub
```

**On PR creation:**
1. 🤖 Bot posts comprehensive analysis comment
2. 📊 Shows breaking changes, impacts, files changed
3. ✅ Lists recommended actions

**During review:**
```
Reviewer: What does the new validateToken function do?
Bot: [Detailed explanation based on code analysis]

Reviewer: bump - need urgent review for security fix
[Notification sent to team via Discord/Slack]

Reviewer: [auto] add tests for validateToken
Bot: ✅ Changes applied! [commit link]
```

### Example 4: Team Collaboration

**Developer A** (creates PR):
```bash
git push origin feature/api-redesign
```

**Developer B** (requests attention):
```
Comment: bump - this redesigns our core API, needs thorough review
```

**Team receives:**
- 🔔 Discord notification with PR link
- 📱 Pushbullet notification on phones
- 💬 Slack message in team channel

**Developer C** (reviews):
```
Comment: [auto] add JSDoc to all new functions
```

**Bot:**
- ✅ Adds documentation
- 📝 Commits changes
- 💬 Posts summary

---

## 🤖 PR Bot Commands

### Q&A Mode

**Triggers:** Questions with `?` or question words

**Examples:**
```
What does validateToken do?
How do I use the new SessionManager?
Why was formatString removed?
Explain the breaking change in auth.ts
```

**Bot analyzes PR code and answers based on:**
- Changed files
- Diffs
- Context from commit messages
- Generated documentation

### Agentic Mode

**Trigger:** `[auto]` prefix

**Authorization:** PR author or assignees only

**Commands:**

**Add Documentation:**
```
[auto] add JSDoc comments to all functions in auth.ts
[auto] add TypeScript types to database.ts
```

**Fix Issues:**
```
[auto] fix type errors in utils.ts
[auto] add null checks to formatString
[auto] handle edge case in validateToken
```

**Refactoring:**
```
[auto] rename Logger to AppLogger
[auto] extract validation logic into separate function
[auto] split auth.ts into smaller modules
```

**Add Tests:**
```
[auto] create unit tests for validateToken
[auto] add edge case tests for formatString
[auto] add integration tests for payment flow
```

**Security:**
- 🔒 Only PR author/assignees can trigger
- 🔒 Bot can only modify files in PR
- 🔒 All changes committed with full history
- 🔒 Changes can be reverted anytime

**Limits:**
- Max 5 file edits per command
- 2 minute timeout per action
- Requires clear, specific instructions

---

## 🔔 Notifications

### Discord Setup

1. **Create webhook:**
   - Server Settings → Integrations → Webhooks
   - Create Webhook → Copy URL

2. **Add to GitHub:**
   - Repo Settings → Secrets → Actions
   - Add: `DISCORD_WEBHOOK_URL`

3. **Test:**
   - Push any commit
   - Check Discord channel

**Features:**
- 🎨 Color-coded embeds
- 🔗 Clickable links
- 📢 @here ping for urgent
- 📊 Rich formatting

### Slack Setup

1. **Create webhook:**
   - Slack → Apps → Incoming Webhooks
   - Add to Workspace → Copy URL

2. **Add to GitHub:**
   - Repo Settings → Secrets → Actions
   - Add: `SLACK_WEBHOOK_URL`

**Features:**
- 📦 Professional blocks
- 🔘 Action buttons
- 📱 Mobile-friendly
- 🎯 Channel targeting

### Pushbullet Setup

1. **Get token:**
   - https://www.pushbullet.com/#settings
   - Create Access Token → Copy

2. **Add to GitHub:**
   - Repo Settings → Secrets → Actions
   - Add: `PUSHBULLET`

**Features:**
- 📱 Mobile push notifications
- 💻 Desktop alerts
- 🔗 Clickable links
- ⚡ Instant delivery

### PR Bump Keywords

**Normal Priority:**
- `bump`
- `ping`
- `review needed`
- `please review`
- `PTAL` (Please Take A Look)
- `R4R` (Ready for Review)

**Urgent (with @here ping):**
- `urgent`
- `blocked`
- `priority`
- `critical`
- `help needed`

---

## 🏗️ Architecture

### Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Code Push/PR Created                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   auto-docs.yml (Main Workflow)             │
├─────────────────────────────────────────────────────────────┤
│ 1. Detect changed files (.ts, .js, .py)                    │
│ 2. Generate documentation (generate-docs.py)                │
│ 3. Detect breaking changes                                  │
│ 4. Route to wiki pages (wiki-manager.py)                   │
│ 5. Update CHANGELOG.md                                      │
│ 6. Send notifications (send-notifications.py)               │
│ 7. Post PR comment (if PR)                                  │
│ 8. Commit changes back to repo                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┬──────────────┐
       ▼               ▼               ▼              ▼
   Discord         Slack          Pushbullet      GitHub Wiki
```

### File Structure

```
.github/
├── workflows/
│   ├── auto-docs.yml       # Main documentation workflow
│   ├── pr-bot.yml          # Q&A bot for PRs
│   ├── agentic-bot.yml     # Code modification bot
│   └── pr-bump.yml         # PR bump notifications
├── scripts/
│   ├── generate-docs.py    # AI documentation generator
│   ├── wiki-manager.py     # Intelligent wiki routing
│   ├── send-notifications.py # Multi-platform notifications
│   ├── answer-question.py  # Q&A bot logic
│   └── agentic-bot.py      # Code modification logic
└── wiki-mapping.json       # Persistent wiki page mapping

docs/                       # Generated documentation
API-DOCS.md                 # Consolidated API docs
CHANGELOG.md                # Auto-generated changelog
wiki_summary.md             # Wiki organization summary
```

### Data Flow

```
Code Change
    ↓
Git Diff Detection
    ↓
Groq API (LLM Analysis)
    ↓
Documentation Generation
    ↓
Breaking Change Detection
    ↓
Wiki Page Routing (LLM Decision)
    ↓
Persistent Mapping Storage
    ↓
Multi-Platform Notifications
    ↓
GitHub Commit (auto-update)
```

---

## 🔧 Troubleshooting

### "GROQ_API_KEY not set"

**Problem:** Workflow fails with API key error

**Solutions:**
1. Verify secret exists: `Settings → Secrets → Actions`
2. Check secret name is exactly `GROQ_API_KEY`
3. Regenerate key at https://console.groq.com
4. Re-add secret to GitHub

### "No documentation generated"

**Problem:** Workflow runs but creates no docs

**Possible Causes:**
1. No code files changed (only README, configs, etc.)
2. Changed files don't match trigger patterns
3. Files in `.gitignore` or excluded paths

**Solutions:**
```bash
# Check which files changed
git diff --name-only HEAD~1 HEAD

# Verify workflow triggers
# Edit .github/workflows/auto-docs.yml paths section
```

### "Wiki not initialized"

**Problem:** Wiki updates fail

**Solution:**
```bash
# Initialize wiki manually:
# 1. Go to: https://github.com/<owner>/<repo>/wiki
# 2. Create any page with any content
# 3. Wiki is now active for automation
```

### "API rate limit exceeded"

**Problem:** Too many API calls to Groq

**Solutions:**
1. Reduce frequency by committing less often
2. Batch changes before pushing
3. Use different model (some have higher limits)
4. Upgrade Groq plan if needed

### "Bot doesn't respond to [auto] commands"

**Problem:** Agentic bot doesn't make changes

**Checks:**
1. Are you PR author or assignee?
2. Did you use exact `[auto]` prefix?
3. Is command specific enough?
4. Check workflow logs for errors

**Test:**
```
[auto] add comment "test" to auth.ts
```

### "Notifications not received"

**Problem:** No Discord/Slack/Pushbullet notifications

**Checks:**
1. Verify secret names match exactly
2. Test webhook URL manually:
   ```bash
   curl -X POST <webhook-url> \
     -H "Content-Type: application/json" \
     -d '{"content":"Test"}'
   ```
3. Check workflow logs for API errors
4. Verify permissions on webhook

---

## 💰 Cost Analysis

### Groq API Costs

**Model:** `llama-3.3-70b-versatile`

**Pricing:** $0.075 per 1M tokens

**Typical Usage:**
- Small file (< 200 lines): ~500 tokens = $0.0000375
- Medium file (200-500 lines): ~2,000 tokens = $0.00015
- Large file (> 500 lines): ~5,000 tokens = $0.000375

**Monthly Estimate (100 commits/month):**
- Small project: $0.004/month (~$0.05/year)
- Medium project: $0.015/month (~$0.18/year)
- Large project: $0.038/month (~$0.46/year)

**Free tier:** 30 requests/minute, 14,400/day

### GitHub Actions Minutes

**Usage per workflow run:** ~2-5 minutes

**Free tier:** 2,000 minutes/month (public repos: unlimited)

**Cost if exceeded:** $0.008/minute

**Monthly estimate:** Negligible (well within free tier)

### Total Monthly Cost

**Small team (< 50 commits/month):**
- Groq: < $0.01
- GitHub: $0 (free tier)
- **Total: ~$0.01/month**

**Medium team (100-200 commits/month):**
- Groq: ~$0.02
- GitHub: $0 (free tier)
- **Total: ~$0.02/month**

**Large team (500+ commits/month):**
- Groq: ~$0.10
- GitHub: $0 (free tier)
- **Total: ~$0.10/month**

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Development Setup

```bash
# Clone repo
git clone https://github.com/Kynlos/CI-CD-Monitor-Test.git
cd CI-CD-Monitor-Test

# Install dependencies
pip install requests

# Set up test environment
export GROQ_API_KEY="your-key"
export DISCORD_WEBHOOK_URL="your-webhook"
```

### Testing Locally

```bash
# Test documentation generation
echo "test.ts" > changed_files.txt
python .github/scripts/generate-docs.py

# Test wiki routing
python .github/scripts/wiki-manager.py

# Test notifications
python .github/scripts/send-notifications.py
```

### Contribution Guidelines

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing`)
3. **Test** thoroughly
4. **Commit** with conventional commits (`feat:`, `fix:`, `docs:`)
5. **Push** to your fork
6. **Open** Pull Request

### Code Standards

- Python: Follow PEP 8
- Comments: Explain "why", not "what"
- Tests: Add for new features
- Docs: Update README for changes

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **Groq** - Lightning-fast LLM inference
- **GitHub Actions** - Automation platform
- **Community** - Feature requests and feedback

---

## 📞 Support

- **Issues:** https://github.com/Kynlos/CI-CD-Monitor-Test/issues
- **Discussions:** https://github.com/Kynlos/CI-CD-Monitor-Test/discussions
- **Email:** support@example.com

---

## 🗺️ Roadmap

### Coming Soon
- [ ] Multi-language support (Go, Rust, Java, C++)
- [ ] Visual dependency graphs
- [ ] Auto-generated migration guides
- [ ] Semantic version automation
- [ ] Code quality scoring
- [ ] Security vulnerability scanning
- [ ] Performance regression detection
- [ ] Interactive code examples
- [ ] Teams/MS Teams notifications
- [ ] Email digest reports

### In Progress
- [x] Discord notifications
- [x] Slack notifications
- [x] Pushbullet notifications
- [x] PR bump system
- [x] Intelligent wiki routing
- [x] Breaking change detection
- [x] Agentic bot
- [x] Q&A bot

---

<div align="center">

**Made with ❤️ by developers, for developers**

[⭐ Star this repo](https://github.com/Kynlos/CI-CD-Monitor-Test) • [🐛 Report Bug](https://github.com/Kynlos/CI-CD-Monitor-Test/issues) • [💡 Request Feature](https://github.com/Kynlos/CI-CD-Monitor-Test/issues)

</div>
