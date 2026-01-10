from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
from app.core.auth import get_auth_context

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract authentication info and store in request state.
    This allows rate limiting to use user-based keys.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip auth extraction for public endpoints
        if request.url.path in ["/api/v1/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        # Try to extract auth info (but don't fail if not present)
        try:
            api_key = request.headers.get("X-API-Key")
            authorization = request.headers.get("Authorization")
            
            if api_key or authorization:
                auth_context = await get_auth_context(api_key=api_key, authorization=authorization)
                request.state.user_id = auth_context.user_id
                request.state.auth_method = auth_context.auth_method
        except HTTPException:
            # Auth failed, but let the endpoint handle it
            pass
        
        return await call_next(request)
