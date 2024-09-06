from dataclasses import dataclass, field
from typing import Optional

from domain.entities.colliving import User
from domain.interfaces.repository import UserRepository
from gateways.repositories.memory.base import MemoryRepository


class MemoryUserRepository(MemoryRepository,UserRepository):
    def __init__(self, storage) -> None:
        super().__init__(storage=storage)
        self.users: list[User] = self.storage.create_table([], "users")


    async def add(self, user: User) -> User:
        self.users.append(user)
        return user

    async def get_by_uuid(self, uuid: str) -> Optional[User]:
        for user in self.users:
            if user.oid == uuid:
                return user
        return None
