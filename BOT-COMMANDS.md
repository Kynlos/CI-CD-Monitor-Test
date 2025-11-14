# PR Bot Commands

The PR bot has two modes: **Q&A** and **Agentic Actions**.

## Q&A Mode (Ask Questions)

**Trigger:** Any comment with a question mark or question words

**Examples:**
- "What does the Logger class do?"
- "Explain the breaking change in auth.ts"
- "How do I use formatString?"
- "Why was this function removed?"

**Response:** Bot analyzes the PR code and answers your question

---

## Agentic Mode (Make Code Changes)

**Trigger:** Comments starting with `[auto]` prefix

**Authorization:** Only PR author and assignees

### How It Works

**Clear commands** - Bot executes immediately:
```
[auto] add JSDoc comments to all functions in utils.ts
[auto] add error handling to the login function
[auto] fix the type error in database.ts
[auto] rename formatString to format
```

**Ambiguous requests** - Bot asks for confirmation first:
```
You: [auto] this needs better comments
Bot: 🤔 Do you want me to add comments to all functions? Reply "yes" to proceed.
You: yes
Bot: ✅ Changes applied! [commit abc123]
```

### Example Commands

**Add documentation:**
```
[auto] add JSDoc comments to all exported functions in utils.ts
```

**Fix issues:**
```
[auto] fix the type errors in auth.ts
[auto] add null checks to formatString
```

**Refactor:**
```
[auto] rename the Logger class to AppLogger
[auto] extract the validation logic into a separate function
```

**Add features:**
```
[auto] add a debug parameter to the Logger constructor
[auto] add error handling to all async functions
```

**Add tests:**
```
[auto] create unit tests for the formatString function
[auto] add test cases for edge cases in parseJSON
```

### What Gets Committed

When the bot makes changes:
1. ✅ Modifies the requested files
2. ✅ Commits with message: `bot: <your request>`
3. ✅ Pushes to your PR branch
4. ✅ Posts comment with:
   - Files modified
   - Commit link
   - Summary of changes

### Security

- 🔒 Only PR author and assignees can trigger
- 🔒 Bot can only modify files already in the PR
- 🔒 All changes are committed (full git history)
- 🔒 You can revert any bot commit

### Rate Limits

- Max 5 file edits per command
- 2 minute timeout per action
- If bot fails, it posts an error message

### Tips

**Be specific:**
- ✅ "[auto] add comments to utils.ts"
- ❌ "[auto] improve the code" (too vague)

**One task at a time:**
- ✅ "[auto] add error handling to login"
- ❌ "[auto] fix everything and add tests and improve docs" (too much)

**Reference specific files:**
- ✅ "[auto] fix auth.ts"
- ❌ "[auto] fix the auth code" (which file?)

### Debugging

If bot doesn't respond:
1. Check you used `[auto]` prefix
2. Check you're the PR author or assignee
3. Check action logs at `/actions/workflows/agentic-bot.yml`

If bot makes wrong changes:
1. Revert the commit
2. Rephrase your request more specifically
3. Try breaking it into smaller tasks
