from faker import Faker
import pytest

from domain.logic.commands.colliving import (
    CreateHouseCommand,
    CreateRoomCommand,
    CreateUserCommand,
    JoinRoomCommand,
)
from domain.logic.exceptions.colliving import (
    HouseNotFoundException,
    UserNotFoundException,
    RoomNotFoundException,
    RoomIsFullException,
    UserAlreadyInRoomException,
)
from domain.logic.interfaces.repository import HouseRepository, ResidentRepository
from domain.logic.mediator import Mediator


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
async def test_create_room(
    mediator: Mediator, faker: Faker, room_repository: HouseRepository
) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    room, *_ = await mediator.handle_command(
        CreateRoomCommand(
            name=faker.name(), house_uuid=house.oid, capacity=faker.random_int(1, 10)
        )
    )
    assert room
    assert room.house_id == house.oid
    assert await room_repository.get_by_uuid(room.oid)


@pytest.mark.asyncio
async def test_create_room_with_non_existing_house(
    mediator: Mediator, faker: Faker
) -> None:
    with pytest.raises(HouseNotFoundException):
        await mediator.handle_command(
            CreateRoomCommand(
                name=faker.name(),
                house_uuid=faker.uuid4(),
                capacity=faker.random_int(1, 10),
            )
        )


@pytest.mark.asyncio
async def test_join_room_with_user_not_exists(mediator: Mediator, faker: Faker) -> None:
    with pytest.raises(UserNotFoundException):
        await mediator.handle_command(JoinRoomCommand(faker.uuid4(), faker.uuid4()))


@pytest.mark.asyncio
async def test_join_room_with_room_not_exists(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))

    with pytest.raises(RoomNotFoundException):
        await mediator.handle_command(
            JoinRoomCommand(
                user.oid,
                faker.uuid4(),
            )
        )


@pytest.mark.asyncio
async def test_join_room_with_room_is_full(mediator: Mediator, faker: Faker) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    user2, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    room, *_ = await mediator.handle_command(
        CreateRoomCommand(name=faker.name(), house_uuid=house.oid, capacity=1)
    )

    await mediator.handle_command(JoinRoomCommand(user2.oid, room.oid))

    with pytest.raises(RoomIsFullException):
        await mediator.handle_command(JoinRoomCommand(user.oid, room.oid))


@pytest.mark.asyncio
async def test_join_room_with_user_already_in_room(
    mediator: Mediator, faker: Faker
) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    room, *_ = await mediator.handle_command(
        CreateRoomCommand(name=faker.name(), house_uuid=house.oid, capacity=5)
    )

    await mediator.handle_command(JoinRoomCommand(user.oid, room.oid))

    with pytest.raises(UserAlreadyInRoomException):
        await mediator.handle_command(JoinRoomCommand(user.oid, room.oid))


@pytest.mark.asyncio
async def test_join_room_success(
    mediator: Mediator, faker: Faker, resident_repository: ResidentRepository
) -> None:
    user, *_ = await mediator.handle_command(CreateUserCommand(name=faker.name()))
    house, *_ = await mediator.handle_command(
        CreateHouseCommand(name=faker.name(), owner_uuid=user.oid)
    )
    room, *_ = await mediator.handle_command(
        CreateRoomCommand(name=faker.name(), house_uuid=house.oid, capacity=5)
    )

    await mediator.handle_command(JoinRoomCommand(user.oid, room.oid))

    residents = await resident_repository.get_by_room_uuid(room.oid)

    assert user.oid in [resident.user_id for resident in residents]
