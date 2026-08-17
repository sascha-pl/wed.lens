from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.models.user import User


class UserService(BaseModel):
    def __init__(self, session: Session):
        self.session = session

    async def create_user(
        self,
        name: str,
        email: EmailStr,
        password_hash: str,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
        )

        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)

        return user