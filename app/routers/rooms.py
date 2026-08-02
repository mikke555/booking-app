from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status

from app.dependencies import DateRangeDep, RoomServiceDep, get_current_admin
from app.schemas.rooms import (
    RoomCreate,
    RoomRead,
    RoomReadAvailable,
    RoomUpdate,
    room_create_examples,
)

router = APIRouter(tags=["Rooms"])


@router.get(
    "/hotels/{hotel_id}/rooms",
    response_model=list[RoomReadAvailable],
    description="List rooms of a specific hotel available for the requested dates, including the quantity left.",
)
async def list_by_hotel(hotel_id: int, dates: DateRangeDep, service: RoomServiceDep):
    return await service.list_available_by_hotel(hotel_id=hotel_id, dates=dates)


@router.post(
    "/hotels/{hotel_id}/rooms",
    response_model=RoomRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
async def add_room(
    hotel_id: int,
    payload: Annotated[RoomCreate, Body(openapi_examples=room_create_examples)],
    service: RoomServiceDep,
):
    return await service.create_room(payload, hotel_id=hotel_id)


@router.get("/rooms/{room_id}", response_model=RoomRead)
async def get_room(room_id: int, service: RoomServiceDep):
    return await service.get_room(room_id)


@router.patch(
    "/rooms/{room_id}",
    response_model=RoomRead,
    dependencies=[Depends(get_current_admin)],
)
async def update_room(room_id: int, payload: RoomUpdate, service: RoomServiceDep):
    return await service.update_room(room_id, payload)


@router.delete(
    "/rooms/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
async def delete_room(room_id: int, service: RoomServiceDep):
    await service.delete_room(room_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
