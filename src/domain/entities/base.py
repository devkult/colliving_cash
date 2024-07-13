from abc import ABC
from dataclasses import dataclass, field
import datetime
from uuid import uuid4


@dataclass(kw_only=True)
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.oid == other.oid

