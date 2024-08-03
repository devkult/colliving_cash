from domain.entities.colliving import Resident
from gateways.models.colliving import ResidentModel


def resident_model_to_entity(resident_model: ResidentModel) -> Resident:
    return Resident(
        oid=resident_model.uuid,
        user_id=resident_model.user_uuid,
        room_id=resident_model.room_uuid,
    )


def resident_entity_to_model(resident: Resident) -> ResidentModel:
    return ResidentModel(
        uuid=resident.oid,
        user_uuid=resident.user_id,
        room_uuid=resident.room_id,
    )
