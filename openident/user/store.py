from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from openident.user import User


class UserStore(ABC):
    @abstractmethod
    async def create_user(self, name: str) -> User:
        pass

    @abstractmethod
    async def get_user(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def get_users(
        self, limit: Optional[int], offset: Optional[int]
    ) -> list[User]:
        pass

    @abstractmethod
    async def update_user(self, user_id: UUID, *, name: Optional[str]) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        pass
