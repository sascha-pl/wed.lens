from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.photo_service import PhotoService

router = APIRouter(tags=["photo"])

@router.delete(
    "/photo/{photo_id}",
    summary="Delete photo",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_photo(
    photo_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
) -> Response:
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    photo_service = PhotoService(
        db_session=db,
    )

    photo = await photo_service.delete(id=photo_id)

    if photo is None:
        raise HTTPException(
            status_code=404,
            detail="Photo not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)