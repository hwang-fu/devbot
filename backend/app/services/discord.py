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
