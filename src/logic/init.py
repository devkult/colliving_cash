from functools import lru_cache
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from gateways.repositories.memory import (
    MemoryHouseRepository,
    MemoryResidentRepository,
    MemoryRoomRepository,
    MemoryUserRepository,
)

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
from logic.interfaces.repository import (
    IHouseRepository,
    IResidentRepository,
    IRoomRepository,
    IUserRepository,
)
from logic.mediator import Mediator


class DummyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(self) -> IUserRepository:
        return MemoryUserRepository()

    @provide
    async def get_house_repository(self) -> IHouseRepository:
        return MemoryHouseRepository()

    @provide
    async def get_room_repository(self) -> IRoomRepository:
        return MemoryRoomRepository()

    @provide
    async def get_resident_repository(self) -> IResidentRepository:
        return MemoryResidentRepository()

    @provide
    async def get_create_user_command_handler(
        self, user_repository: IUserRepository
    ) -> CreateUserCommandHandler:
        return CreateUserCommandHandler(user_repository=user_repository)

    @provide
    async def get_create_house_command_handler(
        self, house_repository: IHouseRepository, user_repository: IUserRepository
    ) -> CreateHouseCommandHandler:
        return CreateHouseCommandHandler(
            house_repository=house_repository, user_repository=user_repository
        )

    @provide
    async def get_create_room_command_handler(
        self, room_repository: IRoomRepository, house_repository: IHouseRepository
    ) -> CreateRoomCommandHandler:
        return CreateRoomCommandHandler(
            room_repository=room_repository, house_repository=house_repository
        )

    @provide
    async def get_join_room_command_handler(
        self,
        user_repository: IUserRepository,
        room_repository: IRoomRepository,
        resident_repository: IResidentRepository,
    ) -> JoinRoomCommandHandler:
        return JoinRoomCommandHandler(
            user_repository=user_repository,
            room_repository=room_repository,
            resident_repository=resident_repository,
        )

    @provide
    async def get_mediator(
        self,
        get_create_user_command_handler: CreateUserCommandHandler,
        get_join_room_command_handler: JoinRoomCommandHandler,
        get_create_room_command_handler: CreateRoomCommandHandler,
        get_create_house_command_handler: CreateHouseCommandHandler,
    ) -> Mediator:
        mediator = Mediator()
        mediator.register_command(CreateUserCommand, [get_create_user_command_handler])
        mediator.register_command(JoinRoomCommand, [get_join_room_command_handler])
        mediator.register_command(CreateRoomCommand, [get_create_room_command_handler])
        mediator.register_command(CreateHouseCommand, [get_create_house_command_handler])

        return mediator


@lru_cache(1)
def init_container() -> AsyncContainer:
    return _init_container()


def _init_container() -> AsyncContainer:
    return make_async_container(DummyProvider())
