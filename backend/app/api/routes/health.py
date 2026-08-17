from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["system"])


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse, summary="Check API availability")
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
