from dataclasses import dataclass, field
from typing import Optional, TypeAlias

from domain.entities.colliving import Resident
from domain.logic.interfaces.repository import ResidentRepository

RoomId = str
UserId = str


class MemoryResidentRepository(ResidentRepository):
    residents: dict[RoomId, list[UserId]] = {}

    async def add(self, resident: Resident) -> Resident:
        if resident.room_id not in self.residents:
            self.residents[resident.room_id] = []
        self.residents[resident.room_id].append(resident.user_id)
        return resident

    async def get_by_uuid(self, uuid: str) -> Optional[Resident]:
        for room_oid in self.residents:
            if uuid in self.residents[room_oid]:
                return Resident(user_id=uuid, room_id=room_oid)
        return None

    async def get_by_room_uuid(self, room_uuid: str) -> list[Resident]:
        if room_uuid in self.residents:
            return [
                Resident(user_id=resident_uuid, room_id=room_uuid)
                for resident_uuid in self.residents[room_uuid]
            ]
        return []
