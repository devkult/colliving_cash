from dataclasses import dataclass
from sqlalchemy import select
from typing import Optional
from domain.entities.colliving import User
from gateways.models.colliving import UserModel
from gateways.repositories.alchemy.base import SqlAlchemyRepository
from gateways.datamappers import user_datamapper as datamapper
from logic.interfaces.repository import  UserRepository


@dataclass
class SqlAlchemyUserRepository(SqlAlchemyRepository, UserRepository):

    async def add(self, user: User) -> User:
        self.session.add(datamapper.user_entity_to_model(user))
        return user

    async def get_by_uuid(self, uuid: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.uuid == uuid)
        )
        user_model = result.scalars().first()
        if user_model is None:
            return None
        return datamapper.user_model_to_entity(user_model)
