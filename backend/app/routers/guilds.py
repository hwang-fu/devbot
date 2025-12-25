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


@router.post("/{guild_id}/repos")
async def add_repo(guild_id: str, owner: str, name: str):
    """Add a repo to watch for a guild."""
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO repos (guild_id, owner, name) VALUES (?, ?, ?)",
            (guild_id, owner, name),
        )
        await db.commit()
        return {"status": "added", "guild_id": guild_id, "owner": owner, "name": name}
    except Exception:
        raise HTTPException(
            status_code=400, detail="Repo already exists for this guild"
        )
    finally:
        await db.close()


@router.delete("/{guild_id}/repos/{owner}/{name}")
async def remove_repo(guild_id: str, owner: str, name: str):
    """Remove a watched repo from a guild."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "DELETE FROM repos WHERE guild_id = ? AND owner = ? AND name = ?",
            (guild_id, owner, name),
        )
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Repo not found")
        return {"status": "removed", "guild_id": guild_id, "owner": owner, "name": name}
    finally:
        await db.close()
