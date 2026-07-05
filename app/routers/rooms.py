from fastapi import APIRouter, Response, status

from app.dependencies import RoomServiceDep
from app.schemas.rooms import RoomCreate, RoomRead, RoomUpdate

router = APIRouter(tags=["Rooms"])


@router.get("/hotels/{hotel_id}/rooms", response_model=list[RoomRead])
async def list_by_hotel(hotel_id: int, service: RoomServiceDep):
    return await service.list_rooms_by_hotel(hotel_id=hotel_id)


@router.post(
    "/hotels/{hotel_id}/rooms",
    response_model=RoomRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_room(hotel_id: int, payload: RoomCreate, service: RoomServiceDep):
    return await service.create_room(hotel_id, payload)


@router.get("/rooms/{room_id}", response_model=RoomRead)
async def get_room(room_id: int, service: RoomServiceDep):
    return await service.get_room(room_id)


@router.patch("/rooms/{room_id}", response_model=RoomRead)
async def update_room(room_id: int, payload: RoomUpdate, service: RoomServiceDep):
    return await service.update_room(room_id, payload)


@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int, service: RoomServiceDep):
    await service.delete_room(room_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
