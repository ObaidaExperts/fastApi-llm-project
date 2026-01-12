from fastapi import APIRouter, Depends

from app.core.database import DatabaseSession, get_db
from app.core.tracing import get_trace_id
from app.models.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Returns the health status of the service and a trace ID for request tracking",
    tags=["health"],
)
async def health_check(db: DatabaseSession = Depends(get_db)) -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Service status and trace ID
    """
    trace_id = get_trace_id()

    return HealthResponse(
        status="ok",
        trace_id=trace_id,
    )
