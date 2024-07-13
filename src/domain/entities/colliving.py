from dataclasses import dataclass, field
import datetime

from domain.entities.base import BaseEntity


@dataclass
class User(BaseEntity):
    name: str

    @classmethod
    def create(cls, name: str) -> "User":
        return cls(
            name=name,
        )


@dataclass
class Room(BaseEntity):
    name: str
    capacity: int
    house_oid: str

    @classmethod
    def create(cls, name: str, capacity: int, house_oid: str) -> "Room":
        return cls(name=name, capacity=capacity, house_oid=house_oid)


@dataclass
class Resident(BaseEntity):
    user_oid: str
    room_oid: str

    @classmethod
    def create(cls, user_oid: str, room_oid: str) -> "Resident":
        return cls(user_oid=user_oid, room_oid=room_oid)


@dataclass
class Bill(BaseEntity):
    amount: int
    title: str
    description: str
    user_oid: str


@dataclass
class House(BaseEntity):
    name: str
    owner_oid: str

    @classmethod
    def create(cls, name: str, owner_oid: str) -> "House":
        return cls(
            name=name,
            owner_oid=owner_oid,
        )
