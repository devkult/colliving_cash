from dataclasses import dataclass, field
from domain.entities.colliving import House
from logic.interfaces.repository import IHouseRepository

@dataclass
class MemoryHouseRepository(IHouseRepository):
    houses: list[House] = field(default_factory=list)

    async def create(self, house: House) -> House:
        self.houses.append(house)
        return house
    