"""
Unit tests for OAuth authentication.
"""
import pytest
from fastapi import HTTPException, status

from app.core.oauth import verify_bearer_token


class TestOAuthAuth:
    """Test cases for OAuth authentication."""

    @pytest.mark.asyncio
    async def test_verify_bearer_token_valid(self):
        """Test verification of a valid bearer token."""
        authorization = "Bearer oauth_test123"
        auth_context = await verify_bearer_token(authorization)
        assert auth_context.user_id == "user_test123"

    @pytest.mark.asyncio
    async def test_verify_bearer_token_invalid_prefix(self):
        """Test verification with invalid token prefix."""
        authorization = "Bearer invalid_token"
        with pytest.raises(HTTPException) as exc_info:
            await verify_bearer_token(authorization)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid bearer token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_verify_bearer_token_missing(self):
        """Test verification when authorization header is missing."""
        authorization = None
        with pytest.raises(HTTPException) as exc_info:
            await verify_bearer_token(authorization)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Bearer token is missing" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_verify_bearer_token_wrong_format(self):
        """Test verification with wrong authorization format."""
        authorization = "Basic dGVzdDp0ZXN0"
        with pytest.raises(HTTPException) as exc_info:
            await verify_bearer_token(authorization)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_verify_bearer_token_no_bearer_prefix(self):
        """Test verification without Bearer prefix."""
        authorization = "oauth_test123"
        with pytest.raises(HTTPException) as exc_info:
            await verify_bearer_token(authorization)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_verify_bearer_token_different_oauth_prefixes(self):
        """Test verification with different oauth token prefixes."""
        # Test with oauth_ prefix
        auth1 = await verify_bearer_token("Bearer oauth_user1")
        assert auth1.user_id == "user_user1"

        # Test with oauth_ prefix and numbers
        auth2 = await verify_bearer_token("Bearer oauth_12345")
        assert auth2.user_id == "user_12345"
