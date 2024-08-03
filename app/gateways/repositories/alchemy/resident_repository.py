from dataclasses import dataclass
from sqlalchemy import select
from typing import Optional
from domain.entities.colliving import Resident
from gateways.models.colliving import ResidentModel
from gateways.repositories.alchemy.base import SqlAlchemyRepository
from gateways.datamappers import resident_datamapper as datamapper
from domain.logic.interfaces.repository import ResidentRepository, ResidentRepository


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

    async def get_by_room_uuid(self, room_uuid: str) -> list[Resident]:
        result = await self.session.execute(
            select(ResidentModel).where(ResidentModel.room_uuid == room_uuid)
        )
        resident_models = result.scalars().all()
        return [
            datamapper.resident_model_to_entity(resident_model)
            for resident_model in resident_models
        ]
