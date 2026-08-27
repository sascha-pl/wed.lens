from typing import Annotated

from fastapi import APIRouter, Cookie, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.userservice import UserService


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
    session_key: str | None = Cookie(default=None),
) -> InitializeResponse:
    if session_key is None:
        return InitializeResponse(authenticated=False)

    user_service = UserService(db)

    user = user_service.get_user_from_session(session_key)

    if user is None:
        return InitializeResponse(authenticated=False)

    user_service.touch_session(user)

    return InitializeResponse(
        authenticated=True,
        user=AppUser(
            name=user.name,
            email=user.email,
        ),
    )