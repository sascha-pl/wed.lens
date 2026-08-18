from typing import Annotated
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

router = APIRouter(tags=["system"])

from app.db.session import get_db
from app.services.userservice import UserService


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    success: bool


@router.post("/login", response_model=LoginUserResponse, summary="Create a new user")
def login(
        data: UserLogin,
        db: Annotated[Session, Depends(get_db)]
) -> LoginUserResponse:
    try:
        password_hasher = PasswordHasher()
        user = UserService(db).get_user(data.email)
        if user is None: return LoginUserResponse(success=False)
        password_hasher.verify(user.password_hash, data.password)
        return LoginUserResponse(success=True)
    except Argon2Error:
        return LoginUserResponse(success=False)
