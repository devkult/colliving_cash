from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.colliving import House, User


class IHouseRepository(ABC):
    @abstractmethod
    async def create(self, home: House) -> House:
        ...
    
class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        ...
    
    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[User]:
        ...
