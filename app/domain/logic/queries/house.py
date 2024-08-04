from dataclasses import dataclass
from typing import Optional

from domain.entities.colliving import House, Resident
from domain.logic.exceptions.colliving import HouseNotFoundException
from domain.logic.interfaces.repository import HouseRepository, ResidentRepository
from domain.logic.queries.base import BaseQueryHandler


@dataclass(frozen=True)
class GetHouseQuery:
    house_uuid: str


@dataclass(frozen=True)
class GetHouseQueryHandler(BaseQueryHandler[GetHouseQuery, Optional[House]]):
    house_repository: HouseRepository

    async def handle(self, query: GetHouseQuery) -> Optional[House]:
        house = await self.house_repository.get_by_uuid(query.house_uuid)
        if house is None:
            raise HouseNotFoundException(query.house_uuid)

        return house


@dataclass(frozen=True)
class GetHouseResidentsQuery:
    house_uuid: str


@dataclass(frozen=True)
class GetHouseResidentsQueryHandler(
    BaseQueryHandler[GetHouseResidentsQuery, list[Resident]]
):
    house_repository: HouseRepository
    residents_repository: ResidentRepository

    async def handle(self, query: GetHouseResidentsQuery) -> list[Resident]:
        house = await self.house_repository.get_by_uuid(query.house_uuid)
        if house is None:
            raise HouseNotFoundException(query.house_uuid)

        return await self.residents_repository.get_by_house_uuid(house.oid)
