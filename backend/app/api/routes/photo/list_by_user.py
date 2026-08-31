from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.routes.photo import PhotoResponse
from app.db.session import get_db
from app.models.user import User
from app.services.photo_service import PhotoService

router = APIRouter(tags=["photos"])

@router.get(
    "/photo",
    summary="List user's photos",
    response_model=list[PhotoResponse],
)
async def list_photos(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
) -> list[PhotoResponse]:
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )
    photo_service = PhotoService(
        db_session=db
    )

    photos = await photo_service.list_by_user(
        user_id=user.id,
    )

    return [
        PhotoResponse.model_validate(photo)
        for photo in photos
    ]