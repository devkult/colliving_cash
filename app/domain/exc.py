from dataclasses import dataclass


@dataclass(frozen=True)
class ColivingCashException(Exception):
    @property
    def message(self) -> str:
        return f"Coliving cash exception"
