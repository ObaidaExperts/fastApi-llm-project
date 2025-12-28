from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.tracing import generate_trace_id, set_trace_id

class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Trace-Id") or generate_trace_id()
        set_trace_id(trace_id)

        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response
