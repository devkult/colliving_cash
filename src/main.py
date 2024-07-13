import asyncio
from gateways.repositories.memory.house_repository import MemoryHouseRepository
from gateways.repositories.memory.room_repository import MemoryRoomRepository
from gateways.repositories.memory.user_repository import MemoryUserRepository
from logic.commands.colliving import CreateHouseCommand, CreateHouseCommandHandler, CreateRoomCommand, CreateRoomCommandHandler, CreateUserCommand, CreateUserCommandHandler


async def test():
    user_repository = MemoryUserRepository()
    house_repository = MemoryHouseRepository()
    room_repository = MemoryRoomRepository()

    # TODO: should be a factory
    handler = CreateUserCommandHandler(user_repository=user_repository)
    res = await handler.handle(CreateUserCommand(name="test_user"))
    print(res)

    handler = CreateHouseCommandHandler(house_repository=house_repository, user_repository=user_repository)
    res = await handler.handle(CreateHouseCommand(name="test_house", owner_uuid=res.oid))
    print(res)

    handler = CreateRoomCommandHandler(room_repository=room_repository, house_repository=house_repository)
    res = await handler.handle(CreateRoomCommand(name="test_room", capacity=10, house_oid=res.oid))
    print(res)


asyncio.run(test())