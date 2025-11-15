#!/usr/bin/env python3
"""
Notification Service - Send updates to Discord/Slack
Handles character limits and formats messages beautifully
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK_URL')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK_URL')

# Discord limits
DISCORD_CONTENT_LIMIT = 2000
DISCORD_EMBED_DESC_LIMIT = 4096
DISCORD_EMBED_FIELD_LIMIT = 1024
DISCORD_EMBED_TOTAL_LIMIT = 6000

class NotificationService:
    def __init__(self):
        self.repo = os.environ.get('GITHUB_REPOSITORY', 'Unknown Repo')
        self.commit_sha = os.environ.get('GITHUB_SHA', 'unknown')[:7]
        self.commit_message = self._clean_commit_message(os.environ.get('COMMIT_MESSAGE', 'No message'))
        self.actor = os.environ.get('GITHUB_ACTOR', 'Unknown')
        self.run_url = f"https://github.com/{self.repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
    
    def _clean_commit_message(self, message: str) -> str:
        """Remove Amp and other metadata from commit message"""
        lines = message.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip Amp-specific lines
            if line.startswith('Amp-Thread-ID:'):
                continue
            if line.startswith('Co-authored-by: Amp'):
                continue
            # Add other lines
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
        
    def truncate(self, text: str, limit: int) -> str:
        """Truncate text to fit within limit"""
        if len(text) <= limit:
            return text
        return text[:limit-3] + "..."
    
    def send_discord(self, 
                     changed_files: List[str], 
                     breaking_changes: List[Dict],
                     changelog_entries: List[Dict],
                     wiki_pages: List[str]) -> bool:
        """Send formatted notification to Discord"""
        if not DISCORD_WEBHOOK:
            print("⚠️  No Discord webhook URL configured")
            return False
        
        # Generate dynamic title based on commit message
        commit_title = self.commit_message.split('\n')[0][:100]  # First line only
        
        # Choose emoji based on content
        emoji = "📝"
        if breaking_changes:
            emoji = "⚠️"
        elif any(word in commit_title.lower() for word in ['feat', 'feature', 'add']):
            emoji = "✨"
        elif any(word in commit_title.lower() for word in ['fix', 'bug']):
            emoji = "🐛"
        elif any(word in commit_title.lower() for word in ['docs', 'documentation']):
            emoji = "📚"
        
        # Build embed
        embed = {
            "title": f"{emoji} {commit_title}",
            "description": f"**{self.repo.split('/')[-1]}** • `{self.commit_sha}`",
            "color": 0xFF6B35 if breaking_changes else 0x4CAF50,  # Orange for breaking, green otherwise
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": f"by {self.actor}"
            },
            "fields": []
        }
        
        # Breaking changes (high priority)
        if breaking_changes:
            breaking_text = "\n".join([
                f"⚠️ **{bc.get('symbol', 'Unknown')}**: {bc.get('message', '')}"
                for bc in breaking_changes[:5]
            ])
            if len(breaking_changes) > 5:
                breaking_text += f"\n... and {len(breaking_changes) - 5} more"
            
            embed["fields"].append({
                "name": "🚨 Breaking Changes Detected",
                "value": self.truncate(breaking_text, DISCORD_EMBED_FIELD_LIMIT),
                "inline": False
            })
        
        # Changed files
        if changed_files:
            files_text = "\n".join([f"• `{Path(f).name}`" for f in changed_files[:10]])
            if len(changed_files) > 10:
                files_text += f"\n... and {len(changed_files) - 10} more"
            
            embed["fields"].append({
                "name": f"📄 Files Changed ({len(changed_files)})",
                "value": self.truncate(files_text, DISCORD_EMBED_FIELD_LIMIT),
                "inline": True
            })
        
        # Wiki pages updated
        if wiki_pages:
            wiki_text = "\n".join([f"• [{page}](https://github.com/{self.repo}/wiki/{page})" 
                                   for page in wiki_pages[:8]])
            if len(wiki_pages) > 8:
                wiki_text += f"\n... and {len(wiki_pages) - 8} more"
            
            embed["fields"].append({
                "name": f"📚 Wiki Pages Updated ({len(wiki_pages)})",
                "value": self.truncate(wiki_text, DISCORD_EMBED_FIELD_LIMIT),
                "inline": True
            })
        
        # Changelog preview
        if changelog_entries:
            changelog_text = ""
            for entry in changelog_entries[:3]:
                changelog_text += f"**{entry.get('file', 'Unknown')}**\n"
                content = entry.get('content', '')[:200]
                changelog_text += f"{content}\n\n"
            
            if changelog_text:
                embed["fields"].append({
                    "name": "📋 Changelog Preview",
                    "value": self.truncate(changelog_text, DISCORD_EMBED_FIELD_LIMIT),
                    "inline": False
                })
        
        # Add action link
        embed["fields"].append({
            "name": "🔗 Links",
            "value": f"[View Workflow Run]({self.run_url}) • [View Wiki](https://github.com/{self.repo}/wiki)",
            "inline": False
        })
        
        # Build payload
        payload = {
            "username": "CI/CD Bot",
            "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            "embeds": [embed]
        }
        
        # Send to Discord
        try:
            response = requests.post(
                DISCORD_WEBHOOK,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                print("✓ Discord notification sent successfully")
                return True
            else:
                print(f"⚠️  Discord notification failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error sending Discord notification: {e}")
            return False
    
    def send_slack(self,
                   changed_files: List[str],
                   breaking_changes: List[Dict],
                   changelog_entries: List[Dict],
                   wiki_pages: List[str]) -> bool:
        """Send formatted notification to Slack"""
        if not SLACK_WEBHOOK:
            print("⚠️  No Slack webhook URL configured")
            return False
        
        # Generate dynamic title based on commit message
        commit_title = self.commit_message.split('\n')[0][:100]
        
        # Choose emoji based on content
        emoji = "📝"
        if breaking_changes:
            emoji = "⚠️"
        elif any(word in commit_title.lower() for word in ['feat', 'feature', 'add']):
            emoji = "✨"
        elif any(word in commit_title.lower() for word in ['fix', 'bug']):
            emoji = "🐛"
        elif any(word in commit_title.lower() for word in ['docs', 'documentation']):
            emoji = "📚"
        
        # Build Slack blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} {commit_title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Commit:* `{self.commit_sha}`\n*By:* {self.actor}\n*Message:* {self.commit_message}"
                }
            }
        ]
        
        # Breaking changes
        if breaking_changes:
            breaking_text = "\n".join([
                f"⚠️ *{bc.get('symbol', 'Unknown')}*: {bc.get('message', '')}"
                for bc in breaking_changes[:5]
            ])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🚨 Breaking Changes Detected*\n{breaking_text}"
                }
            })
        
        # Files and wiki
        if changed_files or wiki_pages:
            fields = []
            if changed_files:
                files_list = ", ".join([f"`{Path(f).name}`" for f in changed_files[:5]])
                if len(changed_files) > 5:
                    files_list += f" +{len(changed_files)-5} more"
                fields.append({
                    "type": "mrkdwn",
                    "text": f"*Files:* {files_list}"
                })
            
            if wiki_pages:
                wiki_list = ", ".join(wiki_pages[:5])
                if len(wiki_pages) > 5:
                    wiki_list += f" +{len(wiki_pages)-5} more"
                fields.append({
                    "type": "mrkdwn",
                    "text": f"*Wiki Pages:* {wiki_list}"
                })
            
            blocks.append({
                "type": "section",
                "fields": fields
            })
        
        # Actions
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Workflow"},
                    "url": self.run_url
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Wiki"},
                    "url": f"https://github.com/{self.repo}/wiki"
                }
            ]
        })
        
        payload = {"blocks": blocks}
        
        try:
            response = requests.post(
                SLACK_WEBHOOK,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✓ Slack notification sent successfully")
                return True
            else:
                print(f"⚠️  Slack notification failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error sending Slack notification: {e}")
            return False


def load_workflow_data():
    """Load data from workflow artifacts"""
    data = {
        'changed_files': [],
        'breaking_changes': [],
        'changelog_entries': [],
        'wiki_pages': []
    }
    
    # Load changed files
    if os.path.exists('changed_files.txt'):
        with open('changed_files.txt', 'r') as f:
            data['changed_files'] = [line.strip() for line in f if line.strip()]
    
    # Load breaking changes
    if os.path.exists('breaking_changes.txt'):
        # Indicates breaking changes were detected
        data['breaking_changes'] = [{'symbol': 'API', 'message': 'Breaking changes detected'}]
    
    # Load wiki summary
    if os.path.exists('wiki_summary.md'):
        with open('wiki_summary.md', 'r') as f:
            content = f.read()
            # Extract wiki pages from summary
            for line in content.split('\n'):
                if line.startswith('### ') and not line.startswith('### **'):
                    page_name = line.replace('### ', '').strip()
                    if page_name:
                        data['wiki_pages'].append(page_name)
    
    # Try to load more detailed breaking changes if available
    try:
        if os.path.exists('doc_output.md'):
            with open('doc_output.md', 'r') as f:
                content = f.read()
                if '⚠️ BREAKING CHANGES' in content:
                    # Parse breaking changes from doc output
                    lines = content.split('\n')
                    in_breaking = False
                    breaking_list = []
                    for line in lines:
                        if '⚠️ BREAKING CHANGES' in line:
                            in_breaking = True
                        elif in_breaking and line.startswith('- **'):
                            # Extract symbol and message
                            parts = line.replace('- **', '').split('**:', 1)
                            if len(parts) == 2:
                                breaking_list.append({
                                    'symbol': parts[0].strip(),
                                    'message': parts[1].strip()
                                })
                        elif in_breaking and line.startswith('#'):
                            break
                    
                    if breaking_list:
                        data['breaking_changes'] = breaking_list
    except:
        pass
    
    return data


def main():
    print("="*80)
    print("NOTIFICATION SERVICE")
    print("="*80)
    
    # Get commit message from git
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            os.environ['COMMIT_MESSAGE'] = result.stdout.strip()
    except:
        pass
    
    # Load workflow data
    data = load_workflow_data()
    
    print(f"Changed files: {len(data['changed_files'])}")
    print(f"Breaking changes: {len(data['breaking_changes'])}")
    print(f"Wiki pages: {len(data['wiki_pages'])}")
    
    # Initialize service
    service = NotificationService()
    
    # Send notifications
    results = []
    
    if DISCORD_WEBHOOK:
        print("\n📢 Sending Discord notification...")
        success = service.send_discord(
            data['changed_files'],
            data['breaking_changes'],
            data['changelog_entries'],
            data['wiki_pages']
        )
        results.append(('Discord', success))
    
    if SLACK_WEBHOOK:
        print("\n📢 Sending Slack notification...")
        success = service.send_slack(
            data['changed_files'],
            data['breaking_changes'],
            data['changelog_entries'],
            data['wiki_pages']
        )
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
