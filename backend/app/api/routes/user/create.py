from typing import Annotated

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core import config
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter(tags=["user"])
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    authenticated: bool


@router.post(
    "/user/create",
    response_model=UserCreateResponse,
    summary="Create a new user and create a session",
)
def create_user(
    data: UserCreate,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> UserCreateResponse:
    try:
        password_hasher = PasswordHasher()
        user_service = UserService(db)

        user: User = user_service.create_user(
            data.name,
            data.email,
            password_hasher.hash(data.password),
        )

        session = user_service.create_session(user)

        db.commit()

        response.set_cookie(
            key="session_key",
            value=session.session_key,
            httponly=True,
            secure= config.get_settings().app_env != 'local',
            samesite="lax",
            max_age=60 * 60 * 24 * 180,
        )

        return UserCreateResponse(authenticated=True)

    except Exception:  # noqa: BLE001
        db.rollback()
        return UserCreateResponse(authenticated=False)