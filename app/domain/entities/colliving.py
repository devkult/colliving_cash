from dataclasses import dataclass

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
class Resident(BaseEntity):
    user_id: str
    house_id: str

    @classmethod
    def create(cls, user_id: str, house_id: str) -> "Resident":
        return cls(user_id=user_id, house_id=house_id)


@dataclass
class Bill(BaseEntity):
    amount: int
    title: str
    description: str
    user_oid: str


@dataclass
class House(BaseEntity):
    name: str
    owner_id: str

    @classmethod
    def create(cls, name: str, owner_id: str) -> "House":
        return cls(
            name=name,
            owner_id=owner_id,
        )
