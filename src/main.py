import asyncio
from gateways.repositories.memory.house_repository import MemoryHouseRepository
from gateways.repositories.memory.user_repository import MemoryUserRepository
from logic.commands.colliving import CreateHouseCommand, CreateHouseCommandHandler, CreateUserCommand, CreateUserCommandHandler


async def test():
    user_repository = MemoryUserRepository()
    handler = CreateUserCommandHandler(user_repository=user_repository)
    res = await handler.handle(CreateUserCommand(name="test"))
    print(res)

    handler = CreateHouseCommandHandler(house_repository=MemoryHouseRepository(), user_repository=user_repository)
    res = await handler.handle(CreateHouseCommand(name="test", owner_uuid=res.oid))
    print(res)


asyncio.run(test())