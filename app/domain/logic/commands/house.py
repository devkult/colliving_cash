from domain.entities.colliving import House, Resident
from domain.logic.commands.base import BaseCommand, BaseCommandHandler
from domain.logic.exceptions.colliving import (
    HouseNotFoundException,
    UserAlreadyJoinedHouseException,
    UserNotFoundException,
)
from domain.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    UserRepository,
)
from domain.interfaces.uow import AsyncUnitOfWork


from dataclasses import dataclass


@dataclass(frozen=True)
class CreateHouseCommand(BaseCommand):
    name: str
    owner_uuid: str


@dataclass
class CreateHouseCommandHandler(BaseCommandHandler[CreateHouseCommand, House]):
    uow: AsyncUnitOfWork
    house_repository: HouseRepository
    user_repository: UserRepository

    async def handle(self, command: CreateHouseCommand) -> House:
        user = await self.user_repository.get_by_uuid(command.owner_uuid)
        if user is None:
            raise UserNotFoundException(command.owner_uuid)

        house = House.create(name=command.name, owner=user)
        house = await self.house_repository.add(house)
        await self.uow.commit()
        return house


@dataclass(frozen=True)
class JoinHouseCommand(BaseCommand):
    user_uuid: str
    house_uuid: str


@dataclass
class JoinHouseCommandHandler(BaseCommandHandler[JoinHouseCommand, Resident]):
    uow: AsyncUnitOfWork
    house_repository: HouseRepository
    user_repository: UserRepository
    residents_repository: ResidentRepository

    async def handle(self, command: JoinHouseCommand) -> Resident:
        house = await self.house_repository.get_by_uuid(command.house_uuid)
        if house is None:
            raise HouseNotFoundException(command.house_uuid)

        user = await self.user_repository.get_by_uuid(command.user_uuid)
        if user is None:
            raise UserNotFoundException(command.user_uuid)

        if await self.residents_repository.get_by_user_and_house_uuid(
            user_uuid=user.oid, house_uuid=house.oid
        ):
            raise UserAlreadyJoinedHouseException(user.oid, house.oid)

        resident = Resident.create(user=user, house=house)
        resident = await self.residents_repository.add(resident)
        await self.uow.commit()
        return resident
