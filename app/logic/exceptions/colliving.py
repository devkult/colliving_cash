from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True)
class UserNotFoundException(LogicException):
    user_uuid: str

    @property
    def message(self) -> str:
        return f"User with uuid {self.user_uuid} not found"


@dataclass(frozen=True)
class HouseNotFoundException(LogicException):
    house_uuid: str

    @property
    def message(self) -> str:
        return f"House with uuid {self.house_uuid} not found"


@dataclass(frozen=True)
class RoomNotFoundException(LogicException):
    room_uuid: str

    @property
    def message(self) -> str:
        return f"Room with uuid {self.room_uuid} not found"


@dataclass(frozen=True)
class RoomIsFullException(LogicException):
    room_uuid: str

    @property
    def message(self) -> str:
        return f"Room with uuid {self.room_uuid} is full"


@dataclass(frozen=True)
class UserAlreadyInRoomException(LogicException):
    user_uuid: str
    room_uuid: str

    @property
    def message(self) -> str:
        return f"User with uuid {self.user_uuid} already in room with uuid {self.room_uuid}"
