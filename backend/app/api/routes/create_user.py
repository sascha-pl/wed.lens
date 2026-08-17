from typing import Annotated
from argon2 import PasswordHasher
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

router = APIRouter(tags=["system"])

from app.db.session import get_db
from app.services.userservice import UserService


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    success: bool


@router.post("/create_user", response_model=CreateUserResponse, summary="Create a new user")
def create_user(
        data: UserCreate,
        db: Annotated[Session, Depends(get_db)]
) -> CreateUserResponse:
    try:
        password_hasher = PasswordHasher()
        UserService(db).create_user(data.name, data.email, password_hasher.hash(data.password),)
        db.commit()
        return CreateUserResponse(success=True)
    except:
        db.rollback()
        return CreateUserResponse(success=False)
    finally:
        db.close()
