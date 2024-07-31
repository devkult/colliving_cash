from dishka import AsyncContainer, make_async_container, provide

from config.ioc import MyProvider
from gateways.repositories.memory import (
    MemoryHouseRepository,
    MemoryResidentRepository,
    MemoryRoomRepository,
    MemoryUserRepository,
)
from logic.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    RoomRepository,
    UserRepository,
)
from logic.interfaces.uow import AsyncUnitOfWork


class DummySession:
    async def commit(self):
        pass

    async def rollback(self):
        pass


class DummyProvider(MyProvider):

    @provide
    async def get_uow(self) -> AsyncUnitOfWork:
        return DummySession()

    @provide
    async def get_user_repository(self) -> UserRepository:
        return MemoryUserRepository()

    @provide
    async def get_house_repository(self) -> HouseRepository:
        return MemoryHouseRepository()

    @provide
    async def get_room_repository(self) -> RoomRepository:
        return MemoryRoomRepository()

    @provide
    async def get_resident_repository(self) -> ResidentRepository:
        return MemoryResidentRepository()


def init_dummy_container() -> AsyncContainer:
    return make_async_container(DummyProvider())
