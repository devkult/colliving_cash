from dataclasses import dataclass, field
from typing import Optional, TypeAlias

from domain.entities.colliving import Resident
from domain.logic.interfaces.repository import ResidentRepository

HouseId = str
UserId = str


class MemoryResidentRepository(ResidentRepository):
    residents: list[Resident] = []

    async def add(self, resident: Resident) -> Resident:
        self.residents.append(resident)
        return resident

    async def get_by_uuid(self, uuid: str) -> Optional[Resident]:
        return next(
            (resident for resident in self.residents if resident.user_id == uuid), None
        )

    async def get_by_house_uuid(self, house_uuid: str) -> list[Resident]:
        return [
            resident for resident in self.residents if resident.house_id == house_uuid
        ]

    async def get_by_user_and_house_uuid(
        self, user_uuid: str, house_uuid: str
    ) -> Optional[Resident]:
        residents_in_house = await self.get_by_house_uuid(house_uuid)
        return next(
            (
                resident
                for resident in residents_in_house
                if resident.user_id == user_uuid
            ),
            None,
        )
