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
