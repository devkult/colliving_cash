from pydantic import BaseModel

from domain.entities.colliving import House


class CreateHouseRequestSchema(BaseModel):
    name: str
    owner_uuid: str


class CreateHouseResponseSchema(BaseModel):
    house_uuid: str

    @classmethod
    def from_entity(cls, house: House):
        return cls(house_uuid=house.oid)