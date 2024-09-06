from dataclasses import dataclass

from domain.logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    user_uuid: str

    @property
    def message(self) -> str:
        return f"User with id {self.user_uuid} not found"


@dataclass(eq=False)
class HouseNotFoundException(LogicException):
    house_uuid: str

    @property
    def message(self) -> str:
        return f"House with id {self.house_uuid} not found"


@dataclass(eq=False)
class UserAlreadyJoinedHouseException(LogicException):
    user_uuid: str
    house_uuid: str

    @property
    def message(self) -> str:
        return f"User with id {self.user_uuid} already joined house with uuid {self.house_uuid}"
