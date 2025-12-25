import aiosqlite
from pathlib import Path

from app.config import settings

DATABASE_PATH = Path(settings.database_path)


async def get_db() -> aiosqlite.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    db = await get_db()
    try:
        await db.executescript("""
              -- Conversation history (per user, global across guilds)
              CREATE TABLE IF NOT EXISTS conversations (
                  id INTEGER PRIMARY KEY,
                  user_id TEXT NOT NULL,
                  role TEXT NOT NULL,
                  content TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              );

              -- Watched repositories (per guild)
              CREATE TABLE IF NOT EXISTS repos (
                  id INTEGER PRIMARY KEY,
                  guild_id TEXT NOT NULL,
                  owner TEXT NOT NULL,
                  name TEXT NOT NULL,
                  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  UNIQUE(guild_id, owner, name)
              );

              -- Guild configuration
              CREATE TABLE IF NOT EXISTS guild_config (
                  guild_id TEXT PRIMARY KEY,
                  notification_channel_id TEXT
              );
          """)
        await db.commit()
        print("Database initialized successfully")
    finally:
        await db.close()
