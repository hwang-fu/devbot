"""Router for GitHub webhook handling."""

import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Request

from app.config import settings
from app.database import get_db


router = APIRouter(prefix="/webhook", tags=["github"])


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature."""
    if not signature.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    """Receive and process GitHub webhook events."""
    payload = await request.body()

    # Verify signature if secret is configured
    if settings.github_webhook_secret:
        if not x_hub_signature_256:
            raise HTTPException(status_code=401, detail="Missing signature")
        if not verify_signature(
            payload, x_hub_signature_256, settings.github_webhook_secret
        ):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse JSON payload
    data = await request.json()

    # Only handle issue events for now
    if x_github_event == "issues":
        await handle_issue_event(data)
        return {"status": "processed", "event": "issues"}

    # Ignore other events
    return {"status": "ignored", "event": x_github_event}


async def handle_issue_event(data: dict):
    """Handle GitHub issue events."""
    action = data.get("action")
    issue = data.get("issue", {})
    repo = data.get("repository", {})

    repo_owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    # Find guilds watching this repo
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT guild_id FROM repos WHERE owner = ? AND name = ?",
            (repo_owner, repo_name),
        )
        guilds = await cursor.fetchall()

        if not guilds:
            print(f"No guilds watching {repo_owner}/{repo_name}")
            return

        # Build the embed
        from app.services.discord import build_issue_embed, send_channel_message

        embed = build_issue_embed(action, issue, repo)

        # Send to each guild's notification channel
        for guild in guilds:
            guild_id = guild["guild_id"]
            cursor = await db.execute(
                "SELECT notification_channel_id FROM guild_config WHERE guild_id = ?",
                (guild_id,),
            )
            config = await cursor.fetchone()
            if config and config["notification_channel_id"]:
                await send_channel_message(config["notification_channel_id"], embed)
                print(f"Sent notification to guild {guild_id}")
            else:
                print(f"Guild {guild_id} has no notification channel set")
    finally:
        await db.close()
