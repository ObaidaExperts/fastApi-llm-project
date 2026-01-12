"""
Unit tests for endpoint edge cases and error handling.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestChatEndpointEdgeCases:
    """Test cases for chat endpoint edge cases."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_chat_endpoint_invalid_json(self, client):
        """Test chat endpoint with invalid JSON."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123", "Content-Type": "application/json"},
            data="invalid json",
        )
        assert response.status_code == 422

    def test_chat_endpoint_missing_messages(self, client):
        """Test chat endpoint with missing messages field."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={},
        )
        assert response.status_code == 422

    def test_chat_endpoint_empty_messages_array(self, client):
        """Test chat endpoint with empty messages array."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={"messages": []},
        )
        assert response.status_code == 422

    def test_chat_endpoint_invalid_message_structure(self, client):
        """Test chat endpoint with invalid message structure."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={"messages": [{"invalid": "structure"}]},
        )
        assert response.status_code == 422

    def test_chat_endpoint_invalid_role(self, client):
        """Test chat endpoint with invalid role."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={"messages": [{"role": "invalid", "content": "Hello"}]},
        )
        assert response.status_code == 422

    def test_chat_endpoint_empty_content(self, client):
        """Test chat endpoint with empty content."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={"messages": [{"role": "user", "content": ""}]},
        )
        assert response.status_code == 422

    def test_chat_endpoint_missing_content(self, client):
        """Test chat endpoint with missing content field."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={"messages": [{"role": "user"}]},
        )
        assert response.status_code == 422

    def test_chat_endpoint_very_long_message(self, client):
        """Test chat endpoint with very long message content."""
        long_content = "a" * 10000
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={"messages": [{"role": "user", "content": long_content}]},
        )
        # Should still work (no length limit in model)
        assert response.status_code == 200

    def test_chat_endpoint_multiple_messages(self, client):
        """Test chat endpoint with multiple messages."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json={
                "messages": [
                    {"role": "system", "content": "You are helpful"},
                    {"role": "user", "content": "First message"},
                    {"role": "assistant", "content": "Response"},
                    {"role": "user", "content": "Second message"},
                ]
            },
        )
        assert response.status_code == 200


class TestAuthEndpointEdgeCases:
    """Test cases for auth endpoint edge cases."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_oauth_callback_missing_code(self, client):
        """Test OAuth callback without code parameter."""
        response = client.get("/api/v1/auth/callback")
        assert response.status_code == 422

    def test_oauth_callback_empty_code(self, client):
        """Test OAuth callback with empty code."""
        response = client.get("/api/v1/auth/callback?code=")
        # May return 422 or 200 depending on validation
        assert response.status_code in [200, 422]

    def test_oauth_me_without_token(self, client):
        """Test OAuth me endpoint without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_oauth_me_invalid_token_format(self, client):
        """Test OAuth me endpoint with invalid token format."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "InvalidFormat token123"},
        )
        assert response.status_code in [401, 403]

    def test_oauth_me_malformed_authorization_header(self, client):
        """Test OAuth me endpoint with malformed authorization header."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "NotBearer token123"},
        )
        assert response.status_code in [401, 403]


class TestHealthEndpointEdgeCases:
    """Test cases for health endpoint edge cases."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_health_endpoint_wrong_method(self, client):
        """Test health endpoint with wrong HTTP method."""
        response = client.post("/api/v1/health")
        assert response.status_code == 405

    def test_health_endpoint_response_always_ok(self, client):
        """Test that health endpoint always returns ok status."""
        for _ in range(5):
            response = client.get("/api/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert "trace_id" in data

    def test_health_endpoint_trace_id_unique(self, client):
        """Test that health endpoint generates unique trace IDs."""
        trace_ids = set()
        for _ in range(10):
            response = client.get("/api/v1/health")
            data = response.json()
            trace_ids.add(data["trace_id"])

        # All trace IDs should be unique
        assert len(trace_ids) == 10
