from domain.entities.colliving import User
from gateways.models.colliving import UserModel


def user_model_to_entity(user: UserModel) -> User:
    return User(
        oid=user.uuid,
        name=user.name,
    )

def user_entity_to_model(user: User) -> UserModel:
    return UserModel(
        uuid=user.oid,
        name=user.name,
    )