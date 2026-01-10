"""
Unit tests for authentication middleware.
"""
from unittest.mock import Mock

import pytest
from fastapi import Request

from app.middleware.auth_middleware import AuthMiddleware


class TestAuthMiddleware:
    """Test cases for authentication middleware."""

    @pytest.fixture
    def middleware(self):
        """Create auth middleware instance."""
        return AuthMiddleware(app=Mock())

    @pytest.fixture
    def mock_call_next(self):
        """Create a mock call_next function."""

        async def call_next(request):
            response = Mock()
            response.status_code = 200
            return response

        return call_next

    @pytest.mark.asyncio
    async def test_auth_middleware_health_endpoint_bypassed(self, middleware, mock_call_next):
        """Test that health endpoint bypasses auth extraction."""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/health"
        request.headers = {}

        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_auth_middleware_docs_bypassed(self, middleware, mock_call_next):
        """Test that docs endpoint bypasses auth extraction."""
        request = Mock(spec=Request)
        request.url.path = "/docs"
        request.headers = {}

        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_auth_middleware_extracts_api_key(self, middleware, mock_call_next):
        """Test that middleware extracts API key and sets user_id."""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/chat/stream"
        request.headers = {"X-API-Key": "test-api-key-123"}
        request.state = Mock()

        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200
        assert hasattr(request.state, "user_id")
        assert request.state.user_id == "user1"
        assert request.state.auth_method == "api_key"

    @pytest.mark.asyncio
    async def test_auth_middleware_extracts_oauth_token(self, middleware, mock_call_next):
        """Test that middleware extracts OAuth token and sets user_id."""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/chat/stream"
        request.headers = {"Authorization": "Bearer oauth_test123"}
        request.state = Mock()

        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200
        assert hasattr(request.state, "user_id")
        assert request.state.user_id == "user_test123"
        assert request.state.auth_method == "oauth"

    @pytest.mark.asyncio
    async def test_auth_middleware_no_auth_continues(self, middleware, mock_call_next):
        """Test that middleware continues when no auth is provided."""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/chat/stream"
        request.headers = {}
        request.state = Mock()
        # Ensure user_id is not set initially
        if hasattr(request.state, "user_id"):
            delattr(request.state, "user_id")

        response = await middleware.dispatch(request, mock_call_next)
        assert response.status_code == 200
        # Should not have user_id set when no auth provided
        assert not hasattr(request.state, "user_id")
