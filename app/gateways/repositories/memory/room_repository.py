from dataclasses import dataclass, field
from typing import Optional

from domain.entities.colliving import Room
from logic.interfaces.repository import RoomRepository


class MemoryRoomRepository(RoomRepository):
    rooms: list[Room] = []

    async def add(self, room: Room) -> Room:
        self.rooms.append(room)
        return room

    async def get_by_uuid(self, uuid: str) -> Optional[Room]:
        for room in self.rooms:
            if room.oid == uuid:
                return room
        return None
