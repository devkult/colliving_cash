from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional
from domain.entities.colliving import Resident
from gateways.models.colliving import ResidentModel
from gateways.repositories.alchemy.base import SqlAlchemyRepository
from gateways.datamappers import resident_datamapper as datamapper
from domain.interfaces.repository import ResidentRepository, ResidentRepository


@dataclass
class SqlAlchemyResidentRepository(SqlAlchemyRepository, ResidentRepository):

    async def add(self, resident: Resident) -> Resident:
        self.session.add(datamapper.resident_entity_to_model(resident))
        return resident

    async def get_by_uuid(self, uuid: str) -> Optional[Resident]:
        result = await self.session.execute(
            select(ResidentModel).where(ResidentModel.uuid == uuid)
        )
        resident_model = result.scalars().first()
        if resident_model is None:
            return None
        return datamapper.resident_model_to_entity(resident_model)

    async def get_by_house_uuid(self, house_uuid: str) -> list[Resident]:
        result = await self.session.execute(
            select(ResidentModel).where(ResidentModel.house_uuid == house_uuid)
        )
        resident_models = result.scalars().all()
        return [
            datamapper.resident_model_to_entity(resident_model)
            for resident_model in resident_models
        ]

    async def get_by_user_and_house_uuid(
        self, user_uuid: str, house_uuid: str
    ) -> Optional[Resident]:
        result = await self.session.execute(
            select(ResidentModel)
            .options(
                joinedload(ResidentModel.user),  # подгружаем UserModel
                joinedload(ResidentModel.house)  # подгружаем HouseModel
            )
            .where(ResidentModel.user_uuid == user_uuid)
            .where(ResidentModel.house_uuid == house_uuid)
        )
        resident_model = result.scalars().first()
        if resident_model is None:
            return None
        return datamapper.resident_model_to_entity(resident_model)