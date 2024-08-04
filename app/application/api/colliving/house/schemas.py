from pydantic import BaseModel

from domain.entities.colliving import House, Resident


class CreateHouseRequestSchema(BaseModel):
    name: str
    owner_uuid: str


class CreateHouseResponseSchema(BaseModel):
    house_uuid: str

    @classmethod
    def from_entity(cls, house: House):
        return cls(house_uuid=house.oid)


class GetHouseResponseSchema(BaseModel):
    name: str
    owner_uuid: str

    @classmethod
    def from_entity(cls, house: House):
        return cls(
            name=house.name,
            owner_uuid=house.owner_id,
        )


class GetHouseResidentsResponseSchema(BaseModel):
    residents: list[str]

    @classmethod
    def from_entity(cls, residents: list[Resident]):
        return cls(residents=[resident.oid for resident in residents])


class JoinHouseRequestSchema(BaseModel):
    user_uuid: str
    house_uuid: str


class JoinHouseResponseSchema(BaseModel):
    resident_uuid: str

    @classmethod
    def from_entity(cls, resident: Resident):
        return cls(resident_uuid=resident.user_id)
