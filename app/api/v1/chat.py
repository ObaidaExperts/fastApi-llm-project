
from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse

from app.core.auth import AuthContext, get_auth_context
from app.core.database import DatabaseSession, get_db
from app.models.chat import ChatRequest, ChatStreamChunk
from app.services.chat_service import stream_chat_tokens

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/stream",
    response_model=None,  # StreamingResponse doesn't use response_model
    summary="Stream chat responses",
    description="Streams chat responses using Server-Sent Events (SSE). "
    "Requires authentication via API Key or OAuth Bearer token. "
    "Returns a stream of ChatStreamChunk objects.",
    responses={
        200: {
            "description": "Streaming response with chat tokens",
            "content": {
                "text/event-stream": {
                    "schema": {
                        "type": "string",
                        "format": "event-stream",
                        "example": 'data: {"token": "Hello", "trace_id": "abc123", "finished": false}\n\n',
                    }
                }
            },
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authentication required. Provide either API Key (X-API-Key header) or Bearer token (Authorization header)"
                    }
                }
            },
        },
        429: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {"detail": "Rate limit exceeded: 60 requests per minute"}
                }
            },
        },
    },
)
async def chat_stream(
    request: ChatRequest,
    db: DatabaseSession = Depends(get_db),
    api_key: str
    | None = Header(
        default=None,
        alias="X-API-Key",
        description="API key for authentication",
        examples=["test-api-key-123"],
    ),
    authorization: str
    | None = Header(
        default=None,
        description="Bearer token for OAuth authentication",
        examples=["Bearer oauth_demo_auth_code_12345"],
    ),
    auth: AuthContext = Depends(get_auth_context),
) -> StreamingResponse:
    """
    Stream chat responses with authentication required.

    This endpoint streams chat responses using Server-Sent Events (SSE).
    Each chunk follows the ChatStreamChunk model structure.

    Args:
        request: Chat request with messages
        db: Database session
        api_key: Optional API key header
        authorization: Optional OAuth bearer token
        auth: Authentication context (injected by dependency)

    Returns:
        StreamingResponse: SSE stream of ChatStreamChunk objects

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 429 if rate limit is exceeded
    """
    user_message = request.messages[-1].content

    async def event_generator():
        async for chunk in stream_chat_tokens(user_message):
            # Validate chunk structure matches ChatStreamChunk model
            chunk_model = ChatStreamChunk(**chunk)
            yield f"data: {chunk_model.model_dump_json()}\n\n"

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
