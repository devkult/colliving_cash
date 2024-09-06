from domain.entities.colliving import Resident
from gateways.models.colliving import ResidentModel


def resident_model_to_entity(resident_model: ResidentModel) -> Resident:
    return Resident(
        oid=resident_model.uuid,
        user=resident_model.user,
        house=resident_model.house,
    )


def resident_entity_to_model(resident: Resident) -> ResidentModel:
    return ResidentModel(
        uuid=resident.oid,
        user_uuid=resident.user.oid,
        house_uuid=resident.house.oid,
    )
