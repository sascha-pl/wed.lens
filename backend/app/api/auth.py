from typing import Annotated

from fastapi import Cookie, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    session_key: Annotated[str | None, Cookie()] = None,
) -> User | None:
    if session_key is None:
        return None

    user = UserService(db).get_user_from_session(session_key)

    return user