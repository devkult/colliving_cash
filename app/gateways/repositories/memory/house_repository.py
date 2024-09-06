from dataclasses import dataclass, field
from typing import Optional
from domain.entities.colliving import House
from domain.interfaces.repository import HouseRepository
from gateways.repositories.memory.base import MemoryRepository


class MemoryHouseRepository(MemoryRepository, HouseRepository):

    def __init__(self, storage) -> None:
        super().__init__(storage)
        self.houses: list[House] = self.storage.create_table([], "houses")

    async def add(self, house: House) -> House:
        self.houses.append(house)
        return house

    async def get_by_uuid(self, uuid: str) -> Optional[House]:
        return next((house for house in self.houses if house.oid == uuid), None)
