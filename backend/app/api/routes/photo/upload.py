from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.photo_service import PhotoService
from app.services.storage.base import StorageService
from app.services.storage.local_db import LocalDatabaseStorageService

router = APIRouter(tags=["photos"])

class PhotoUploadResponse(BaseModel):
    id: UUID


@router.post(
    "/photo/upload",
    summary="Upload a photo",
    status_code=201,
)
async def upload_photo(
    file: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
) -> PhotoUploadResponse:
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

    size_bytes = 0

    async def content():
        nonlocal size_bytes

        while chunk := await file.read(1024 * 1024):
            size_bytes += len(chunk)
            yield chunk


    storage_object_id = await storage_service.save(
        content=content(),
    )

    photo_id = await photo_service.add(
        id=storage_object_id,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        uploaded_by_user_id=user.id,
    )

    db.commit()

    return PhotoUploadResponse(
        id = photo_id
    )