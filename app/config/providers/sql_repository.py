from dishka import Scope, provide

from sqlalchemy.ext.asyncio import AsyncSession

from gateways.repositories.alchemy.house_repository import SqlAlchemyHouseRepository
from gateways.repositories.alchemy.user_repository import SqlAlchemyUserRepository
from logic.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    RoomRepository,
    UserRepository,
)

from .base_provider import MyProvider


class SqlRepositoryProvider(MyProvider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return SqlAlchemyUserRepository(session)

    @provide
    async def get_house_repository(self, session: AsyncSession) -> HouseRepository:
        return SqlAlchemyHouseRepository(session)

    @provide
    async def get_room_repository(self) -> RoomRepository:
        pass

    @provide
    async def get_resident_repository(self) -> ResidentRepository:
        pass
