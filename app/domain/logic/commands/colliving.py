from dataclasses import dataclass

from domain.entities.colliving import House, Resident, Room, User
from domain.logic.commands.base import BaseCommand, CommandHandler
from domain.logic.exceptions.colliving import (
    HouseNotFoundException,
    RoomIsFullException,
    RoomNotFoundException,
    UserAlreadyInRoomException,
    UserNotFoundException,
)
from domain.logic.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    RoomRepository,
    UserRepository,
)
from domain.logic.interfaces.uow import AsyncUnitOfWork


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str


@dataclass
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    uow: AsyncUnitOfWork
    user_repository: UserRepository

    async def handle(self, command: CreateUserCommand) -> User:
        user = User.create(name=command.name)
        user = await self.user_repository.add(user)
        await self.uow.commit()
        return user


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


@dataclass(frozen=True)
class CreateRoomCommand(BaseCommand):
    name: str
    capacity: int
    house_uuid: str


@dataclass
class CreateRoomCommandHandler(CommandHandler[CreateRoomCommand, Room]):
    house_repository: HouseRepository
    room_repository: RoomRepository
    uow: AsyncUnitOfWork

    async def handle(self, command: CreateRoomCommand) -> Room:
        house = await self.house_repository.get_by_uuid(command.house_uuid)
        if house is None:
            raise HouseNotFoundException(command.house_uuid)

        room = Room.create(
            name=command.name, capacity=command.capacity, house_id=command.house_uuid
        )

        room = await self.room_repository.add(room)

        await self.uow.commit()

        return room


@dataclass(frozen=True)
class JoinRoomCommand(BaseCommand):
    user_oid: str
    room_oid: str


@dataclass
class JoinRoomCommandHandler(CommandHandler[JoinRoomCommand, None]):
    user_repository: UserRepository
    room_repository: RoomRepository
    resident_repository: ResidentRepository
    uow: AsyncUnitOfWork

    async def handle(self, command: JoinRoomCommand) -> None:
        user = await self.user_repository.get_by_uuid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)

        room = await self.room_repository.get_by_uuid(command.room_oid)
        if room is None:
            raise RoomNotFoundException(command.room_oid)

        residents = await self.resident_repository.get_by_room_uuid(room.oid)
        if len(residents) >= room.capacity:
            raise RoomIsFullException(room.oid)

        if user.oid in [resident.user_id for resident in residents]:
            raise UserAlreadyInRoomException(command.user_oid, room.oid)

        resident = Resident.create(user_id=command.user_oid, room_id=command.room_oid)
        await self.resident_repository.add(resident)

        await self.uow.commit()
