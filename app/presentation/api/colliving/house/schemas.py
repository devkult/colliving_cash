from pydantic import BaseModel

from domain.entities.colliving import House, Resident


class CreateHouseRequestSchema(BaseModel):
    name: str
    owner_id: str


class CreateHouseResponseSchema(BaseModel):
    house_id: str

    @classmethod
    def from_entity(cls, house: House):
        return cls(house_id=house.oid)


class GetHouseResponseSchema(BaseModel):
    name: str
    owner_id: str

    @classmethod
    def from_entity(cls, house: House):
        return cls(
            name=house.name,
            owner_id=house.owner.oid,
        )


class GetHouseResidentsResponseSchema(BaseModel):
    residents: list[str]

    @classmethod
    def from_entity(cls, residents: list[Resident]):
        return cls(residents=[resident.oid for resident in residents])


class JoinHouseRequestSchema(BaseModel):
    user_id: str


class JoinHouseResponseSchema(BaseModel):
    resident_id: str

    @classmethod
    def from_entity(cls, resident: Resident):
        return cls(resident_id=resident.oid)
