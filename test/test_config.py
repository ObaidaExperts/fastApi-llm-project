"""
Unit tests for configuration.
"""

from app.core.config import settings


class TestSettings:
    """Test cases for Settings class."""

    def test_settings_default_values(self):
        """Test that settings have default values."""
        assert settings.API_KEY_HEADER == "X-API-Key"
        assert isinstance(settings.API_KEYS, dict)
        assert len(settings.API_KEYS) > 0

    def test_settings_api_keys_exist(self):
        """Test that default API keys are configured."""
        assert "test-api-key-123" in settings.API_KEYS
        assert "test-api-key-456" in settings.API_KEYS
        assert settings.API_KEYS["test-api-key-123"] == "user1"
        assert settings.API_KEYS["test-api-key-456"] == "user2"

    def test_settings_rate_limit_defaults(self):
        """Test rate limit default values."""
        assert settings.RATE_LIMIT_ENABLED is True
        assert settings.RATE_LIMIT_PER_MINUTE == 60
        assert settings.RATE_LIMIT_PER_HOUR == 1000

    def test_settings_oauth_config_exists(self):
        """Test that OAuth configuration exists."""
        assert hasattr(settings, "OAUTH_CLIENT_ID")
        assert hasattr(settings, "OAUTH_CLIENT_SECRET")
        assert hasattr(settings, "OAUTH_AUTHORIZATION_URL")
        assert hasattr(settings, "OAUTH_TOKEN_URL")
        assert hasattr(settings, "OAUTH_REDIRECT_URI")

    def test_settings_redis_url_optional(self):
        """Test that Redis URL is optional."""
        assert hasattr(settings, "REDIS_URL")
        # Can be None for in-memory storage
        assert settings.REDIS_URL is None or isinstance(settings.REDIS_URL, str)
