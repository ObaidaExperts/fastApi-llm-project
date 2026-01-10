"""
Unit tests for rate limiting middleware.
"""
import pytest
import time
from fastapi import Request
from starlette.responses import Response
from unittest.mock import Mock, patch, AsyncMock
from app.middleware.rate_limit import RateLimitMiddleware, get_rate_limit_key
from app.core.config import settings


class TestRateLimitKey:
    """Test cases for rate limit key generation."""

    def test_get_rate_limit_key_with_user_id(self):
        """Test rate limit key generation with user_id in request state."""
        request = Mock(spec=Request)
        request.state.user_id = "user1"
        request.state.auth_method = "api_key"
        
        key = get_rate_limit_key(request)
        assert key == "user:user1"

    def test_get_rate_limit_key_without_user_id(self):
        """Test rate limit key generation without user_id (uses IP)."""
        request = Mock(spec=Request)
        request.client = Mock()
        request.client.host = "127.0.0.1"
        # Ensure state doesn't have user_id
        request.state = Mock()
        if hasattr(request.state, 'user_id'):
            delattr(request.state, 'user_id')
        
        # Mock get_remote_address function
        with patch('app.middleware.rate_limit.get_remote_address', return_value="127.0.0.1"):
            key = get_rate_limit_key(request)
            assert key == "127.0.0.1"


class TestRateLimitMiddleware:
    """Test cases for rate limiting middleware."""

    @pytest.fixture
    def middleware(self):
        """Create rate limit middleware instance."""
        return RateLimitMiddleware(app=Mock())

    @pytest.fixture
    def mock_request(self):
        """Create a mock request."""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/chat/stream"
        request.state.user_id = "user1"
        request.client.host = "127.0.0.1"
        return request

    @pytest.fixture
    def mock_call_next(self):
        """Create a mock call_next function."""
        async def call_next(request):
            return Response(content="OK", status_code=200)
        return call_next

    @pytest.mark.asyncio
    async def test_rate_limit_health_endpoint_bypassed(self, middleware, mock_call_next):
        """Test that health endpoint bypasses rate limiting."""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/health"
        
        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_rate_limit_docs_bypassed(self, middleware, mock_call_next):
        """Test that docs endpoint bypasses rate limiting."""
        request = Mock(spec=Request)
        request.url.path = "/docs"
        
        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_rate_limit_within_limit(self, middleware, mock_request, mock_call_next):
        """Test that requests within limit are allowed."""
        # Reset storage
        from app.middleware.rate_limit import limiter
        limiter.storage = {}
        
        response = await middleware.dispatch(mock_request, mock_call_next)
        assert response.status_code == 200
        assert "X-RateLimit-Limit-Minute" in response.headers
        assert "X-RateLimit-Limit-Hour" in response.headers

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded_minute(self, middleware, mock_request, mock_call_next):
        """Test that requests exceeding minute limit are blocked."""
        from app.middleware.rate_limit import limiter
        from app.core.config import settings
        from fastapi import HTTPException
        
        # Reset storage
        limiter.storage = {}
        
        # Set up to exceed minute limit
        key = get_rate_limit_key(mock_request)
        minute_key = f"{key}:minute"
        current_time = time.time()
        
        limiter.storage[minute_key] = {
            "count": settings.RATE_LIMIT_PER_MINUTE,
            "reset": current_time + 60
        }
        
        with pytest.raises(HTTPException) as exc_info:
            await middleware.dispatch(mock_request, mock_call_next)
        # Should raise HTTPException with 429 status
        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_rate_limit_headers_present(self, middleware, mock_request, mock_call_next):
        """Test that rate limit headers are present in response."""
        from app.middleware.rate_limit import limiter
        limiter.storage = {}
        
        response = await middleware.dispatch(mock_request, mock_call_next)
        
        assert "X-RateLimit-Limit-Minute" in response.headers
        assert "X-RateLimit-Limit-Hour" in response.headers
        assert "X-RateLimit-Remaining-Minute" in response.headers
        assert "X-RateLimit-Remaining-Hour" in response.headers
