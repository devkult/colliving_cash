from faker import Faker
import pytest

from domain.logic.commands.house import CreateHouseCommand, JoinHouseCommand
from domain.logic.commands.user import CreateUserCommand
from domain.logic.exceptions.colliving import (
    HouseNotFoundException,
    UserAlreadyJoinedHouseException,
    UserNotFoundException,
)
from domain.logic.interfaces.repository import HouseRepository
from domain.logic.mediator import Mediator
from domain.logic.queries.house import GetHouseQuery, GetHouseResidentsQuery


@pytest.mark.asyncio
async def test_create_user(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    assert user


@pytest.mark.asyncio
async def test_create_house(
    mediator: Mediator, faker: Faker, house_repository: HouseRepository
) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    assert house
    assert house.owner_id == user.oid
    assert await house_repository.get_by_uuid(house.oid)


@pytest.mark.asyncio
async def test_create_house_with_non_existing_user(
    mediator: Mediator, faker: Faker
) -> None:
    with pytest.raises(UserNotFoundException):
        await mediator.handle_command(
            CreateHouseCommand(name=faker.name(), owner_uuid=faker.uuid4())
        )


@pytest.mark.asyncio
async def test_join_house(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    resident, *_ = await mediator.handle_command(
        JoinHouseCommand(house_uuid=house.oid, user_uuid=user.oid)
    )
    assert resident
    assert resident.user_id == user.oid
    assert resident.house_id == house.oid


@pytest.mark.asyncio
async def test_join_non_existing_house(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    with pytest.raises(HouseNotFoundException):
        await mediator.handle_command(
            JoinHouseCommand(house_uuid=faker.uuid4(), user_uuid=user.oid)
        )


@pytest.mark.asyncio
async def test_join_non_existing_user(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    with pytest.raises(UserNotFoundException):
        await mediator.handle_command(
            JoinHouseCommand(house_uuid=house.oid, user_uuid=faker.uuid4())
        )


@pytest.mark.asyncio
async def test_join_already_joined_house(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    resident, *_ = await mediator.handle_command(
        JoinHouseCommand(house_uuid=house.oid, user_uuid=user.oid)
    )
    with pytest.raises(UserAlreadyJoinedHouseException):
        await mediator.handle_command(
            JoinHouseCommand(house_uuid=house.oid, user_uuid=user.oid)
        )


@pytest.mark.asyncio
async def test_get_house_residents(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    resident, *_ = await mediator.handle_command(
        JoinHouseCommand(house_uuid=house.oid, user_uuid=user.oid)
    )
    residents = await mediator.handle_query(
        GetHouseResidentsQuery(house_uuid=house.oid)
    )
    assert resident in residents


@pytest.mark.asyncio
async def test_get_non_existing_house_residents(
    mediator: Mediator, faker: Faker
) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    with pytest.raises(HouseNotFoundException):
        await mediator.handle_query(GetHouseResidentsQuery(house_uuid=faker.uuid4()))


@pytest.mark.asyncio
async def test_get_house(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    assert await mediator.handle_query(GetHouseQuery(house_uuid=house.oid))


@pytest.mark.asyncio
async def test_get_non_existing_house(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    with pytest.raises(HouseNotFoundException):
        await mediator.handle_query(GetHouseQuery(house_uuid=faker.uuid4()))
