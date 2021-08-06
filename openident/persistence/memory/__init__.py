from contextlib import suppress
from datetime import datetime
from secrets import token_urlsafe
from typing import Optional
from uuid import UUID, uuid4

from openident.client import Client
from openident.client.store import ClientStore
from openident.user import User
from openident.user.store import UserStore


class MemoryUserStore(UserStore):
    users: dict[UUID, User]

    def __init__(self) -> None:
        self.users = {}

    async def create_user(self, name: str) -> User:
        user = User(id=uuid4(), name=name, created_at=datetime.now())
        self.users[user.id] = user
        return user

    async def update_user(self, user_id: UUID, *, name: Optional[str]) -> User:
        user = await self.get_user(user_id)
        if name is not None:
            user.name = name
        return user

    async def get_user(self, user_id: UUID) -> User:
        return self.users[user_id]

    async def get_users(
        self, limit: Optional[int], offset: Optional[int]
    ) -> list[User]:
        if limit is None:
            limit = len(self.users)
        offset = offset or 0
        return [
            user
            for user in sorted(self.users.values(), key=lambda user: user.created_at)
        ][offset : limit + offset]

    async def delete_user(self, user_id: UUID) -> None:
        with suppress(KeyError):
            del self.users[user_id]


class MemoryClientStore(ClientStore):
    """
    MemoryPersister is a basic implementation of a ClientStore.
    As it does not actually persist any data
    its purpose is for unit testing and serving as a reference implementation
    """

    clients: dict[UUID, Client]

    def __init__(self) -> None:
        self.clients = {}

    async def create_client(
        self,
        name: str,
        scope: Optional[list[str]] = None,
        redirect_uris: Optional[list[str]] = None,
    ) -> Client:
        client = Client(
            id=uuid4(),
            name=name,
            secret=token_urlsafe(40),
            scope=scope or [],
            redirect_uris=redirect_uris or [],
            created_at=datetime.now(),
        )
        self.clients[client.id] = client
        return client

    async def update_client(
        self,
        client_id: UUID,
        name: Optional[str] = None,
        scope: Optional[list[str]] = None,
        redirect_uris: Optional[list[str]] = None,
    ) -> Client:
        client = await self.get_client(client_id)
        if name is not None:
            client.name = name
        if scope is not None:
            client.scope = scope
        if redirect_uris is not None:
            client.redirect_uris = redirect_uris
        return client

    async def get_client(self, client_id: UUID) -> Client:
        return self.clients[client_id]

    async def get_clients(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[Client]:
        if limit is None:
            limit = len(self.clients)
        offset = offset or 0
        return [
            client
            for client in sorted(
                self.clients.values(), key=lambda client: client.created_at
            )
        ][offset : limit + offset]

    async def delete_client(self, client_id: UUID) -> None:
        with suppress(KeyError):
            del self.clients[client_id]
