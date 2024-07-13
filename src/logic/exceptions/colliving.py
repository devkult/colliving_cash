from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True)
class UserNotFoundException(LogicException):
    user_uuid: str

    @property
    def message(self) -> str:
        return f"User with uuid {self.user_uuid} not found"
    