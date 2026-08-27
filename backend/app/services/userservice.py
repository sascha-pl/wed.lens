import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_session import UserSession

SESSION_EXPIRY = timedelta(days=180)

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

    def get_user_from_session(
        self,
        session_key: str,
    ) -> User | None:
        statement = (
            select(User)
            .join(
                UserSession,
                UserSession.user_id == User.id,
            )
            .where(UserSession.session_key == session_key)
        )

        return self.db_session.scalar(statement)

    def create_session(self, user: User) -> UserSession:
        session = UserSession(
            session_key=secrets.token_hex(32),
            user_id=user.id,
        )

        self.db_session.add(session)
        self.db_session.flush()
        self.db_session.refresh(session)

        return session

    def touch_session(self, user: User) -> None:
        statement = (
            update(UserSession).where(UserSession.user_id == user.id).values(date_last_used=datetime.now())
        )

        self.db_session.execute(statement)
        self.db_session.commit()

    def delete_session(self, session_key: str) -> None:
        statement = delete(UserSession).where(
            UserSession.session_key == session_key
        )

        self.db_session.execute(statement)
        self.db_session.commit()

    def cleanup(self) -> None:
        #Delete expired sessions
        expiry_cutoff = datetime.now(timezone.utc) - SESSION_EXPIRY

        statement = (
            delete(UserSession)
            .where(UserSession.date_last_used < expiry_cutoff)
        )

        self.db_session.execute(statement)
        self.db_session.commit()