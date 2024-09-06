from dataclasses import dataclass
from typing import Optional

from domain.entities.colliving import House, Resident
from domain.logic.exceptions.colliving import HouseNotFoundException
from domain.interfaces.repository import HouseRepository, ResidentRepository
from domain.logic.queries.base import BaseQueryHandler, BaseQuery


@dataclass(frozen=True)
class GetHouseQuery(BaseQuery[House]):
    house_uuid: str


@dataclass(frozen=True)
class GetHouseQueryHandler(BaseQueryHandler[House]):
    house_repository: HouseRepository

    async def handle(self, query: GetHouseQuery) -> House:
        house = await self.house_repository.get_by_uuid(query.house_uuid)
        if house is None:
            raise HouseNotFoundException(query.house_uuid)

        return house


@dataclass(frozen=True)
class GetHouseResidentsQuery(BaseQuery[list[Resident]]):
    house_uuid: str


@dataclass(frozen=True)
class GetHouseResidentsQueryHandler(BaseQueryHandler[list[Resident]]):
    house_repository: HouseRepository
    residents_repository: ResidentRepository

    async def handle(self, query: GetHouseResidentsQuery) -> list[Resident]:
        house = await self.house_repository.get_by_uuid(query.house_uuid)
        if house is None:
            raise HouseNotFoundException(query.house_uuid)

        return await self.residents_repository.get_by_house_uuid(house.oid)
