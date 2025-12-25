"""Ollama AI service for chat completions."""

import httpx

from app.config import settings


async def verify_model():
    """Verify the configured Ollama model is available."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.ollama_host}/api/tags",
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            models = [m["name"].split(":")[0] for m in data.get("models", [])]

            if settings.ollama_model not in models:
                raise RuntimeError(
                    f"Model '{settings.ollama_model}' not found. "
                    f"Available: {models}. Run: ollama pull {settings.ollama_model}"
                )
            print(f"Ollama model '{settings.ollama_model}' verified")
        except httpx.ConnectError:
            raise RuntimeError(
                f"Cannot connect to Ollama at {settings.ollama_host}. "
                "Is Ollama running?"
            )


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
                "model": settings.ollama_model,
                "messages": messages,
                "stream": False,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
