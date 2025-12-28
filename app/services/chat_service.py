import asyncio
from app.core.tracing import get_trace_id

async def generate_chat_stream(prompt: str):
    trace_id = get_trace_id()

    tokens = prompt.split()
    for token in tokens:
        # Trace ID is still available here
        yield f"[trace_id={trace_id}] {token} "
        await asyncio.sleep(0.1)
