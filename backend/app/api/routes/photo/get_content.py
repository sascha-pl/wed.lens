from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.photo_service import PhotoService
from app.services.storage.base import StorageService
from app.services.storage.local_db import LocalDatabaseStorageService

router = APIRouter(tags=["photo"])

@router.get(
    "/photo/{photo_id}/content",
    summary="Get photo content",
)
async def get_photo_content(
    photo_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
) -> StreamingResponse:
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )
    storage_service: StorageService = LocalDatabaseStorageService(
        db_session=db,
    )

    photo_service = PhotoService(
        db_session=db
    )

    photo = await photo_service.get(id=photo_id)

    if photo is None:
        raise HTTPException(
            status_code=404,
            detail="Photo not found",
        )

    content = await storage_service.get(id=photo_id)

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Photo content not found",
        )

    return StreamingResponse(
        content,
        media_type=photo.content_type,
    )