"""Album Endpoint modules."""

from fastapi import APIRouter

router = APIRouter(tags=["album"])

__all__ = ["router"]