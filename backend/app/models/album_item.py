import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AlbumItem(Base):
    __tablename__ = "album_item"

    album_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("album.id", ondelete="CASCADE"),
        primary_key=True,
    )
    photo_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("photo.id", ondelete="CASCADE"),
        primary_key=True,
    )
    date_added: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    added_by_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))