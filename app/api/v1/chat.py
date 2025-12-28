from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.chat_service import generate_chat_stream
from app.core.database import DatabaseSession, get_db
from app.core.auth import AuthContext, get_auth_context

router = APIRouter(prefix="/chat")

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    db: DatabaseSession = Depends(get_db),
    auth: AuthContext = Depends(get_auth_context),
):
    user_message = request.messages[-1].content

    async def event_generator():
        async for chunk in generate_chat_stream(user_message):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
