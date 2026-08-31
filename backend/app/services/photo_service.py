from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.photo import Photo
from app.services.storage.base import StorageService


class PhotoService:
    def __init__(
        self,
        *,
        db_session: Session
    ):
        self.db_session = db_session

    async def add(
        self,
        *,
        id: UUID,
        content_type: str,
        size_bytes: int,
        uploaded_by_user_id: UUID,
    ) -> UUID:
        photo = Photo(
            id=id,
            content_type=content_type,
            size_bytes=size_bytes,
            uploaded_by_user_id=uploaded_by_user_id,
        )

        self.db_session.add(photo)
        self.db_session.flush()

        return photo.id

    async def delete(
        self,
        *,
        id: UUID,
    ) -> Photo | None:
        photo = await self.get(id=id)

        if photo is None:
            return None

        photo.is_deleted = True
        self.db_session.commit()

        return photo

    async def get(
        self,
        *,
        id: UUID,
    ) -> Photo | None:
        return self.db_session.scalar(
            select(Photo).where(Photo.id == id, Photo.is_deleted.is_(False))
        )

    async def list_by_user(
        self,
        *,
        user_id: UUID,
    ) -> list[Photo]:
        return list(
            self.db_session.scalars(
                select(Photo)
                .where(Photo.uploaded_by_user_id == user_id, Photo.is_deleted.is_(False))
                .order_by(Photo.date_created.desc())
            )
        )

    def cleanUp(
            self,
            *,
            storage_service: StorageService,
        ) -> None:
        #Delete expired sessions
        for photo in self.db_session.scalars(
            select(Photo)
            .where(Photo.is_deleted.is_(True))
        ):
            if storage_service.delete(id=photo.id):
                self.db_session.delete(photo)
                self.db_session.flush()
