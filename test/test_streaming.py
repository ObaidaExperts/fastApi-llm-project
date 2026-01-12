"""
Unit tests for streaming behavior.
"""
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.chat import ChatStreamChunk
from app.services.chat_service import stream_chat_tokens


class TestStreamingService:
    """Test cases for chat streaming service."""

    @pytest.mark.asyncio
    async def test_stream_chat_tokens_basic(self):
        """Test basic streaming functionality."""
        prompt = "Hello world"
        chunks = []
        async for chunk in stream_chat_tokens(prompt):
            chunks.append(chunk)

        assert len(chunks) > 0
        assert chunks[-1]["finished"] is True
        assert chunks[-1]["token"] == ""

    @pytest.mark.asyncio
    async def test_stream_chat_tokens_structure(self):
        """Test that stream chunks have correct structure."""
        prompt = "Test message"
        async for chunk in stream_chat_tokens(prompt):
            # Validate chunk structure matches ChatStreamChunk model
            assert "token" in chunk
            assert "trace_id" in chunk
            assert "finished" in chunk
            assert isinstance(chunk["finished"], bool)
            # Only validate with model if trace_id is not None
            if chunk["trace_id"] is not None:
                chunk_model = ChatStreamChunk(**chunk)
                assert chunk_model.trace_id == chunk["trace_id"]

    @pytest.mark.asyncio
    async def test_stream_chat_tokens_trace_id_consistency(self):
        """Test that trace_id remains consistent throughout stream."""
        prompt = "Hello world test"
        trace_ids = set()
        async for chunk in stream_chat_tokens(prompt):
            trace_ids.add(chunk["trace_id"])

        # All chunks should have the same trace_id
        assert len(trace_ids) == 1

    @pytest.mark.asyncio
    async def test_stream_chat_tokens_final_chunk(self):
        """Test that final chunk has finished=True and empty token."""
        prompt = "Test"
        chunks = []
        async for chunk in stream_chat_tokens(prompt):
            chunks.append(chunk)

        final_chunk = chunks[-1]
        assert final_chunk["finished"] is True
        assert final_chunk["token"] == ""

    @pytest.mark.asyncio
    async def test_stream_chat_tokens_empty_prompt(self):
        """Test streaming with empty prompt."""
        prompt = ""
        chunks = []
        async for chunk in stream_chat_tokens(prompt):
            chunks.append(chunk)

        # Should still produce at least the final chunk
        assert len(chunks) >= 1
        assert chunks[-1]["finished"] is True


class TestStreamingEndpoint:
    """Test cases for streaming endpoint behavior."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def chat_request_payload(self):
        """Create chat request payload."""
        return {"messages": [{"role": "user", "content": "Hello"}]}

    def test_streaming_response_format(self, client, chat_request_payload):
        """Test that streaming response follows SSE format."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json=chat_request_payload,
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        # Check that response contains SSE format
        content = response.text
        assert "data:" in content

    def test_streaming_response_chunks(self, client, chat_request_payload):
        """Test that streaming response contains multiple chunks."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json=chat_request_payload,
        )
        assert response.status_code == 200

        content = response.text
        # Count data: lines (each chunk)
        data_lines = [line for line in content.split("\n") if line.startswith("data:")]
        assert len(data_lines) > 0

    def test_streaming_response_json_format(self, client, chat_request_payload):
        """Test that each chunk is valid JSON."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json=chat_request_payload,
        )
        assert response.status_code == 200

        content = response.text
        for line in content.split("\n"):
            if line.startswith("data:"):
                json_str = line.replace("data:", "").strip()
                if json_str:
                    # Should be valid JSON
                    chunk_data = json.loads(json_str)
                    assert "token" in chunk_data
                    assert "trace_id" in chunk_data
                    assert "finished" in chunk_data

    def test_streaming_response_headers(self, client, chat_request_payload):
        """Test that streaming response has correct headers."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json=chat_request_payload,
        )
        assert response.status_code == 200
        assert "Cache-Control" in response.headers
        assert response.headers["Cache-Control"] == "no-cache"
        assert "Connection" in response.headers
        assert response.headers["Connection"] == "keep-alive"

    def test_streaming_response_auth_headers(self, client, chat_request_payload):
        """Test that streaming response includes auth headers."""
        response = client.post(
            "/api/v1/chat/stream",
            headers={"X-API-Key": "test-api-key-123"},
            json=chat_request_payload,
        )
        assert response.status_code == 200
        assert "X-Auth-Method" in response.headers
        assert "X-User-ID" in response.headers

    def test_streaming_with_different_messages(self, client):
        """Test streaming with different message content."""
        test_cases = [
            {"messages": [{"role": "user", "content": "Short"}]},
            {
                "messages": [
                    {"role": "user", "content": "This is a longer message with multiple words"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "You are helpful"},
                    {"role": "user", "content": "Hello"},
                ]
            },
        ]

        for payload in test_cases:
            response = client.post(
                "/api/v1/chat/stream",
                headers={"X-API-Key": "test-api-key-123"},
                json=payload,
            )
            assert response.status_code == 200
            assert "data:" in response.text
