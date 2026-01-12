"""
Unit tests for Pydantic models.
"""
import pytest
from pydantic import ValidationError

from app.models.auth import OAuthCallbackQuery, OAuthTokenResponse, UserInfoResponse
from app.models.chat import ChatMessage, ChatRequest, ChatStreamChunk
from app.models.health import HealthResponse


class TestChatMessage:
    """Test cases for ChatMessage model."""

    def test_valid_chat_message(self):
        """Test creating a valid ChatMessage."""
        message = ChatMessage(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"

    def test_chat_message_all_roles(self):
        """Test ChatMessage with all valid roles."""
        for role in ["system", "user", "assistant"]:
            message = ChatMessage(role=role, content="Test")
            assert message.role == role

    def test_chat_message_invalid_role(self):
        """Test ChatMessage with invalid role."""
        with pytest.raises(ValidationError) as exc_info:
            ChatMessage(role="invalid", content="Test")
        assert "role" in str(exc_info.value).lower()

    def test_chat_message_empty_content(self):
        """Test ChatMessage with empty content (should fail validation)."""
        with pytest.raises(ValidationError) as exc_info:
            ChatMessage(role="user", content="")
        assert (
            "min_length" in str(exc_info.value).lower() or "content" in str(exc_info.value).lower()
        )

    def test_chat_message_missing_fields(self):
        """Test ChatMessage with missing required fields."""
        with pytest.raises(ValidationError):
            ChatMessage(role="user")
        with pytest.raises(ValidationError):
            ChatMessage(content="Hello")

    def test_chat_message_model_dump(self):
        """Test ChatMessage model serialization."""
        message = ChatMessage(role="user", content="Hello")
        data = message.model_dump()
        assert data == {"role": "user", "content": "Hello"}

    def test_chat_message_model_dump_json(self):
        """Test ChatMessage JSON serialization."""
        message = ChatMessage(role="user", content="Hello")
        json_str = message.model_dump_json()
        assert "user" in json_str
        assert "Hello" in json_str


class TestChatRequest:
    """Test cases for ChatRequest model."""

    def test_valid_chat_request(self):
        """Test creating a valid ChatRequest."""
        request = ChatRequest(messages=[ChatMessage(role="user", content="Hello")])
        assert len(request.messages) == 1
        assert request.messages[0].role == "user"

    def test_chat_request_multiple_messages(self):
        """Test ChatRequest with multiple messages."""
        request = ChatRequest(
            messages=[
                ChatMessage(role="system", content="You are a helpful assistant"),
                ChatMessage(role="user", content="Hello"),
                ChatMessage(role="assistant", content="Hi there!"),
            ]
        )
        assert len(request.messages) == 3

    def test_chat_request_empty_messages(self):
        """Test ChatRequest with empty messages list (should fail)."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(messages=[])
        assert (
            "min_length" in str(exc_info.value).lower() or "messages" in str(exc_info.value).lower()
        )

    def test_chat_request_missing_messages(self):
        """Test ChatRequest with missing messages field."""
        with pytest.raises(ValidationError):
            ChatRequest()

    def test_chat_request_invalid_message_type(self):
        """Test ChatRequest with invalid message type."""
        with pytest.raises(ValidationError):
            ChatRequest(messages=["invalid"])

    def test_chat_request_model_dump(self):
        """Test ChatRequest model serialization."""
        request = ChatRequest(messages=[ChatMessage(role="user", content="Hello")])
        data = request.model_dump()
        assert "messages" in data
        assert len(data["messages"]) == 1


class TestChatStreamChunk:
    """Test cases for ChatStreamChunk model."""

    def test_valid_chat_stream_chunk(self):
        """Test creating a valid ChatStreamChunk."""
        chunk = ChatStreamChunk(token="Hello", trace_id="abc123", finished=False)
        assert chunk.token == "Hello"
        assert chunk.trace_id == "abc123"
        assert chunk.finished is False

    def test_chat_stream_chunk_finished(self):
        """Test ChatStreamChunk with finished flag."""
        chunk = ChatStreamChunk(token="", trace_id="abc123", finished=True)
        assert chunk.finished is True
        assert chunk.token == ""

    def test_chat_stream_chunk_missing_fields(self):
        """Test ChatStreamChunk with missing required fields."""
        with pytest.raises(ValidationError):
            ChatStreamChunk(token="Hello")
        with pytest.raises(ValidationError):
            ChatStreamChunk(trace_id="abc123")

    def test_chat_stream_chunk_model_dump(self):
        """Test ChatStreamChunk model serialization."""
        chunk = ChatStreamChunk(token="Hello", trace_id="abc123", finished=False)
        data = chunk.model_dump()
        assert data["token"] == "Hello"
        assert data["trace_id"] == "abc123"
        assert data["finished"] is False


class TestHealthResponse:
    """Test cases for HealthResponse model."""

    def test_valid_health_response(self):
        """Test creating a valid HealthResponse."""
        response = HealthResponse(status="ok", trace_id="abc123")
        assert response.status == "ok"
        assert response.trace_id == "abc123"

    def test_health_response_error_status(self):
        """Test HealthResponse with error status."""
        response = HealthResponse(status="error", trace_id="abc123")
        assert response.status == "error"

    def test_health_response_invalid_status(self):
        """Test HealthResponse with invalid status (should fail pattern validation)."""
        with pytest.raises(ValidationError):
            HealthResponse(status="invalid", trace_id="abc123")

    def test_health_response_missing_fields(self):
        """Test HealthResponse with missing required fields."""
        with pytest.raises(ValidationError):
            HealthResponse(status="ok")
        with pytest.raises(ValidationError):
            HealthResponse(trace_id="abc123")


class TestOAuthTokenResponse:
    """Test cases for OAuthTokenResponse model."""

    def test_valid_oauth_token_response(self):
        """Test creating a valid OAuthTokenResponse."""
        response = OAuthTokenResponse(access_token="token123", token_type="bearer", expires_in=3600)
        assert response.access_token == "token123"
        assert response.token_type == "bearer"
        assert response.expires_in == 3600

    def test_oauth_token_response_invalid_token_type(self):
        """Test OAuthTokenResponse with invalid token_type."""
        with pytest.raises(ValidationError):
            OAuthTokenResponse(access_token="token123", token_type="invalid", expires_in=3600)

    def test_oauth_token_response_negative_expires_in(self):
        """Test OAuthTokenResponse with negative expires_in."""
        with pytest.raises(ValidationError):
            OAuthTokenResponse(access_token="token123", token_type="bearer", expires_in=-1)

    def test_oauth_token_response_zero_expires_in(self):
        """Test OAuthTokenResponse with zero expires_in (should fail)."""
        with pytest.raises(ValidationError):
            OAuthTokenResponse(access_token="token123", token_type="bearer", expires_in=0)


class TestUserInfoResponse:
    """Test cases for UserInfoResponse model."""

    def test_valid_user_info_response(self):
        """Test creating a valid UserInfoResponse."""
        response = UserInfoResponse(user_id="user1", auth_method="oauth")
        assert response.user_id == "user1"
        assert response.auth_method == "oauth"

    def test_user_info_response_api_key_method(self):
        """Test UserInfoResponse with api_key auth_method."""
        response = UserInfoResponse(user_id="user1", auth_method="api_key")
        assert response.auth_method == "api_key"

    def test_user_info_response_invalid_auth_method(self):
        """Test UserInfoResponse with invalid auth_method."""
        with pytest.raises(ValidationError):
            UserInfoResponse(user_id="user1", auth_method="invalid")


class TestOAuthCallbackQuery:
    """Test cases for OAuthCallbackQuery model."""

    def test_valid_oauth_callback_query(self):
        """Test creating a valid OAuthCallbackQuery."""
        query = OAuthCallbackQuery(code="auth_code_123")
        assert query.code == "auth_code_123"

    def test_oauth_callback_query_empty_code(self):
        """Test OAuthCallbackQuery with empty code (should fail)."""
        with pytest.raises(ValidationError):
            OAuthCallbackQuery(code="")

    def test_oauth_callback_query_missing_code(self):
        """Test OAuthCallbackQuery with missing code field."""
        with pytest.raises(ValidationError):
            OAuthCallbackQuery()
