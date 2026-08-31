"""Photo Endpoint modules."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PhotoResponse(BaseModel):
    id: UUID
    content_type: str
    size_bytes: int
    uploaded_by_user_id: UUID
    date_created: datetime

    model_config = ConfigDict(from_attributes=True)

__all__ = ["PhotoResponse"]