from dataclasses import dataclass

from domain.entities.colliving import House, Resident, Room, User
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.colliving import (
    HouseNotFoundException,
    RoomNotFoundException,
    UserNotFoundException,
)
from logic.interfaces.repository import (
    IHouseRepository,
    IResidentRepository,
    IRoomRepository,
    IUserRepository,
)


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str


@dataclass
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    user_repository: IUserRepository

    async def handle(self, command: CreateUserCommand) -> User:
        user = User.create(name=command.name)
        return await self.user_repository.create(user)


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
class CreateRoomCommand(BaseCommand):
    name: str
    capacity: int
    house_oid: str


@dataclass
class CreateRoomCommandHandler(CommandHandler[CreateRoomCommand, Room]):
    house_repository: IHouseRepository
    room_repository: IRoomRepository

    async def handle(self, command: CreateRoomCommand) -> Room:
        house = await self.house_repository.get_by_uuid(command.house_oid)
        if house is None:
            raise HouseNotFoundException(command.house_oid)

        room = Room.create(
            name=command.name, capacity=command.capacity, house_oid=command.house_oid
        )
        return await self.room_repository.create(room)


@dataclass(frozen=True)
class JoinRoomCommand(BaseCommand):
    user_oid: str
    room_oid: str


@dataclass
class JoinRoomCommandHandler(CommandHandler[JoinRoomCommand, None]):
    user_repository: IUserRepository
    room_repository: IRoomRepository
    resident_repository: IResidentRepository

    async def handle(self, command: JoinRoomCommand) -> None:
        user = await self.user_repository.get_by_uuid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)

        room = await self.room_repository.get_by_uuid(command.room_oid)
        if room is None:
            raise RoomNotFoundException(command.room_oid)

        resident = Resident.create(user_oid=command.user_oid, room_oid=command.room_oid)
        return await self.resident_repository.create(resident)
