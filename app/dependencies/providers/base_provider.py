from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from domain.logic.commands.colliving import (
    CreateHouseCommand,
    CreateHouseCommandHandler,
    CreateRoomCommand,
    CreateRoomCommandHandler,
    CreateUserCommand,
    CreateUserCommandHandler,
    JoinRoomCommand,
    JoinRoomCommandHandler,
)
from domain.logic.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    RoomRepository,
    UserRepository,
)
from domain.logic.interfaces.uow import AsyncUnitOfWork
from domain.logic.mediator import Mediator


class MyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_uow(self, session: AsyncSession) -> AsyncUnitOfWork:
        return session

    @provide
    async def get_create_user_command_handler(
        self, uow: AsyncUnitOfWork, user_repository: UserRepository
    ) -> CreateUserCommandHandler:
        return CreateUserCommandHandler(uow=uow, user_repository=user_repository)

    @provide
    async def get_create_house_command_handler(
        self,
        uow: AsyncUnitOfWork,
        house_repository: HouseRepository,
        user_repository: UserRepository,
    ) -> CreateHouseCommandHandler:
        return CreateHouseCommandHandler(
            uow=uow, house_repository=house_repository, user_repository=user_repository
        )

    @provide
    async def get_create_room_command_handler(
        self,
        uow: AsyncUnitOfWork,
        room_repository: RoomRepository,
        house_repository: HouseRepository,
    ) -> CreateRoomCommandHandler:
        return CreateRoomCommandHandler(
            room_repository=room_repository, house_repository=house_repository, uow=uow
        )

    @provide
    async def get_join_room_command_handler(
        self,
        uow: AsyncUnitOfWork,
        user_repository: UserRepository,
        room_repository: RoomRepository,
        resident_repository: ResidentRepository,
    ) -> JoinRoomCommandHandler:
        return JoinRoomCommandHandler(
            user_repository=user_repository,
            room_repository=room_repository,
            resident_repository=resident_repository,
            uow=uow,
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
