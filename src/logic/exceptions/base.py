from dataclasses import dataclass


@dataclass
class LogicException(Exception):
    @property
    def message(self) -> str:
        return "Logic exception"

