# Advanced Auto-Documentation CI/CD

GitHub Actions workflow with intelligent code analysis and documentation generation.

## Features

### 🔍 1. Breaking Change Detection
- Automatically detects when function signatures change
- Identifies removed exports
- Labels PRs as `breaking-change` and `major`
- Suggests semver version bumps

### 📝 2. Changelog Generation
- Auto-updates CHANGELOG.md on every commit
- Categorizes: Breaking Changes, Added, Changed, Removed
- Links to commits and files
- Maintains chronological history

### 🎯 3. Diff-Aware Documentation
- Only documents what actually changed
- Shows before/after comparisons
- Highlights modifications, not just regenerating everything
- Includes git diffs in context

### 🔗 4. Cross-File Impact Analysis
- Detects when changes affect other files
- Shows dependency relationships
- Warns about potential cascading effects
- Example: "You modified function X which is called by Y, Z"

### 💬 5. Smart PR Comments
- Comprehensive analysis posted on every PR
- Breaking changes highlighted prominently
- Impact analysis included
- Action items for reviewers
- Documentation links

### 📚 6. Intelligent Wiki Routing (NEW!)
- **Automatically routes docs to GitHub Wiki pages**
- **LLM-powered smart categorization** - Decides best wiki page for each file
- **Persistent mapping** - Never forgets where things go (`.github/wiki-mapping.json`)
- **Reads existing pages** - Makes intelligent decisions based on current wiki structure
- **Consistency guaranteed** - Same files always go to same pages
- **Domain grouping** - Related files organized together logically
- **Auto-verification** - Checks mapping consistency on every run

## Setup for https://github.com/Kynlos/CI-CD-Monitor-Test

### 1. Add GitHub Secrets

1. Go to https://github.com/Kynlos/CI-CD-Monitor-Test/settings/secrets/actions
2. Click "New repository secret"
3. Add the following secrets:
   - **Required:**
     - `GROQ_API_KEY` - Your Groq API key
   - **Optional (for notifications):**
     - `DISCORD_WEBHOOK_URL` - Discord webhook URL for notifications
     - `SLACK_WEBHOOK_URL` - Slack webhook URL for notifications

### 2. Copy Workflow Files

Copy these files to your repo:

```bash
mkdir -p .github/workflows
mkdir -p .github/scripts

cp .github/workflows/auto-docs.yml <your-repo>/.github/workflows/
cp .github/scripts/generate-docs.py <your-repo>/.github/scripts/
chmod +x <your-repo>/.github/scripts/generate-docs.py
```

### 3. Commit and Push

```bash
git add .github/
git commit -m "feat: Add Symbol Capsules auto-documentation CI/CD"
git push
```

## How It Works

### On Every Commit to Main:

1. **Detects changed files** - Only processes .ts/.js/.py files that changed
2. **Reads file contents** - Gets the full code
3. **Calls Groq API** - Generates documentation
4. **Routes to Wiki** - Smart wiki-manager.py decides which wiki page for each file
5. **Updates Wiki** - Pushes to GitHub Wiki automatically
6. **Commits docs** - Updates `API-DOCS.md`, `CHANGELOG.md`, and wiki mapping

### On Every Pull Request:

1. **Same process**
2. **Posts PR comment** with:
   - Generated documentation
   - List of changes
   - Token usage statistics

## Example Output

### PR Comment:

```markdown
## 🤖 Auto-Generated Documentation

**Changes detected in 2 file(s)**

### auth.ts

**Added Functions:**
- `validateToken(token: string): Promise<User>` - Validates JWT token and returns user object
- `refreshSession(sessionId: string): Promise<Session>` - Refreshes expired session

**Modified Functions:**
- `login(username, password, options?)` - Now accepts optional LoginOptions parameter

### database.ts

**Added Classes:**
- `DatabaseConnection` - Manages PostgreSQL connection pool with automatic retry

---

**Token Usage:**
- Total tokens: 3,240
- Cost: $0.000243

*Documentation automatically generated from code changes.*
```

### Committed File (API-DOCS.md):

```markdown
# API Documentation

*Last updated: 2025-11-14*

## auth.ts

### validateToken
Validates JWT token and returns authenticated user object.

**Signature:** `async validateToken(token: string): Promise<User>`

**Parameters:**
- `token` - JWT authentication token

**Returns:** User object if valid

...
```

## Benefits

### Automated Documentation

- **Never outdated** - Regenerated on every commit
- **Consistent format** - LLM ensures uniform style
- **PR reviews** - Reviewers see what APIs changed
- **Breaking changes** - Automatically highlighted



## Customization

### Change the Model

Edit `.github/scripts/generate-docs.py`:

```python
MODEL = 'llama-3.3-70b-versatile'  # Default (fast, cheap)
# MODEL = 'openai/gpt-oss-120b'    # More capable
# MODEL = 'mixtral-8x7b-32768'     # Alternative
```

### Customize Documentation Prompt

Edit the prompt in `generate_documentation()`:

```python
prompt = f"""Generate API documentation...

Include:
1. Overview
2. Function descriptions
3. Usage examples  # <-- Add this
4. Type definitions  # <-- Add this
```

### Change Trigger Files

Edit `.github/workflows/auto-docs.yml`:

```yaml
paths:
  - '**.ts'      # TypeScript
  - '**.py'      # Python
  - '**.go'      # Add Go
  - '**.rs'      # Add Rust
```

## Testing Locally

```bash
# Simulate changed files
echo "src/auth.ts" > changed_files.txt
echo "src/database.ts" >> changed_files.txt

# Run generator
export GROQ_API_KEY="your-key"
python .github/scripts/generate-docs.py

# Check output
cat doc_output.md
cat API-DOCS.md
```

## Troubleshooting

### "GROQ_API_KEY not set"

**Fix:** Add the secret in GitHub repo settings:
```
Settings → Secrets and variables → Actions → New repository secret
```

### "No documentation generated"

**Cause:** No code files changed

**Check:** Look at workflow logs to see which files were detected

### "API rate limit exceeded"

**Fix:** Add rate limiting or use a different model

## Next Steps

1. **Add to your repo** - Follow setup steps above
2. **Make a test commit** - Watch the action run
3. **Review generated docs** - Check API-DOCS.md
4. **Submit a PR** - See the PR comment with docs
5. **Customize prompts** - Tune to your needs

## Files

- `.github/workflows/auto-docs.yml` - GitHub Actions workflow
- `.github/scripts/generate-docs.py` - Documentation generator
- `.github/scripts/wiki-manager.py` - Intelligent wiki routing system
- `.github/wiki-mapping.json` - Persistent file-to-wiki-page mapping
- `API-DOCS.md` - Auto-generated documentation (committed)
- `doc_output.md` - PR comment content (not committed)
- `wiki_summary.md` - Wiki organization summary (generated on each run)

## Cost Analysis


