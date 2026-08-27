from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.userservice import UserService


router = APIRouter(tags=["system"])


@router.post("/user/logout")
def logout(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    session_key: str | None = Cookie(default=None),
) -> dict[str, bool]:
    if session_key is not None:
        UserService(db).delete_session(session_key)

    response.delete_cookie(
        key="session_key",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return {"authenticated": False}