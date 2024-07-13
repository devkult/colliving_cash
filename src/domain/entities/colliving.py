from dataclasses import dataclass, field
import datetime

from domain.entities.base import BaseEntity


@dataclass
class User(BaseEntity):
    name: str


@dataclass
class Room(BaseEntity):
    name: str
    users: list[User] = field(default_factory=list)


@dataclass
class Bill(BaseEntity):
    amount: int
    title: str
    description: str


@dataclass
class House(BaseEntity):
    name: str
    owner: User 
    users: list[User] = field(default_factory=list)
    bills: dict[User : list[Bill]] = field(default_factory=dict)
    rooms: list[Room] = field(default_factory=list)

    @classmethod
    def create(cls, name: str, owner: User) -> "House":
        return cls(
            name=name,
            owner=owner,
        )