import asyncio
from logic.commands.colliving import (
    CreateHouseCommand,
    CreateRoomCommand,
    CreateUserCommand,
    JoinRoomCommand,
)
from logic.init import init_dummy_container
from logic.mediator import Mediator


async def test() -> None:
    container = init_dummy_container()
    mediator = await container.get(Mediator)
    mediator.container = container
    user_res, *_ = await mediator.handle_command(CreateUserCommand("user1"))
    house_res, *_ = await mediator.handle_command(CreateHouseCommand("house1", user_res.oid))
    room_res, *_ = await mediator.handle_command(CreateRoomCommand("room1", 10, house_res.oid))
    resident_res, *_ = await mediator.handle_command(JoinRoomCommand(user_res.oid, room_res.oid))
    print(user_res.oid, house_res.oid, room_res.oid, resident_res.oid)

asyncio.run(test())
