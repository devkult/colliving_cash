from pydantic import BaseModel

from domain.entities.colliving import Resident, Room


class CreateRoomRequestSchema(BaseModel):
    name: str
    capacity: int
    house_uuid: str


class CreateRoomResponseSchema(BaseModel):
    room_uuid: str

    @classmethod
    def from_entity(cls, room: Room):
        return cls(room_uuid=room.oid)


class JoinRoomRequestSchema(BaseModel):
    user_uuid: str
    room_uuid: str


class JoinRoomResponseSchema(BaseModel):
    resident_uuid: str

    @classmethod
    def from_entity(cls, resident: Resident):
        return cls(resident_uuid=resident.oid)
