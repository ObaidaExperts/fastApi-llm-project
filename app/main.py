from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.tracing import TracingMiddleware

app = FastAPI(title="AI Chat Service")

# Middleware order matters: Auth -> Rate Limit -> Tracing
app.add_middleware(AuthMiddleware)
if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware)
app.add_middleware(TracingMiddleware)

app.include_router(api_router, prefix="/api")
