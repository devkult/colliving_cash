from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.colliving import House, Resident, User


class HouseRepository(ABC):
    @abstractmethod
    async def add(self, home: House) -> House: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[House]: ...


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[User]: ...


class ResidentRepository(ABC):
    @abstractmethod
    async def add(self, resident: Resident) -> Resident: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[Resident]: ...

    @abstractmethod
    async def get_by_house_uuid(self, house_uuid: str) -> list[Resident]: ...

    @abstractmethod
    async def get_by_user_and_house_uuid(
        self, user_uuid: str, house_uuid: str
    ) -> Optional[Resident]: ...
