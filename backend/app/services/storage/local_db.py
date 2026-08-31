from collections.abc import AsyncIterator
from uuid import UUID

from sqlalchemy import delete, exists, select

from app.db.session import Session
from app.models.storage_object import StorageObject


# we will probably need streaming capabilities for remote storage solutions, so here:
async def _content_stream(content: bytes) -> AsyncIterator[bytes]:
    yield content

class LocalDatabaseStorageService:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    async def save(
        self,
        *,
        content: AsyncIterator[bytes],
    ) -> UUID:
        chunks: list[bytes] = []

        async for chunk in content:
            chunks.append(chunk)

        data = b"".join(chunks)

        storage_object = StorageObject(
            content = data
        )
        
        self.db_session.add(storage_object)
        self.db_session.flush()

        return storage_object.id
        
    async def get(
        self,
        *,
        id: UUID,
    ) -> AsyncIterator[bytes] | None:
        storage_object = self.db_session.scalar(
            select(StorageObject).where(StorageObject.id == id)
        )
        
        if storage_object is None:
            return None

        return _content_stream(storage_object.content)

    async def delete(
        self,
        *,
        id: UUID,
    ) -> bool:
        result = self.db_session.execute(
            delete(StorageObject)
            .where(StorageObject.id == id)
            .returning(StorageObject.id)
        )

        return result.scalar_one_or_none() is not None

    async def exists(
        self,
        *,
        id: UUID,
    ) -> bool:
        return self.db_session.scalar(
            select(
                exists().where(StorageObject.id == id)
            )
        ) is True

    def cleanUp(
        self
    ) -> None:
        return #TODO remove zombies