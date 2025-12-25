from fastapi import APIRouter
from pydantic import BaseModel

from app.database import get_db
from app.services.ollama import chat_completion

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    db = await get_db()
    try:
        # Get conversation history
        cursor = await db.execute(
            "SELECT role, content FROM conversations WHERE user_id = ? ORDER BY id",
            (request.user_id,),
        )
        rows = await cursor.fetchall()
        messages = [{"role": row["role"], "content": row["content"]} for row in rows]

        # Add new user message
        messages.append({"role": "user", "content": request.message})

        # Get AI response
        response = await chat_completion(messages)

        # Save both messages to database
        await db.execute(
            "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
            (request.user_id, "user", request.message),
        )
        await db.execute(
            "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
            (request.user_id, "assistant", response),
        )
        await db.commit()

        return ChatResponse(response=response)
    finally:
        await db.close()


@router.post("/clear")
async def clear_history(user_id: str):
    db = await get_db()
    try:
        await db.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        await db.commit()
        return {"status": "cleared", "user_id": user_id}
    finally:
        await db.close()
