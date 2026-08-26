from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.userservice import UserService
from app.models.user import User


router = APIRouter(tags=["system"])


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    authenticated: bool


@router.post(
    "/login",
    response_model=LoginUserResponse,
    summary="Login a user and create a session",
)
def login(
    data: UserLogin,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> LoginUserResponse:
    password_hasher = PasswordHasher()
    user_service = UserService(db)

    user: User | None = user_service.get_user(data.email)

    if user is None:
        return LoginUserResponse(authenticated=False)

    try:
        password_hasher.verify(user.password_hash, data.password)
    except Argon2Error:
        return LoginUserResponse(authenticated=False)

    session = user_service.create_session(user)

    from app.core import config
    response.set_cookie(
        key="session_key",
        value=session.session_key,
        httponly=True,
        secure= config.get_settings().app_env != 'local',
        samesite="lax",
        max_age=60 * 60 * 24 * 180,
    )

    return LoginUserResponse(authenticated=True)