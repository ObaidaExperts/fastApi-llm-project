import asyncio

from app.core.tracing import get_trace_id


async def stream_chat_tokens(prompt: str):
    """
    Simulates token-by-token streaming from an LLM.
    Trace ID remains available for the entire stream.
    """
    trace_id = get_trace_id()

    tokens = prompt.split()
    for token in tokens:
        yield {
            "token": token,
            "trace_id": trace_id,
            "finished": False,
        }
        await asyncio.sleep(0.1)

    yield {
        "token": "",
        "trace_id": trace_id,
        "finished": True,
    }
