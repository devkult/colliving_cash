from dataclasses import dataclass, field
from typing import Optional
from domain.entities.colliving import House
from logic.interfaces.repository import HouseRepository


class MemoryHouseRepository(HouseRepository):
    houses: list[House] = []

    async def create(self, house: House) -> House:
        self.houses.append(house)
        return house

    async def get_by_uuid(self, uuid: str) -> Optional[House]:
        return next((house for house in self.houses if house.oid == uuid), None)
