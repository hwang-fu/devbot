import time
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

start_time = time.time()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health():
    uptime = time.time() - start_time
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "version": "0.1.0",
        "port": settings.port,
    }


@app.post("/test-db")
async def test_db_write(message: str = "Hello from test"):
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


@app.get("/test-db")
async def test_db_read():
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM conversations WHERE user_id = 'test-user' ORDER BY id DESC LIMIT 5"
        )
        rows = await cursor.fetchall()
        return {"rows": [dict(row) for row in rows]}
    finally:
        await db.close()
