from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter(tags=["system"])


class AppUser(BaseModel):
    name: str
    email: EmailStr


class InitializeResponse(BaseModel):
    authenticated: bool
    user: AppUser | None = None


@router.get(
    "/initialize",
    response_model=InitializeResponse,
    summary="Initialize the application session",
)
def initialize(
    *,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
) -> InitializeResponse:

    if user is None:
        return InitializeResponse(authenticated=False)

    user_service = UserService(db)
    user_service.touch_session(user)

    return InitializeResponse(
        authenticated=True,
        user=AppUser(
            name=user.name,
            email=user.email,
        ),
    )