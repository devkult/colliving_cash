from dataclasses import dataclass
from sqlalchemy import select
from typing import Optional
from domain.entities.colliving import Room
from gateways.models.colliving import RoomModel
from gateways.repositories.alchemy.base import SqlAlchemyRepository
from gateways.datamappers import room_datamapper as datamapper
from domain.logic.interfaces.repository import RoomRepository


@dataclass
class SqlAlchemyRoomRepository(SqlAlchemyRepository, RoomRepository):

    async def add(self, room: Room) -> Room:
        self.session.add(datamapper.room_entity_to_model(room))
        return room

    async def get_by_uuid(self, uuid: str) -> Optional[Room]:
        result = await self.session.execute(
            select(RoomModel).where(RoomModel.uuid == uuid)
        )
        room_model = result.scalars().first()
        if room_model is None:
            return None
        return datamapper.room_model_to_entity(room_model)
