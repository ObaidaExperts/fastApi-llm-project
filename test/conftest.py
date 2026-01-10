"""
Pytest configuration and shared fixtures.
"""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_api_key():
    """Return a valid test API key."""
    return "test-api-key-123"


@pytest.fixture
def mock_oauth_token():
    """Return a valid test OAuth token."""
    return "oauth_test123"


@pytest.fixture
def mock_chat_request():
    """Return a mock chat request payload."""
    return {"messages": [{"role": "user", "content": "Hello, how are you?"}]}


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch("app.core.config.settings") as mock:
        mock.API_KEYS = {
            "test-api-key-123": "user1",
            "test-api-key-456": "user2",
        }
        mock.RATE_LIMIT_ENABLED = True
        mock.RATE_LIMIT_PER_MINUTE = 60
        mock.RATE_LIMIT_PER_HOUR = 1000
        yield mock
