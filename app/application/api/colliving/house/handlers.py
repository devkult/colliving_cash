from fastapi import APIRouter, HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from application.api.colliving.house.schemas import (
    CreateHouseRequestSchema,
    CreateHouseResponseSchema,
    GetHouseResidentsResponseSchema,
    GetHouseResponseSchema,
    JoinHouseRequestSchema,
    JoinHouseResponseSchema,
)
from domain.entities.colliving import House, Resident
from domain.exc import ColivingCashException
from domain.logic.commands.house import CreateHouseCommand, JoinHouseCommand
from domain.logic.exceptions.colliving import (
    HouseNotFoundException,
    UserNotFoundException,
)
from domain.logic.mediator import Mediator
from domain.logic.queries.house import GetHouseQuery, GetHouseResidentsQuery

router = APIRouter()


@router.get(
    "/{house_id}",
    status_code=status.HTTP_200_OK,
    description="Get house details",
    responses={status.HTTP_200_OK: {"model": GetHouseResponseSchema}},
)
@inject
async def get_house(house_id: str, mediator: FromDishka[Mediator]):
    try:
        house: House = await mediator.handle_query(GetHouseQuery(house_uuid=house_id))
    except HouseNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": e.message}
        )
    return GetHouseResponseSchema.from_entity(house)


@router.post(
    "",
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


@router.get(
    "/{house_id}/residents",
    status_code=status.HTTP_200_OK,
    description="Get all residents in the house",
    responses={status.HTTP_200_OK: {"model": GetHouseResidentsResponseSchema}},
)
@inject
async def get_house_residents(house_id: str, mediator: FromDishka[Mediator]):
    try:
        residents: list[Resident] = await mediator.handle_query(
            GetHouseResidentsQuery(house_uuid=house_id)
        )
    except HouseNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": e.message}
        )
    return GetHouseResidentsResponseSchema.from_entity(residents)


@router.post(
    "/{house_id}/residents",
    status_code=status.HTTP_201_CREATED,
    description="Add a resident to the house",
    responses={status.HTTP_201_CREATED: {"model": JoinHouseResponseSchema}},
)
@inject
async def join_house(schema: JoinHouseRequestSchema, mediator: FromDishka[Mediator]):
    try:
        resident, *_ = await mediator.handle_command(
            JoinHouseCommand(user_uuid=schema.user_uuid, house_uuid=schema.house_uuid)
        )
    except HouseNotFoundException or UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": e.message}
        )
    except ColivingCashException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message}
        )
    return JoinHouseResponseSchema.from_entity(resident)
