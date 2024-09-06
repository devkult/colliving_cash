from dishka import AsyncContainer
from faker import Faker
from pytest import fixture

from domain.logic.mediator import Mediator
from domain.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    UserRepository,
)
from .fixtures import init_dummy_container


@fixture()
async def faker() -> Faker:
    return Faker()


@fixture(scope="session")
def container() -> AsyncContainer:
    return init_dummy_container()


@fixture()
async def mediator(container: AsyncContainer) -> Mediator:
    mediator = await container.get(Mediator)
    return mediator


@fixture()
async def user_repository(container: AsyncContainer) -> UserRepository:
    async with container() as container_r:
        return await container_r.get(UserRepository)


@fixture()
async def house_repository(container: AsyncContainer) -> HouseRepository:
    async with container() as container_r:
        return await container_r.get(HouseRepository)


@fixture()
async def house_repo(container: AsyncContainer) -> ResidentRepository:
    async with container() as container_r:
        return await container_r.get(ResidentRepository)
