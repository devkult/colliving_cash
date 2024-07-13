from dataclasses import dataclass, field
from typing import Optional

from domain.entities.colliving import User
from logic.interfaces.repository import UserRepository


class MemoryUserRepository(UserRepository):
    users: list[User] = []

    async def create(self, user: User) -> User:
        self.users.append(user)
        return user

    async def get_by_uuid(self, uuid: str) -> Optional[User]:
        for user in self.users:
            if user.oid == uuid:
                return user
        return None
