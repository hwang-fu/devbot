import time
from fastapi import FastAPI

app = FastAPI()

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
    }
