from dataclasses import dataclass
from typing import Self

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
class House(BaseEntity):
    name: str
    owner: User

    @classmethod
    def create(cls, name: str, owner: User) -> Self:
        return cls(
            name=name,
            owner=owner,
        )


@dataclass
class Resident(BaseEntity):
    user: User
    house: House

    @classmethod
    def create(cls, user: User, house: House) -> Self:
        return cls(
            user=user,
            house=house,
        )


@dataclass
class Exchange(BaseEntity):
    amount: int
    title: str
    description: str
    resident: Resident


class Bill(BaseEntity):
    exchanges: list[Exchange]
    house: House
