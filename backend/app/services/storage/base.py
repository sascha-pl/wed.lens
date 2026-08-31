from collections.abc import AsyncIterator
from typing import Protocol
from uuid import UUID


class StorageService(Protocol):
    async def save(
        self,
        *,
        content: AsyncIterator[bytes],
    ) -> UUID:
        ...

    async def get(
        self,
        *,
        id: UUID,
    ) -> AsyncIterator[bytes] | None:
        ...

    async def delete(
        self,
        *,
        id: UUID,
    ) -> bool:
        ...

    async def exists(
        self,
        *,
        id: UUID,
    ) -> bool:
        ...

    def cleanUp(
        self,
    ) -> None:
        ...