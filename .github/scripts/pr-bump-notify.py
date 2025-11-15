#!/usr/bin/env python3
"""
PR Bump Notification - Alert team when someone bumps a PR
Detects keywords like 'bump', 'attention', 'review needed', etc.
"""

import os
import re
import sys
import requests
from datetime import datetime

# Webhook URLs
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK_URL')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK_URL')

# PR/Comment info
COMMENT_BODY = os.environ.get('COMMENT_BODY', '')
COMMENT_USER = os.environ.get('COMMENT_USER', 'Unknown')
PR_NUMBER = os.environ.get('PR_NUMBER', '0')
PR_TITLE = os.environ.get('PR_TITLE', 'Unknown PR')
PR_URL = os.environ.get('PR_URL', '')
REPO_NAME = os.environ.get('REPO_NAME', 'Unknown Repo')

# Bump keywords (case-insensitive)
BUMP_KEYWORDS = [
    r'\bbump\b',
    r'\bping\b',
    r'\battention\b',
    r'\breview\s+needed\b',
    r'\bneeds\s+review\b',
    r'\bplease\s+review\b',
    r'\bready\s+for\s+review\b',
    r'\bR4R\b',  # Ready for Review
    r'\bPTAL\b',  # Please Take A Look
    r'\blgtm\?\b',  # LGTM? (Looks Good To Me?)
    r'\banyone\s+available\b',
    r'\bhelp\s+needed\b',
    r'\bblocked\b',
    r'\burgent\b',
    r'\bpriority\b',
]


def is_bump_comment(comment: str) -> bool:
    """Check if comment contains bump keywords"""
    comment_lower = comment.lower()
    for pattern in BUMP_KEYWORDS:
        if re.search(pattern, comment_lower):
            return True
    return False


def truncate(text: str, limit: int) -> str:
    """Truncate text to fit within limit"""
    if len(text) <= limit:
        return text
    return text[:limit-3] + "..."


def send_discord_notification(comment: str, user: str) -> bool:
    """Send PR bump notification to Discord"""
    if not DISCORD_WEBHOOK:
        return False
    
    # Determine urgency color
    urgent_keywords = ['urgent', 'blocked', 'priority', 'critical']
    is_urgent = any(kw in comment.lower() for kw in urgent_keywords)
    color = 0xFF4444 if is_urgent else 0xFFA500  # Red if urgent, orange otherwise
    
    # Build embed
    embed = {
        "title": f"🔔 PR Review Requested - #{PR_NUMBER}",
        "description": f"**{PR_TITLE}**",
        "color": color,
        "timestamp": datetime.utcnow().isoformat(),
        "author": {
            "name": f"{user}",
            "icon_url": f"https://github.com/{user}.png"
        },
        "fields": [
            {
                "name": "💬 Comment",
                "value": truncate(f"_{comment}_", 1024),
                "inline": False
            },
            {
                "name": "📂 Repository",
                "value": REPO_NAME,
                "inline": True
            },
            {
                "name": "🔗 Link",
                "value": f"[View PR]({PR_URL})",
                "inline": True
            }
        ]
    }
    
    if is_urgent:
        embed["fields"].insert(0, {
            "name": "⚠️ Urgency",
            "value": "This PR is marked as urgent/blocked/priority",
            "inline": False
        })
    
    payload = {
        "content": "@here" if is_urgent else None,  # Ping @here for urgent PRs
        "username": "PR Review Bot",
        "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        "embeds": [embed]
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        response = requests.post(
            DISCORD_WEBHOOK,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 204:
            print(f"✓ Discord notification sent for PR #{PR_NUMBER}")
            return True
        else:
            print(f"⚠️  Discord notification failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending Discord notification: {e}")
        return False


def send_slack_notification(comment: str, user: str) -> bool:
    """Send PR bump notification to Slack"""
    if not SLACK_WEBHOOK:
        return False
    
    # Determine urgency
    urgent_keywords = ['urgent', 'blocked', 'priority', 'critical']
    is_urgent = any(kw in comment.lower() for kw in urgent_keywords)
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🔔 PR Review Requested - #{PR_NUMBER}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{PR_TITLE}*\n\n_{comment}_"
            },
            "accessory": {
                "type": "image",
                "image_url": f"https://github.com/{user}.png",
                "alt_text": user
            }
        }
    ]
    
    if is_urgent:
        blocks.insert(1, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "⚠️ *This PR is marked as urgent/blocked/priority*"
            }
        })
    
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"*Repository:* {REPO_NAME} | *Requested by:* {user}"
            }
        ]
    })
    
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "View PR"},
                "url": PR_URL,
                "style": "primary" if is_urgent else None
            }
        ]
    })
    
    payload = {"blocks": blocks}
    
    if is_urgent:
        payload["text"] = f"<!here> Urgent PR Review: {PR_TITLE}"
    
    try:
        response = requests.post(
            SLACK_WEBHOOK,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✓ Slack notification sent for PR #{PR_NUMBER}")
            return True
        else:
            print(f"⚠️  Slack notification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending Slack notification: {e}")
        return False


def main():
    print("="*80)
    print("PR BUMP NOTIFICATION")
    print("="*80)
    print(f"PR: #{PR_NUMBER} - {PR_TITLE}")
    print(f"User: {COMMENT_USER}")
    print(f"Comment: {COMMENT_BODY[:100]}...")
    
    # Check if this is a bump comment
    if not is_bump_comment(COMMENT_BODY):
        print("\nℹ️  Comment does not contain bump keywords - skipping notification")
        sys.exit(0)
    
    print("\n✓ Bump keywords detected!")
    
    # Send notifications
    results = []
    
    if DISCORD_WEBHOOK:
        print("\n📢 Sending Discord notification...")
        success = send_discord_notification(COMMENT_BODY, COMMENT_USER)
        results.append(('Discord', success))
    
    if SLACK_WEBHOOK:
        print("\n📢 Sending Slack notification...")
        success = send_slack_notification(COMMENT_BODY, COMMENT_USER)
        results.append(('Slack', success))
    
    # Summary
    print("\n" + "="*80)
    print("NOTIFICATION SUMMARY")
    print("="*80)
    for platform, success in results:
        status = "✓" if success else "❌"
        print(f"{status} {platform}: {'Sent' if success else 'Failed'}")
    
    if not results:
        print("ℹ️  No webhooks configured")


if __name__ == '__main__':
    main()
