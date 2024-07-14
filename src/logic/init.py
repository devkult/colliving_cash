from functools import lru_cache
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide


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
    HouseRepository,
    ResidentRepository,
    RoomRepository,
    UserRepository,
)
from logic.mediator import Mediator


class MyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(self) -> UserRepository:
        pass

    @provide
    async def get_house_repository(self) -> HouseRepository:
        pass

    @provide
    async def get_room_repository(self) -> RoomRepository:
        pass

    @provide
    async def get_resident_repository(self) -> ResidentRepository:
        pass

    @provide
    async def get_create_user_command_handler(
        self, user_repository: UserRepository
    ) -> CreateUserCommandHandler:
        return CreateUserCommandHandler(user_repository=user_repository)

    @provide
    async def get_create_house_command_handler(
        self, house_repository: HouseRepository, user_repository: UserRepository
    ) -> CreateHouseCommandHandler:
        return CreateHouseCommandHandler(
            house_repository=house_repository, user_repository=user_repository
        )

    @provide
    async def get_create_room_command_handler(
        self, room_repository: RoomRepository, house_repository: HouseRepository
    ) -> CreateRoomCommandHandler:
        return CreateRoomCommandHandler(
            room_repository=room_repository, house_repository=house_repository
        )

    @provide
    async def get_join_room_command_handler(
        self,
        user_repository: UserRepository,
        room_repository: RoomRepository,
        resident_repository: ResidentRepository,
    ) -> JoinRoomCommandHandler:
        return JoinRoomCommandHandler(
            user_repository=user_repository,
            room_repository=room_repository,
            resident_repository=resident_repository,
        )

    @provide(scope=Scope.APP)
    async def get_mediator(
        self,
    ) -> Mediator:
        mediator = Mediator()
        mediator.register_command(CreateUserCommand, [CreateUserCommandHandler])
        mediator.register_command(JoinRoomCommand, [JoinRoomCommandHandler])
        mediator.register_command(CreateRoomCommand, [CreateRoomCommandHandler])
        mediator.register_command(CreateHouseCommand, [CreateHouseCommandHandler])

        return mediator





@lru_cache(1)
def init_container() -> AsyncContainer:
    return _init_container()





def _init_container() -> AsyncContainer:
    return make_async_container(MyProvider())
