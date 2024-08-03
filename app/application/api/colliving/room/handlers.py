from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status
from application.api.colliving.room.schemas import (
    CreateRoomRequestSchema,
    CreateRoomResponseSchema,
    JoinRoomRequestSchema,
    JoinRoomResponseSchema,
)
from domain.exc import ColivingCashException
from domain.logic.commands.room import CreateRoomCommand, JoinRoomCommand
from domain.logic.exceptions.colliving import HouseNotFoundException
from domain.logic.mediator import Mediator


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create a new room",
    responses={status.HTTP_201_CREATED: {"model": CreateRoomResponseSchema}},
)
@inject
async def create_room(schema: CreateRoomRequestSchema, mediator: FromDishka[Mediator]):
    try:
        room, *_ = await mediator.handle_command(
            CreateRoomCommand(
                name=schema.name,
                house_uuid=schema.house_uuid,
                capacity=schema.capacity,
            )
        )
    except HouseNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": e.message}
        )
    except ColivingCashException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message}
        )
    return CreateRoomResponseSchema.from_entity(room)


@router.post(
    "/join",
    status_code=status.HTTP_201_CREATED,
    description="Join a room",
    responses={status.HTTP_201_CREATED: {"model": JoinRoomResponseSchema}},
)
@inject
async def join_room(schema: JoinRoomRequestSchema, mediator: FromDishka[Mediator]):
    try:
        resident, *_ = await mediator.handle_command(
            JoinRoomCommand(user_oid=schema.user_uuid, room_oid=schema.room_uuid)
        )
    except ColivingCashException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message}
        )
    return JoinRoomResponseSchema.from_entity(resident)
