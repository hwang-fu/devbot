"""Discord API service for sending notifications."""

import httpx

from app.config import settings


async def send_channel_message(channel_id: str, embed: dict) -> bool:
    """Send an embed message to a Discord channel."""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {settings.discord_bot_token}",
        "Content-Type": "application/json",
    }
    payload = {"embeds": [embed]}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.status_code == 200


def build_issue_embed(action: str, issue: dict, repo: dict) -> dict:
    """Build a Discord embed for an issue event."""
    repo_name = f"{repo['owner']['login']}/{repo['name']}"
    issue_title = issue["title"]
    issue_url = issue["html_url"]
    issue_number = issue["number"]
    user = issue["user"]["login"]

    # Color based on action
    colors = {
        "opened": 0xFFA500,  # Orange
        "closed": 0x6E7681,  # Gray
        "reopened": 0x238636,  # Green
    }
    color = colors.get(action, 0xFFA500)

    return {
        "title": f"Issue #{issue_number} {action}",
        "description": issue_title,
        "url": issue_url,
        "color": color,
        "author": {"name": repo_name},
        "footer": {"text": f"by {user}"},
    }
