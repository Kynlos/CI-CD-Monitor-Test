# PR Bump Feature Guide

Get your team's attention on pull requests by using bump keywords in comments!

## How It Works

When you comment on a PR with certain keywords, the bot automatically sends a notification to configured Discord/Slack channels.

## Bump Keywords

Any of these will trigger a notification:

- `bump` - Simple attention getter
- `ping` - Quick ping
- `attention` - Needs attention
- `review needed` - Explicit review request
- `needs review` - Same as above
- `please review` - Polite request
- `ready for review` - Mark PR as ready
- `R4R` - Shorthand for Ready for Review
- `PTAL` - Please Take A Look
- `lgtm?` - Looking for approval
- `anyone available` - Seeking reviewer
- `help needed` - Need assistance
- `blocked` - PR is blocked (⚠️ urgent)
- `urgent` - High priority (⚠️ urgent)
- `priority` - Important PR (⚠️ urgent)

## Urgency Detection

Keywords marked as urgent (`urgent`, `blocked`, `priority`, `critical`) will:
- Display in RED on Discord (instead of orange)
- Ping `@here` to notify everyone
- Show as primary button on Slack
- Include urgency warning in notification

## Examples

### Simple Bump
```
bump - still needs review!
```
**Result:** Orange notification sent to Discord/Slack

### Urgent Request
```
This is blocked - need review ASAP!
```
**Result:** RED notification with @here ping

### Polite Request
```
Ready for review - PTAL when you get a chance
```
**Result:** Orange notification with your message

### Help Needed
```
Help needed - not sure if this approach is right
```
**Result:** Notification highlighting that help is needed

## What Gets Sent

The notification includes:
- **PR Number & Title** - #123: Add new feature
- **Your Comment** - The full text of your comment
- **Your GitHub Avatar** - Visual identification
- **Repository Name** - Which repo the PR is in
- **Direct Link** - Clickable link to the PR
- **Urgency Warning** - If urgent keywords detected

## Discord Example

```
🔔 PR Review Requested - #123
Add authentication system

💬 Comment
"bump - this is blocked and needs urgent review!"

⚠️ Urgency
This PR is marked as urgent/blocked/priority

📂 Repository: Kynlos/CI-CD-Monitor-Test
🔗 Link: [View PR]

@here (if urgent)
```

## Slack Example

```
🔔 PR Review Requested - #123
Add authentication system

"bump - this is blocked and needs urgent review!"

⚠️ This PR is marked as urgent/blocked/priority

Repository: Kynlos/CI-CD-Monitor-Test | Requested by: username

[View PR] (primary button if urgent)
```

## Best Practices

### ✅ DO
- Use bump when genuinely need attention
- Add context to your bump message
- Use urgent keywords sparingly for truly critical PRs
- Combine keywords: "Ready for review - PTAL"

### ❌ DON'T
- Spam bumps multiple times per day
- Mark everything as urgent
- Bump immediately after opening PR
- Use offensive language in comments

## Setup Required

To enable this feature, repository admins must add webhook URLs:

1. Go to repo Settings → Secrets and variables → Actions
2. Add `DISCORD_WEBHOOK_URL` and/or `SLACK_WEBHOOK_URL`
3. Save the secrets

Once configured, all PR comments are automatically scanned for bump keywords!

## Testing

1. Open any PR
2. Comment: `bump - testing notifications`
3. Check your Discord/Slack channel
4. You should see a notification within seconds!
