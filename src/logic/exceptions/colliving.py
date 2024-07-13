from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class UserNotFoundException(LogicException):
    uuid: str

    @property
    def message(self) -> str:
        return f"User with uuid {self.uuid} not found"