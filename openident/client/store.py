from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from openident.client import Client


class ClientStore(ABC):
    @abstractmethod
    async def create_client(
        self,
        name: str,
        scope: Optional[list[str]] = None,
        redirect_uris: Optional[list[str]] = None,
    ) -> Client:
        pass

    @abstractmethod
    async def get_client(self, client_id: UUID) -> Client:
        pass

    @abstractmethod
    async def get_clients(
        self, limit: Optional[int], offset: Optional[int]
    ) -> list[Client]:
        pass

    @abstractmethod
    async def update_client(
        self,
        client_id: UUID,
        *,
        name: Optional[str],
        scope: Optional[list[str]],
        redirect_uris: list[str],
    ) -> Client:
        pass

    @abstractmethod
    async def delete_client(self, client_id: UUID) -> None:
        pass
