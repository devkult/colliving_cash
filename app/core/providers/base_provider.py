from aiojobs import Scheduler
from dishka import AsyncContainer, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from domain.logic.commands.house import (
    CreateHouseCommand,
    CreateHouseCommandHandler,
    JoinHouseCommand,
    JoinHouseCommandHandler,
)
from domain.logic.commands.user import CreateUserCommand, CreateUserCommandHandler
from domain.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    UserRepository,
)
from domain.interfaces.uow import AsyncUnitOfWork
from domain.logic.mediator import Mediator
from domain.logic.queries.house import (
    GetHouseQuery,
    GetHouseQueryHandler,
    GetHouseResidentsQuery,
    GetHouseResidentsQueryHandler,
)


class MyProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_scheduler(self) -> Scheduler:
        return Scheduler()

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
            uow=uow,
            house_repository=house_repository,
            user_repository=user_repository,
        )

    @provide
    async def get_join_house_command_handler(
        self,
        uow: AsyncUnitOfWork,
        house_repository: HouseRepository,
        user_repository: UserRepository,
        residents_repository: ResidentRepository,
    ) -> JoinHouseCommandHandler:
        return JoinHouseCommandHandler(
            uow=uow,
            house_repository=house_repository,
            user_repository=user_repository,
            residents_repository=residents_repository,
        )

    @provide
    async def get_get_house_query_handler(
        self, house_repository: HouseRepository
    ) -> GetHouseQueryHandler:
        return GetHouseQueryHandler(house_repository=house_repository)

    @provide
    async def get_get_house_residents_query_handler(
        self,
        house_repository: HouseRepository,
        residents_repository: ResidentRepository,
    ) -> GetHouseResidentsQueryHandler:
        return GetHouseResidentsQueryHandler(
            house_repository=house_repository, residents_repository=residents_repository
        )

    @provide(scope=Scope.APP)
    async def get_mediator(
        self,
        container: AsyncContainer,
    ) -> Mediator:
        mediator = Mediator(container=container)

        mediator.register_command(CreateUserCommand, [CreateUserCommandHandler])
        mediator.register_command(CreateHouseCommand, [CreateHouseCommandHandler])
        mediator.register_command(JoinHouseCommand, [JoinHouseCommandHandler])

        mediator.register_query(GetHouseQuery, GetHouseQueryHandler)
        mediator.register_query(GetHouseResidentsQuery, GetHouseResidentsQueryHandler)
        return mediator
