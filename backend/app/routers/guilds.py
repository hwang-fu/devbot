"""Router for guild-specific endpoints (repos, config)."""

from fastapi import APIRouter, HTTPException

from app.database import get_db

router = APIRouter(prefix="/guilds", tags=["guilds"])


@router.get("/{guild_id}/repos")
async def list_repos(guild_id: str):
    """List all watched repos for a guild."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT owner, name, added_at FROM repos WHERE guild_id = ? "
            "ORDER BY added_at DESC",
            (guild_id,),
        )
        rows = await cursor.fetchall()
        return {"guild_id": guild_id, "repos": [dict(row) for row in rows]}
    finally:
        await db.close()
