from dataclasses import dataclass

from domain.entities.colliving import House, User 
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.colliving import UserNotFoundException
from logic.interfaces.repository import IHouseRepository, IUserRepository


@dataclass(frozen=True)
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

@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str

@dataclass
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    user_repository: IUserRepository
    
    async def handle(self, command: CreateUserCommand) -> User:
        user = User.create(name=command.name)
        return await self.user_repository.create(user)