from dishka import AsyncContainer, Scope, make_async_container, provide

from core.ioc import MyProvider
from gateways.repositories.memory import (
    MemoryHouseRepository,
    MemoryResidentRepository,
    MemoryUserRepository,
)
from domain.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    UserRepository,
)
from domain.interfaces.uow import AsyncUnitOfWork
from gateways.repositories.memory.base import MemoryStorage


class DummySession:
    async def commit(self):
        pass

    async def rollback(self):
        pass


class DummyProvider(MyProvider):

    @provide
    async def get_uow(self) -> AsyncUnitOfWork:
        return DummySession()

    @provide(scope=Scope.APP)
    async def get_memory_storage(self) -> MemoryStorage:
        print("get_memory_storage")
        return MemoryStorage()

    @provide
    async def get_user_repository(self, storage: MemoryStorage) -> UserRepository:
        return MemoryUserRepository(storage=storage)

    @provide
    async def get_house_repository(self, storage: MemoryStorage) -> HouseRepository:
        return MemoryHouseRepository(storage=storage)

    @provide
    async def get_resident_repository(
        self, storage: MemoryStorage
    ) -> ResidentRepository:
        return MemoryResidentRepository(storage=storage)


def init_dummy_container() -> AsyncContainer:
    return make_async_container(DummyProvider())
