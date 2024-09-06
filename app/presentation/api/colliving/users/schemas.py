from pydantic import BaseModel

from domain.entities.colliving import User


class CreateUserRequestSchema(BaseModel):
    name: str


class CreateUserResponseSchema(BaseModel):
    user_id: str

    @classmethod
    def from_entity(cls, user: User):
        return cls(user_id=user.oid)
