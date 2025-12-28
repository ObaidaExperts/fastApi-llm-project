from fastapi import FastAPI
from app.api.router import api_router
from app.middleware.tracing import TracingMiddleware

app = FastAPI(title="AI Chat Service")

app.add_middleware(TracingMiddleware)
app.include_router(api_router, prefix="/api")
