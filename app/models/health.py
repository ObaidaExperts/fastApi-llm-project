from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(
        ...,
        description="Service health status",
        examples=["ok"],
        pattern="^(ok|error)$",
    )
    trace_id: str = Field(
        ...,
        description="Unique trace ID for this request",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "ok",
                    "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                }
            ]
        }
    }
