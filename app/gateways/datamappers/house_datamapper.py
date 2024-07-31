from domain.entities.colliving import House
from gateways.models.colliving import HouseModel


def house_model_to_entity(house: HouseModel) -> House:
    return House(
        oid=house.uuid,
        name=house.name,
        owner_id=house.owner_uuid,
    )

def house_entity_to_model(house: House) -> HouseModel:
    return HouseModel(
        uuid=house.oid,
        name=house.name,
        owner_uuid=house.owner_id,
    )