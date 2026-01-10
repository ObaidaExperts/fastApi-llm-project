from fastapi import APIRouter, Depends

from app.core.database import DatabaseSession, get_db
from app.core.tracing import get_trace_id

router = APIRouter()


@router.get("/health")
async def health_check(db: DatabaseSession = Depends(get_db)):
    trace_id = get_trace_id()

    return {
        "status": "ok",
        "trace_id": trace_id,
    }


# @router.get(
#     "/health",
#     response_model=HealthResponse,
#     summary="Health check (v1)",
# )
# async def health_check():
#     return HealthResponse(
#         status="ok",
#         service="ai-chat-service",
#     )
