from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str

router = APIRouter(tags=["system"])

@router.get("/health", response_model=HealthResponse, summary="Check API availability")
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
