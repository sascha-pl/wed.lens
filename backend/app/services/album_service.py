from uuid import UUID

from app.models.album import Album
from app.models.album_item import AlbumItem
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.photo import Photo


class AlbumService:
    def __init__(
        self,
        *,
        db_session: Session,
    ):
        self.db_session = db_session

    async def add(
        self,
        *,
        name: str,
        owner_user_id: UUID,
    ) -> UUID:
        album = Album(
            name=name,
            owner_user_id=owner_user_id,
        )

        self.db_session.add(album)
        self.db_session.flush()

        return album.id

    async def delete(
        self,
        *,
        id: UUID,
    ) -> None:
        album = self.db_session.get(Album, id)

        if album is None:
            return
        
        self.db_session.delete(album)
        self.db_session.flush()

    async def get(
        self,
        *,
        id: UUID,
    ) -> Album | None:
        return self.db_session.scalar(
            select(Album).where(Album.id == id)
        )

    async def list_photos(
        self,
        *,
        album_id: UUID,
    ) -> list[Photo]:
        return list(
            self.db_session.scalars(
                select(Photo)
                .join(
                    AlbumItem,
                    AlbumItem.photo_id == Photo.id,
                )
                .where(AlbumItem.album_id == album_id)
                .order_by(AlbumItem.date_added.asc())
            )
        )

    async def add_photo(
        self,
        *,
        album_id: UUID,
        photo_id: UUID,
        added_by_user_id: UUID,
    ) -> None:
        album_item = AlbumItem(
            album_id=album_id,
            photo_id=photo_id,
            added_by_user_id=added_by_user_id,
        )

        self.db_session.add(album_item)
        self.db_session.flush()

    async def remove_photo(
        self,
        *,
        album_id: UUID,
        photo_id: UUID,
    ) -> None:
        self.db_session.execute(
            delete(AlbumItem).where(
                AlbumItem.album_id == album_id,
                AlbumItem.photo_id == photo_id,
            )
        )
        self.db_session.flush()