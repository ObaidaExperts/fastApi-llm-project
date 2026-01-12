import time
from collections.abc import Awaitable, Callable

from fastapi import HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Rate limit storage (in-memory for demo, use Redis in production)
if settings.REDIS_URL:
    # Configure Redis storage if available
    pass
else:
    # Use in-memory storage (type ignore for private attribute)
    limiter.storage = {}  # type: ignore[attr-defined]


def get_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key based on user authentication.
    Falls back to IP address if not authenticated.
    """
    # Try to get user ID from request state (set by auth)
    if hasattr(request.state, "user_id"):
        user_id: str = getattr(request.state, "user_id", "")
        return f"user:{user_id}"

    # Fall back to IP address
    ip_address: str = get_remote_address(request)
    return ip_address


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using slowapi.
    Limits requests per minute and per hour.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/api/v1/health", "/api/v1/ready", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        # Get rate limit key
        key = get_rate_limit_key(request)

        # Check per-minute limit
        minute_key = f"{key}:minute"
        storage = limiter.storage  # type: ignore[attr-defined]
        minute_count = storage.get(minute_key, {}).get("count", 0)
        minute_reset = storage.get(minute_key, {}).get("reset", 0)

        current_time = time.time()

        if minute_reset < current_time:
            # Reset minute counter
            storage[minute_key] = {"count": 1, "reset": current_time + 60}
        else:
            if minute_count >= settings.RATE_LIMIT_PER_MINUTE:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {settings.RATE_LIMIT_PER_MINUTE} requests per minute",
                    headers={
                        "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(minute_reset)),
                    },
                )
            storage[minute_key]["count"] += 1

        # Check per-hour limit
        hour_key = f"{key}:hour"
        hour_count = storage.get(hour_key, {}).get("count", 0)
        hour_reset = storage.get(hour_key, {}).get("reset", 0)

        if hour_reset < current_time:
            # Reset hour counter
            storage[hour_key] = {"count": 1, "reset": current_time + 3600}
        else:
            if hour_count >= settings.RATE_LIMIT_PER_HOUR:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {settings.RATE_LIMIT_PER_HOUR} requests per hour",
                    headers={
                        "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_HOUR),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(hour_reset)),
                    },
                )
            storage[hour_key]["count"] += 1

        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit-Minute"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Limit-Hour"] = str(settings.RATE_LIMIT_PER_HOUR)
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            max(0, settings.RATE_LIMIT_PER_MINUTE - storage[minute_key]["count"])
        )
        response.headers["X-RateLimit-Remaining-Hour"] = str(
            max(0, settings.RATE_LIMIT_PER_HOUR - storage[hour_key]["count"])
        )

        return response
