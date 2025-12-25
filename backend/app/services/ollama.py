"""Ollama AI service for chat completions."""

import httpx

from app.config import settings


async def chat_completion(messages: list[dict]) -> str:
    """
    Send messages to Ollama and get AI response.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.

    Returns:
        The AI assistant's response text.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.ollama_host}/api/chat",
            json={
                "model": "llama3",
                "messages": messages,
                "stream": False,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
