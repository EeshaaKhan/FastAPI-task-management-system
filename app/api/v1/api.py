"""
API v1 router aggregation.
"""
from fastapi import APIRouter

from app.api.v1 import tasks, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(tasks.router, tags=["tasks"])
