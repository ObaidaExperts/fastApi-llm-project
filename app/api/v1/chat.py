import json

from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse

from app.core.auth import AuthContext, get_auth_context
from app.core.database import DatabaseSession, get_db
from app.models.chat import ChatRequest
from app.services.chat_service import stream_chat_tokens

router = APIRouter(prefix="/chat")


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    db: DatabaseSession = Depends(get_db),
    api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None),
    auth: AuthContext = Depends(get_auth_context),
):
    """
    Stream chat responses with authentication required.
    Supports both API Key and OAuth authentication.
    """
    user_message = request.messages[-1].content

    async def event_generator():
        async for chunk in stream_chat_tokens(user_message):
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Auth-Method": auth.auth_method,
            "X-User-ID": auth.user_id,
        },
    )
