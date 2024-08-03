from domain.entities.colliving import House
from domain.logic.commands.base import BaseCommand, CommandHandler
from domain.logic.exceptions.colliving import UserNotFoundException
from domain.logic.interfaces.repository import HouseRepository, UserRepository
from domain.logic.interfaces.uow import AsyncUnitOfWork


from dataclasses import dataclass


@dataclass(frozen=True)
class CreateHouseCommand(BaseCommand):
    name: str
    owner_uuid: str


@dataclass
class CreateHouseCommandHandler(CommandHandler[CreateHouseCommand, House]):
    uow: AsyncUnitOfWork
    house_repository: HouseRepository
    user_repository: UserRepository

    async def handle(self, command: CreateHouseCommand) -> House:
        user = await self.user_repository.get_by_uuid(command.owner_uuid)
        if user is None:
            raise UserNotFoundException(command.owner_uuid)

        house = House.create(name=command.name, owner_id=command.owner_uuid)
        house = await self.house_repository.add(house)
        await self.uow.commit()
        return house
