"""Pydantic models for API request/response validation."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    user_id: str
    message: str


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    response: str
