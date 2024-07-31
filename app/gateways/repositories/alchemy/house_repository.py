from dataclasses import dataclass
from sqlalchemy import select
from typing import Optional
from domain.entities.colliving import House
from gateways.models.colliving import HouseModel
from gateways.repositories.alchemy.base import SqlAlchemyRepository
from gateways.datamappers import house_datamapper as datamapper
from logic.interfaces.repository import HouseRepository


@dataclass
class SqlAlchemyHouseRepository(SqlAlchemyRepository, HouseRepository):

    async def add(self, house: House) -> House:
        self.session.add(datamapper.house_entity_to_model(house))
        return house

    async def get_by_uuid(self, uuid: str) -> Optional[House]:
        result = await self.session.execute(
            select(HouseModel).where(HouseModel.uuid == uuid)
        )
        house_model = result.scalars().first()
        if house_model is None:
            return None
        return datamapper.house_model_to_entity(house_model)
