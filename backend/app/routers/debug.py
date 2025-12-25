"""Debug router for development/testing endpoints."""

from fastapi import APIRouter

from app.database import get_db

router = APIRouter(prefix="/debug", tags=["debug"])


@router.post("/test-db")
async def test_db_write(message: str = "Hello from test"):
    """Write test data to database (for development)."""
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
            ("test-user", "user", message),
        )
        await db.commit()
        return {"status": "written", "message": message}
    finally:
        await db.close()


@router.get("/test-db")
async def test_db_read():
    """Read test data from database (for development)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM conversations WHERE user_id = 'test-user' "
            "ORDER BY id DESC LIMIT 5"
        )
        rows = await cursor.fetchall()
        return {"rows": [dict(row) for row in rows]}
    finally:
        await db.close()
