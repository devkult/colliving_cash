from dishka import Provider, Scope, provide

from sqlalchemy.ext.asyncio import AsyncSession

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
    async def get_house(self, session: AsyncSession) -> HouseRepository: ...

    @provide
    async def get_user(self, session: AsyncSession) -> UserRepository: ...

    @provide
    async def get_room(self, session: AsyncSession) -> RoomRepository: ...

    @provide
    async def get_resident(self, session: AsyncSession) -> ResidentRepository: ...
