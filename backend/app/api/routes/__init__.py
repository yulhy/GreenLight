# backend/app/api/routes/__init__.py

from app.api.routes.chat import router as chat_router
from app.api.routes.plans import router as plans_router

__all__ = [
    "chat_router",
    "plans_router",
]
