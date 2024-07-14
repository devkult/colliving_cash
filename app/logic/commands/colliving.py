from dataclasses import dataclass

from domain.entities.colliving import House, Resident, Room, User
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.colliving import (
    HouseNotFoundException,
    RoomIsFullException,
    RoomNotFoundException,
    UserAlreadyInRoomException,
    UserNotFoundException,
)
from logic.interfaces.repository import (
    HouseRepository,
    ResidentRepository,
    RoomRepository,
    UserRepository,
)


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str


@dataclass
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    user_repository: UserRepository

    async def handle(self, command: CreateUserCommand) -> User:
        user = User.create(name=command.name)
        return await self.user_repository.create(user)


@dataclass(frozen=True)
class CreateHouseCommand(BaseCommand):
    name: str
    owner_uuid: str


@dataclass
class CreateHouseCommandHandler(CommandHandler[CreateHouseCommand, House]):
    house_repository: HouseRepository
    user_repository: UserRepository

    async def handle(self, command: CreateHouseCommand) -> House:
        user = await self.user_repository.get_by_uuid(command.owner_uuid)
        if user is None:
            raise UserNotFoundException(command.owner_uuid)

        house = House.create(name=command.name, owner_id=command.owner_uuid)
        return await self.house_repository.create(house)


@dataclass(frozen=True)
class CreateRoomCommand(BaseCommand):
    name: str
    capacity: int
    house_uuid: str


@dataclass
class CreateRoomCommandHandler(CommandHandler[CreateRoomCommand, Room]):
    house_repository: HouseRepository
    room_repository: RoomRepository

    async def handle(self, command: CreateRoomCommand) -> Room:
        house = await self.house_repository.get_by_uuid(command.house_uuid)
        if house is None:
            raise HouseNotFoundException(command.house_uuid)

        room = Room.create(
            name=command.name, capacity=command.capacity, house_id=command.house_uuid
        )
        return await self.room_repository.create(room)


@dataclass(frozen=True)
class JoinRoomCommand(BaseCommand):
    user_oid: str
    room_oid: str


@dataclass
class JoinRoomCommandHandler(CommandHandler[JoinRoomCommand, None]):
    user_repository: UserRepository
    room_repository: RoomRepository
    resident_repository: ResidentRepository

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
        return await self.resident_repository.create(resident)