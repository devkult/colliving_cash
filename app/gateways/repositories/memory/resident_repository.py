from dataclasses import dataclass, field
from typing import Optional, TypeAlias

from domain.entities.colliving import Resident
from domain.interfaces.repository import ResidentRepository
from gateways.repositories.memory.base import MemoryRepository

HouseId = str
UserId = str


class MemoryResidentRepository(MemoryRepository, ResidentRepository):
    def __init__(self, storage) -> None:
        super().__init__(storage)
        self.residents: list[Resident] = self.storage.create_table([], "residents")

    async def add(self, resident: Resident) -> Resident:
        self.residents.append(resident)
        return resident

    async def get_by_uuid(self, uuid: str) -> Optional[Resident]:
        return next(
            (resident for resident in self.residents if resident.oid == uuid), None
        )

    async def get_by_house_uuid(self, house_uuid: str) -> list[Resident]:
        return [
            resident for resident in self.residents if resident.house.oid == house_uuid
        ]

    async def get_by_user_and_house_uuid(
        self, user_uuid: str, house_uuid: str
    ) -> Optional[Resident]:
        residents_in_house = await self.get_by_house_uuid(house_uuid)
        return next(
            (
                resident
                for resident in residents_in_house
                if resident.user.oid == user_uuid
            ),
            None,
        )
