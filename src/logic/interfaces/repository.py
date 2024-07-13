from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.colliving import House, Resident, Room, User


class IHouseRepository(ABC):
    @abstractmethod
    async def create(self, home: House) -> House: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[House]: ...


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[User]: ...


class IRoomRepository(ABC):
    @abstractmethod
    async def create(self, room: Room) -> Room: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[Room]: ...


class IResidentRepository(ABC):
    @abstractmethod
    async def create(self, resident: Resident) -> Resident: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[Resident]: ...
