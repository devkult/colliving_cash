from dataclasses import dataclass

from domain.exc import ColivingCashException


@dataclass(frozen=True)
class LogicException(ColivingCashException):
    @property
    def message(self) -> str:
        return "Logic exception"
