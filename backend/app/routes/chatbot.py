from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.database.mongodb import chatbot_sessions_collection
from app.routes.auth import get_current_user
from app.services.nlp_service import get_wellness_reply

router = APIRouter(prefix="/api", tags=["chatbot"])


class ChatMessage(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/chat")
async def chat(payload: ChatMessage, current_user: dict = Depends(get_current_user)):
    reply = get_wellness_reply(payload.message)
    now = datetime.now(timezone.utc)

    entry = {"role": "user", "text": payload.message, "at": now.isoformat()}
    reply_entry = {"role": "assistant", "text": reply["reply"], "at": now.isoformat()}

    coll = chatbot_sessions_collection()
    if payload.session_id:
        from bson import ObjectId
        await coll.update_one(
            {"_id": ObjectId(payload.session_id)},
            {"$push": {"messages": {"$each": [entry, reply_entry]}}},
        )
        session_id = payload.session_id
    else:
        doc = {
            "user_id": str(current_user["_id"]),
            "messages": [entry, reply_entry],
            "created_at": now,
        }
        result = await coll.insert_one(doc)
        session_id = str(result.inserted_id)

    return {"session_id": session_id, "reply": reply["reply"], "source": reply["source"]}
