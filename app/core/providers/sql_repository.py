from dishka import Scope, provide

from sqlalchemy.ext.asyncio import AsyncSession

from gateways.repositories.alchemy.house_repository import SqlAlchemyHouseRepository
from gateways.repositories.alchemy.resident_repository import (
    SqlAlchemyResidentRepository,
)
from gateways.repositories.alchemy.user_repository import SqlAlchemyUserRepository
from domain.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
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
    async def get_resident_repository(
        self, session: AsyncSession
    ) -> ResidentRepository:
        return SqlAlchemyResidentRepository(session)
