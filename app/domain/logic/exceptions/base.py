from dataclasses import dataclass

from domain.exc import ColivingCashException


@dataclass(eq=False)
class LogicException(ColivingCashException):
    @property
    def message(self) -> str:
        return "Logic exception"
