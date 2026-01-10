"""
Unit tests for unified authentication system.
"""
import pytest
from fastapi import HTTPException, status
from app.core.auth import AuthContext, get_auth_context


class TestAuthContext:
    """Test cases for AuthContext class."""

    def test_auth_context_creation(self):
        """Test creating an AuthContext instance."""
        auth = AuthContext(user_id="user1", auth_method="api_key")
        assert auth.user_id == "user1"
        assert auth.auth_method == "api_key"

    def test_auth_context_default_method(self):
        """Test AuthContext with default auth_method."""
        auth = AuthContext(user_id="user1")
        assert auth.user_id == "user1"
        assert auth.auth_method == "unknown"


class TestUnifiedAuth:
    """Test cases for unified authentication."""

    @pytest.mark.asyncio
    async def test_get_auth_context_with_api_key(self):
        """Test authentication with valid API key."""
        api_key = "test-api-key-123"
        auth_context = await get_auth_context(api_key=api_key)
        assert auth_context.user_id == "user1"
        assert auth_context.auth_method == "api_key"

    @pytest.mark.asyncio
    async def test_get_auth_context_with_oauth(self):
        """Test authentication with valid OAuth token."""
        authorization = "Bearer oauth_test123"
        auth_context = await get_auth_context(authorization=authorization)
        assert auth_context.user_id == "user_test123"
        assert auth_context.auth_method == "oauth"

    @pytest.mark.asyncio
    async def test_get_auth_context_api_key_precedence(self):
        """Test that API key takes precedence over OAuth token."""
        api_key = "test-api-key-123"
        authorization = "Bearer oauth_test123"
        auth_context = await get_auth_context(api_key=api_key, authorization=authorization)
        assert auth_context.auth_method == "api_key"
        assert auth_context.user_id == "user1"

    @pytest.mark.asyncio
    async def test_get_auth_context_no_auth(self):
        """Test authentication failure when no credentials provided."""
        with pytest.raises(HTTPException) as exc_info:
            await get_auth_context(api_key=None, authorization=None)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Authentication required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_auth_context_invalid_api_key_falls_back_to_oauth(self):
        """Test that invalid API key falls back to OAuth."""
        api_key = "invalid-key"
        authorization = "Bearer oauth_test123"
        auth_context = await get_auth_context(api_key=api_key, authorization=authorization)
        assert auth_context.auth_method == "oauth"
        assert auth_context.user_id == "user_test123"

    @pytest.mark.asyncio
    async def test_get_auth_context_invalid_both(self):
        """Test authentication failure when both credentials are invalid."""
        api_key = "invalid-key"
        authorization = "Bearer invalid_token"
        with pytest.raises(HTTPException) as exc_info:
            await get_auth_context(api_key=api_key, authorization=authorization)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
