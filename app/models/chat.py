from pydantic import BaseModel, Field
from typing import List, Literal

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    stream: bool = Field(default=True)

class ChatChunk(BaseModel):
    content: str
    finished: bool = False
