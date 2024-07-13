from dataclasses import dataclass, field
from typing import Optional

from domain.entities.colliving import Room
from logic.interfaces.repository import IRoomRepository


@dataclass
class MemoryRoomRepository(IRoomRepository):
    rooms: list[Room] = field(default_factory=list)

    async def create(self, room: Room) -> Room:
        self.rooms.append(room)
        return room

    async def get_by_oid(self, oid: str) -> Optional[Room]:
        for room in self.rooms:
            if room.oid == oid:
                return room
        return None