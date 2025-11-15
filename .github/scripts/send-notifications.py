#!/usr/bin/env python3
"""
Notification Service - Send updates to Discord/Slack
Handles character limits and formats messages beautifully
"""

import os
import sys
import re
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK_URL')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK_URL')
PUSHBULLET_TOKEN = os.environ.get('PUSHBULLET')

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
    
    def _get_commit_emoji(self, breaking_changes: List[Dict]) -> str:
        """Determine emoji based on commit type"""
        commit_title = self.commit_message.split('\n')[0].lower()
        
        if breaking_changes:
            return "⚠️"
        elif any(word in commit_title for word in ['feat', 'feature', 'add']):
            return "✨"
        elif any(word in commit_title for word in ['fix', 'bug']):
            return "🐛"
        elif any(word in commit_title for word in ['docs', 'documentation']):
            return "📚"
        return "📝"
    
    def _build_discord_embed_base(self, emoji: str) -> Dict:
        """Build base Discord embed structure"""
        commit_title = self.commit_message.split('\n')[0][:100]
        
        return {
            "title": f"{emoji} {commit_title}",
            "description": f"**{self.repo.split('/')[-1]}** • `{self.commit_sha}`",
            "color": 0xFF6B35 if emoji == "⚠️" else 0x4CAF50,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": f"by {self.actor}"},
            "fields": []
        }
    
    def _add_breaking_changes_field(self, embed: Dict, breaking_changes: List[Dict]):
        """Add breaking changes field to embed"""
        if not breaking_changes:
            return
        
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
    
    def _add_files_field(self, embed: Dict, changed_files: List[str]):
        """Add changed files field to embed"""
        if not changed_files:
            return
        
        files_text = "\n".join([f"• `{Path(f).name}`" for f in changed_files[:10]])
        if len(changed_files) > 10:
            files_text += f"\n... and {len(changed_files) - 10} more"
        
        embed["fields"].append({
            "name": f"📄 Files Changed ({len(changed_files)})",
            "value": self.truncate(files_text, DISCORD_EMBED_FIELD_LIMIT),
            "inline": True
        })
    
    def _add_wiki_field(self, embed: Dict, wiki_pages: List[str]):
        """Add wiki pages field to embed"""
        if not wiki_pages:
            return
        
        wiki_text = "\n".join([f"• [{page}](https://github.com/{self.repo}/wiki/{page})" 
                               for page in wiki_pages[:8]])
        if len(wiki_pages) > 8:
            wiki_text += f"\n... and {len(wiki_pages) - 8} more"
        
        embed["fields"].append({
            "name": f"📚 Wiki Pages Updated ({len(wiki_pages)})",
            "value": self.truncate(wiki_text, DISCORD_EMBED_FIELD_LIMIT),
            "inline": True
        })
    
    def _add_analysis_field(self, embed: Dict, analysis_summary: Optional[Dict]):
        """Add code analysis field to embed"""
        if not analysis_summary:
            return
        
        analysis_text = f"**Quality:** {analysis_summary['avg_quality_score']}/100\n"
        
        if analysis_summary['total_vulnerabilities'] > 0:
            analysis_text += f"⚠️ **{analysis_summary['total_vulnerabilities']} security issue(s)**\n"
        
        if analysis_summary['total_performance_issues'] > 0:
            analysis_text += f"🐌 **{analysis_summary['total_performance_issues']} performance issue(s)**\n"
        
        embed["fields"].append({
            "name": "📊 Code Analysis",
            "value": self.truncate(analysis_text, DISCORD_EMBED_FIELD_LIMIT),
            "inline": False
        })
    
    def send_discord(self, 
                     changed_files: List[str], 
                     breaking_changes: List[Dict],
                     changelog_entries: List[Dict],
                     wiki_pages: List[str],
                     analysis_summary: Optional[Dict] = None) -> bool:
        """Send formatted notification to Discord"""
        if not DISCORD_WEBHOOK:
            print("⚠️  No Discord webhook URL configured")
            return False
        
        # Build embed
        emoji = self._get_commit_emoji(breaking_changes)
        embed = self._build_discord_embed_base(emoji)
        
        # Add all field sections
        self._add_breaking_changes_field(embed, breaking_changes)
        self._add_files_field(embed, changed_files)
        self._add_wiki_field(embed, wiki_pages)
        self._add_analysis_field(embed, analysis_summary)
        
        # Add links
        embed["fields"].append({
            "name": "🔗 Links",
            "value": f"[View Workflow Run]({self.run_url}) • [View Wiki](https://github.com/{self.repo}/wiki)",
            "inline": False
        })
        
        # Build and send payload
        payload = {
            "username": "CI/CD Bot",
            "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            "embeds": [embed]
        }
        
        try:
            response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
            
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
                   wiki_pages: List[str],
                   analysis_summary: Optional[Dict] = None) -> bool:
        """Send formatted notification to Slack"""
        if not SLACK_WEBHOOK:
            print("⚠️  No Slack webhook URL configured")
            return False
        
        emoji = self._get_commit_emoji(breaking_changes)
        commit_title = self.commit_message.split('\n')[0][:100]
        
        blocks = self._build_slack_blocks(
            emoji, commit_title, breaking_changes, changed_files, 
            wiki_pages, analysis_summary
        )
        
        payload = {"blocks": blocks}
        
        try:
            response = requests.post(SLACK_WEBHOOK, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✓ Slack notification sent successfully")
                return True
            else:
                print(f"⚠️  Slack notification failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error sending Slack notification: {e}")
            return False
    
    def _build_slack_blocks(self, emoji: str, commit_title: str, 
                           breaking_changes: List[Dict], changed_files: List[str],
                           wiki_pages: List[str], analysis_summary: Optional[Dict]) -> List[Dict]:
        """Build Slack blocks"""
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"{emoji} {commit_title}"}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Commit:* `{self.commit_sha}`\n*By:* {self.actor}\n*Repo:* {self.repo}"
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
                "text": {"type": "mrkdwn", "text": f"*🚨 Breaking Changes*\n{breaking_text}"}
            })
        
        # Files, wiki, and analysis
        if changed_files or wiki_pages or analysis_summary:
            fields = []
            
            if changed_files:
                files_list = ", ".join([f"`{Path(f).name}`" for f in changed_files[:5]])
                if len(changed_files) > 5:
                    files_list += f" +{len(changed_files)-5} more"
                fields.append({"type": "mrkdwn", "text": f"*Files:* {files_list}"})
            
            if wiki_pages:
                wiki_list = ", ".join(wiki_pages[:5])
                if len(wiki_pages) > 5:
                    wiki_list += f" +{len(wiki_pages)-5} more"
                fields.append({"type": "mrkdwn", "text": f"*Wiki:* {wiki_list}"})
            
            if analysis_summary:
                analysis_text = f"*Quality:* {analysis_summary['avg_quality_score']}/100"
                if analysis_summary['total_vulnerabilities'] > 0:
                    analysis_text += f" | ⚠️ {analysis_summary['total_vulnerabilities']} security"
                if analysis_summary['total_performance_issues'] > 0:
                    analysis_text += f" | 🐌 {analysis_summary['total_performance_issues']} performance"
                fields.append({"type": "mrkdwn", "text": analysis_text})
            
            blocks.append({"type": "section", "fields": fields})
        
        # Actions
        blocks.append({
            "type": "actions",
            "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "View Workflow"}, "url": self.run_url},
                {"type": "button", "text": {"type": "plain_text", "text": "View Wiki"}, "url": f"https://github.com/{self.repo}/wiki"}
            ]
        })
        
        return blocks
    
    def send_pushbullet(self,
                        changed_files: List[str],
                        breaking_changes: List[Dict],
                        changelog_entries: List[Dict],
                        wiki_pages: List[str],
                        analysis_summary: Optional[Dict] = None) -> bool:
        """Send push notification via Pushbullet"""
        if not PUSHBULLET_TOKEN:
            print("⚠️  No Pushbullet token configured")
            return False
        
        # Generate dynamic title
        commit_title = self.commit_message.split('\n')[0][:100]
        
        # Choose emoji
        emoji = "📝"
        if breaking_changes:
            emoji = "⚠️"
        elif any(word in commit_title.lower() for word in ['feat', 'feature', 'add']):
            emoji = "✨"
        elif any(word in commit_title.lower() for word in ['fix', 'bug']):
            emoji = "🐛"
        elif any(word in commit_title.lower() for word in ['docs', 'documentation']):
            emoji = "📚"
        
        # Build notification body
        body_parts = [
            f"Repo: {self.repo}",
            f"By: {self.actor}",
            f"Commit: {self.commit_sha}",
        ]
        
        if breaking_changes:
            body_parts.append(f"\n⚠️ {len(breaking_changes)} BREAKING CHANGE(S)")
        
        if changed_files:
            file_list = ', '.join([Path(f).name for f in changed_files[:5]])
            if len(changed_files) > 5:
                file_list += f' +{len(changed_files)-5} more'
            body_parts.append(f"\nFiles: {file_list}")
        
        if wiki_pages:
            body_parts.append(f"Wiki: {len(wiki_pages)} page(s) updated")
        
        # Add analysis summary
        if analysis_summary:
            body_parts.append(f"\nQuality: {analysis_summary['avg_quality_score']}/100")
            if analysis_summary['total_vulnerabilities'] > 0:
                body_parts.append(f"⚠️ {analysis_summary['total_vulnerabilities']} security issues")
            if analysis_summary['total_performance_issues'] > 0:
                body_parts.append(f"🐌 {analysis_summary['total_performance_issues']} performance issues")
        
        body = '\n'.join(body_parts)
        
        # Pushbullet API
        url = "https://api.pushbullet.com/v2/pushes"
        headers = {
            "Access-Token": PUSHBULLET_TOKEN,
            "Content-Type": "application/json"
        }
        
        # Create link push for better interaction
        payload = {
            "type": "link",
            "title": f"{emoji} {commit_title}",
            "body": body,
            "url": self.run_url
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print("✓ Pushbullet notification sent successfully")
                return True
            else:
                print(f"⚠️  Pushbullet notification failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error sending Pushbullet notification: {e}")
            return False


def load_workflow_data():
    """Load data from workflow artifacts"""
    data = {
        'changed_files': [],
        'breaking_changes': [],
        'changelog_entries': [],
        'wiki_pages': [],
        'analysis_summary': None
    }
    
    # Load changed files
    if os.path.exists('changed_files.txt'):
        with open('changed_files.txt', 'r') as f:
            data['changed_files'] = [line.strip() for line in f if line.strip()]
    
    # Load breaking changes
    if os.path.exists('breaking_changes.txt'):
        # Indicates breaking changes were detected
        data['breaking_changes'] = [{'symbol': 'API', 'message': 'Breaking changes detected'}]
    
    # Load wiki summary - only get pages that were ACTUALLY updated
    if os.path.exists('wiki_summary.md'):
        with open('wiki_summary.md', 'r') as f:
            content = f.read()
            # Only look at "Updates Made" section for actually changed pages
            in_updates = False
            for line in content.split('\n'):
                if '## Updates Made' in line:
                    in_updates = True
                elif in_updates and line.startswith('- `'):
                    # Extract page name from: - `file.ts` → [Page-Name]
                    match = re.search(r'\[([^\]]+)\]', line)
                    if match:
                        data['wiki_pages'].append(match.group(1))
    
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
    
    # Load code analysis results
    try:
        if os.path.exists('analysis_results.json'):
            with open('analysis_results.json', 'r') as f:
                analysis_data = json.load(f)
                
                if analysis_data:
                    # Calculate summary
                    avg_score = sum(r['quality_score']['total'] for r in analysis_data) / len(analysis_data)
                    total_vulns = sum(len(r['security_vulnerabilities']) for r in analysis_data)
                    total_perf = sum(len(r['performance_issues']) for r in analysis_data)
                    
                    data['analysis_summary'] = {
                        'files_analyzed': len(analysis_data),
                        'avg_quality_score': round(avg_score, 1),
                        'total_vulnerabilities': total_vulns,
                        'total_performance_issues': total_perf,
                        'details': analysis_data
                    }
    except Exception as e:
        print(f"Warning: Could not load analysis results: {e}")
    
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
    
    # Print analysis summary if available
    if data.get('analysis_summary'):
        summary = data['analysis_summary']
        print(f"\n📊 Code Analysis Summary:")
        print(f"   Files: {summary['files_analyzed']}")
        print(f"   Avg Quality: {summary['avg_quality_score']}/100")
        print(f"   Security Issues: {summary['total_vulnerabilities']}")
        print(f"   Performance Issues: {summary['total_performance_issues']}")
    
    # Send notifications
    results = []
    
    if DISCORD_WEBHOOK:
        print("\n📢 Sending Discord notification...")
        success = service.send_discord(
            data['changed_files'],
            data['breaking_changes'],
            data['changelog_entries'],
            data['wiki_pages'],
            data.get('analysis_summary')
        )
        results.append(('Discord', success))
    
    if SLACK_WEBHOOK:
        print("\n📢 Sending Slack notification...")
        success = service.send_slack(
            data['changed_files'],
            data['breaking_changes'],
            data['changelog_entries'],
            data['wiki_pages'],
            data.get('analysis_summary')
        )
        results.append(('Slack', success))
    
    if PUSHBULLET_TOKEN:
        print("\n📢 Sending Pushbullet notification...")
        success = service.send_pushbullet(
            data['changed_files'],
            data['breaking_changes'],
            data['changelog_entries'],
            data['wiki_pages'],
            data.get('analysis_summary')
        )
        results.append(('Pushbullet', success))
    
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
