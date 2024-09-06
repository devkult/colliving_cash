from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

QR = TypeVar("R", bound=Any)


@dataclass(frozen=True)
class BaseQuery(ABC, Generic[QR]): ...


@dataclass(frozen=True)
class BaseQueryHandler(ABC, Generic[QR]):
    @abstractmethod
    async def handle(self, query: BaseQuery) -> QR: ...
