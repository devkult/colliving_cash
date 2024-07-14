from fastapi import APIRouter, HTTPException, status
from dishka import FromDishka, inject

from application.api.colliving.house.schemas import (
    CreateHouseRequestSchema,
    CreateHouseResponseSchema,
)
from domain.exc import ColivingCashException
from logic.commands.colliving import CreateHouseCommand
from logic.mediator import Mediator

router = APIRouter(prefix="/house")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create a new house",
    responses={status.HTTP_201_CREATED: {"model": CreateHouseResponseSchema}},
)
@inject
async def create_house(
    schema: CreateHouseRequestSchema, mediator: FromDishka[Mediator]
):
    try:
        house, *_ = await mediator.handle_command(
            CreateHouseCommand(name=schema.name, owner_uuid=schema.owner_uuid)
        )
    except ColivingCashException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message}
        )
    return CreateHouseResponseSchema.from_entity(house)
