import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    date_last_used: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )