from fastapi import APIRouter
from api.v1.dota import router as dota_router

api_router = APIRouter()

api_router.include_router(dota_router, prefix="/570")
