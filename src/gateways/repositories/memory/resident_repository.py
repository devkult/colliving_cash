from dataclasses import dataclass, field
from typing import Optional, TypeAlias

from domain.entities.colliving import Resident
from logic.interfaces.repository import IResidentsRepository

RoomId = str
UserId = str


@dataclass
class MemoryResidentRepository(IResidentsRepository):
    residents: dict[RoomId, list[UserId]] = field(default_factory=dict)

    async def create(self, resident: Resident) -> Resident:
        if resident.room_oid not in self.residents:
            self.residents[resident.room_oid] = []
        self.residents[resident.room_oid].append(resident.oid)
        return resident

    async def get_by_uuid(self, uuid: str) -> Optional[Resident]:
        for room_oid in self.residents:
            if uuid in self.residents[room_oid]:
                return Resident(oid=uuid, room_oid=room_oid)
        return None