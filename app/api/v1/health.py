from fastapi import APIRouter
from app.models.health import HealthResponse

router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check (v1)",
)
async def health_check():
    return HealthResponse(
        status="ok",
        service="ai-chat-service",
    )
