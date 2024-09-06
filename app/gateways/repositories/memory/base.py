from typing import TypeVar

from dataclasses import dataclass, field
from typing import TypeVar, Generic
import threading

D = TypeVar("D")


@dataclass
class MemoryStorage(Generic[D]):
    storage: dict[str, D] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def create_table(self, value: D, attribute_name: str) -> D:
        with self.lock:
            atr = self.storage.get(attribute_name)
            if atr is None:
                self.storage[attribute_name] = value
                return value
            return atr


@dataclass
class MemoryRepository:
    storage: MemoryStorage
