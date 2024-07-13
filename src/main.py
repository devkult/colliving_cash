import asyncio
from gateways.repositories.memory.house_repository import MemoryHouseRepository
from gateways.repositories.memory.resident_repository import MemoryResidentRepository
from gateways.repositories.memory.room_repository import MemoryRoomRepository
from gateways.repositories.memory.user_repository import MemoryUserRepository
from logic.commands.colliving import (
    CreateHouseCommand,
    CreateHouseCommandHandler,
    CreateRoomCommand,
    CreateRoomCommandHandler,
    CreateUserCommand,
    CreateUserCommandHandler,
    JoinRoomCommand,
    JoinRoomCommandHandler,
)


async def test():
    user_repository = MemoryUserRepository()
    house_repository = MemoryHouseRepository()
    room_repository = MemoryRoomRepository()
    resident_repository = MemoryResidentRepository()

    # TODO: should be a factory
    handler = CreateUserCommandHandler(user_repository=user_repository)
    user_res = await handler.handle(CreateUserCommand(name="test_user"))
    print(user_res)

    handler = CreateHouseCommandHandler(
        house_repository=house_repository, user_repository=user_repository
    )
    res = await handler.handle(
        CreateHouseCommand(name="test_house", owner_uuid=user_res.oid)
    )
    print(res)

    handler = CreateRoomCommandHandler(
        room_repository=room_repository, house_repository=house_repository
    )
    res = await handler.handle(
        CreateRoomCommand(name="test_room", capacity=10, house_oid=res.oid)
    )
    print(res)

    handler = JoinRoomCommandHandler(
        room_repository=room_repository, user_repository=user_repository, resident_repository=resident_repository
    )
    res = await handler.handle(JoinRoomCommand(room_oid=res.oid, user_oid=user_res.oid))
    print(res)

asyncio.run(test())
