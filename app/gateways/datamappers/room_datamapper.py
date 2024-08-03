from domain.entities.colliving import Room
from gateways.models.colliving import RoomModel


def room_model_to_entity(room: RoomModel) -> Room:
    return Room(
        oid=room.uuid,
        name=room.name,
        capacity=room.capacity,
        house_id=room.house_uuid,
    )


def room_entity_to_model(room: Room) -> RoomModel:
    return RoomModel(
        uuid=room.oid,
        name=room.name,
        capacity=room.capacity,
        house_uuid=room.house_id,
    )
