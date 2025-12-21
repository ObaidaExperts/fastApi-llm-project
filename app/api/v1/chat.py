from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.chat_service import generate_chat_stream

router = APIRouter(prefix="/chat")

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    user_message = request.messages[-1].content

    async def event_generator():
        async for token in generate_chat_stream(user_message):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
