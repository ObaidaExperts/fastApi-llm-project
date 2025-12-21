from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.chat import router as chat_router

router = APIRouter(prefix="/v1")

router.include_router(health_router, tags=["health"])
router.include_router(chat_router, tags=["chat"])
