"""FastAPI application entry point."""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.routers import chat, debug
from app.services.ollama import verify_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await verify_model()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(chat.router)
app.include_router(debug.router)


start_time = time.time()


@app.get("/")
async def root():
    """Basic status check endpoint."""
    return {"status": "ok"}


@app.get("/health")
async def health():
    """Health check with uptime and version info."""
    uptime = time.time() - start_time
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "version": "0.1.0",
        "port": settings.port,
    }
