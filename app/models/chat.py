from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in a chat conversation."""

    role: Literal["system", "user", "assistant"] = Field(
        ...,
        description="The role of the message sender",
        examples=["user"],
    )
    content: str = Field(
        ...,
        description="The content of the message",
        examples=["Hello, how are you?"],
        min_length=1,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"role": "user", "content": "What is the weather today?"},
                {"role": "assistant", "content": "I'm an AI assistant..."},
            ]
        }
    }


class ChatRequest(BaseModel):
    """Request model for chat streaming endpoint."""

    messages: list[ChatMessage] = Field(
        ...,
        description="List of messages in the conversation",
        min_length=1,
        examples=[
            [
                {"role": "user", "content": "Hello, how are you?"},
            ]
        ],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {"role": "user", "content": "Tell me a joke"},
                    ]
                }
            ]
        }
    }


class ChatStreamChunk(BaseModel):
    """A single chunk in the streaming chat response."""

    token: str = Field(
        ...,
        description="The token/chunk of text being streamed",
        examples=["Hello"],
    )
    trace_id: str = Field(
        ...,
        description="Unique trace ID for this request",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )
    finished: bool = Field(
        ...,
        description="Whether this is the final chunk in the stream",
        examples=[False],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"token": "Hello", "trace_id": "abc123", "finished": False},
                {"token": "", "trace_id": "abc123", "finished": True},
            ]
        }
    }
