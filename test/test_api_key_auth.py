"""
Unit tests for API key authentication.
"""
import pytest
from fastapi import HTTPException, status

from app.core.api_key_auth import verify_api_key, verify_api_key_value


class TestAPIKeyAuth:
    """Test cases for API key authentication."""

    def test_verify_api_key_value_valid(self):
        """Test verification of a valid API key."""
        api_key = "test-api-key-123"
        user_id = verify_api_key_value(api_key)
        assert user_id == "user1"

    def test_verify_api_key_value_invalid(self):
        """Test verification of an invalid API key."""
        api_key = "invalid-key"
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key_value(api_key)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid API key" in exc_info.value.detail

    def test_verify_api_key_value_missing(self):
        """Test verification when API key is missing."""
        api_key = None
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key_value(api_key)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "API key is missing" in exc_info.value.detail

    def test_verify_api_key_value_empty_string(self):
        """Test verification when API key is empty string."""
        api_key = ""
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key_value(api_key)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_api_key_value_multiple_keys(self):
        """Test verification with multiple valid API keys."""
        # Test first key
        user_id1 = verify_api_key_value("test-api-key-123")
        assert user_id1 == "user1"

        # Test second key
        user_id2 = verify_api_key_value("test-api-key-456")
        assert user_id2 == "user2"

    @pytest.mark.asyncio
    async def test_verify_api_key_with_security_dependency(self):
        """Test verify_api_key with Security dependency."""
        api_key = "test-api-key-123"
        auth_context = await verify_api_key(api_key)
        assert auth_context.user_id == "user1"
        assert hasattr(auth_context, "user_id")
