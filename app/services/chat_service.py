import asyncio
from typing import AsyncGenerator

async def generate_chat_stream(
    prompt: str,
) -> AsyncGenerator[str, None]:
    """
    Simulates token-by-token streaming.
    Replace with real LLM streaming logic.
    """
    tokens = prompt.split()
    for token in tokens:
        yield token + " "
        await asyncio.sleep(0.1)
