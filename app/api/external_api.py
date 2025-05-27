from api.external.chat import router as chat_router
from fastapi import APIRouter

api_router = APIRouter()

# External
api_router.include_router(chat_router, tags=["external_chat"])
