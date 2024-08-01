from fastapi import APIRouter, HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject


from application.api.colliving.users.schemas import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from domain.exc import ColivingCashException
from domain.logic.commands.colliving import CreateUserCommand
from domain.logic.mediator import Mediator

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create a new user",
    responses={status.HTTP_201_CREATED: {"model": CreateUserResponseSchema}},
)
@inject
async def create_user(schema: CreateUserRequestSchema, mediator: FromDishka[Mediator]):
    try:
        user, *_ = await mediator.handle_command(CreateUserCommand(name=schema.name))
    except ColivingCashException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message}
        )
    return CreateUserResponseSchema.from_entity(user)
