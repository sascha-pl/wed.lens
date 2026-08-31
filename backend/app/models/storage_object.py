import uuid

from sqlalchemy import LargeBinary, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StorageObject(Base):
    __tablename__ = "storage_object"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    content: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )
