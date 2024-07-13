from dataclasses import dataclass

from domain.entities.colliving import House 
from domain.exc import UserNotFoundException
from logic.commands.base import BaseCommand, CommandHandler
from logic.interfaces.repository import IHouseRepository, IUserRepository


@dataclass
class CreateHouseCommand(BaseCommand):
    name: str
    owner_uuid: str 

@dataclass
class CreateHouseCommandHandler(CommandHandler[CreateHouseCommand, House]):
    house_repository: IHouseRepository
    user_repository: IUserRepository
    
    async def handle(self, command: CreateHouseCommand) -> House:
        user = await self.user_repository.get_by_uuid(command.owner_uuid)
        if user is None:
            raise UserNotFoundException(command.owner_uuid)
        
        house = House.create(name=command.name, owner_oid=command.owner_uuid)
        return await self.house_repository.create(house)

        