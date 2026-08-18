from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(
        self,
        name: str,
        email: str,
        password_hash: str,
    ) -> User:
        existing_user = self.db_session.scalar(
            select(User).where(User.email == email)
        )

        if existing_user is not None:
            raise ValueError("Email already exists")

        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
        )

        self.db_session.add(user)
        self.db_session.flush()
        self.db_session.refresh(user)

        return user

    def get_user(
            self,
            email: str
    ) -> User | None:
        return self.db_session.scalar(
            select(User).where(User.email == email)
        )