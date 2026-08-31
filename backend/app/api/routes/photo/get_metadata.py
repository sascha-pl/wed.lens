from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.routes.photo import PhotoResponse
from app.db.session import get_db
from app.models.user import User
from app.services.photo_service import PhotoService

router = APIRouter(tags=["photos"])

@router.get(
    "/photo/{photo_id}",
    summary="Get photo metdata",
)
async def get_photo_metadata(
    photo_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
) -> PhotoResponse:
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )
    photo_service = PhotoService(
        db_session=db,
    )

    photo = await photo_service.get(id=photo_id)

    if photo is None:
        raise HTTPException(
            status_code=404,
            detail="Photo not found",
        )

    return PhotoResponse.model_validate(photo)