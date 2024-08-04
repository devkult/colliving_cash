from dataclasses import dataclass


@dataclass(eq=False)
class ColivingCashException(Exception):
    @property
    def message(self) -> str:
        return f"Coliving cash exception"
