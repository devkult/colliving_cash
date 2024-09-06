from domain.entities.colliving import User
from domain.logic.commands.base import BaseCommand, BaseCommandHandler
from domain.interfaces.repository import UserRepository
from domain.interfaces.uow import AsyncUnitOfWork


from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str


@dataclass
class CreateUserCommandHandler(BaseCommandHandler[CreateUserCommand, User]):
    uow: AsyncUnitOfWork
    user_repository: UserRepository

    async def handle(self, command: CreateUserCommand) -> User:
        user = User.create(name=command.name)
        user = await self.user_repository.add(user)
        await self.uow.commit()
        return user
