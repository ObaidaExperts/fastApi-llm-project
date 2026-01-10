import uuid
from contextvars import ContextVar

trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)


def generate_trace_id() -> str:
    return str(uuid.uuid4())


def set_trace_id(trace_id: str):
    trace_id_ctx.set(trace_id)


def get_trace_id() -> str | None:
    return trace_id_ctx.get()
