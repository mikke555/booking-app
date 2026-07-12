from typing import Annotated

from fastapi import APIRouter, Body, Response, status

from app.dependencies import HotelFilterDep, HotelServiceDep
from app.schemas.hotels import (
    HotelCreate,
    HotelRead,
    HotelUpdate,
    hotel_create_examples,
)

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get(
    "/",
    response_model=list[HotelRead],
    description="List hotels with at least one room available for the requested dates.",
)
async def list_hotels(service: HotelServiceDep, filters: HotelFilterDep):
    return await service.list_hotels(filters)


@router.post("/", response_model=HotelRead, status_code=status.HTTP_201_CREATED)
async def create_hotel(
    payload: Annotated[HotelCreate, Body(openapi_examples=hotel_create_examples)],
    service: HotelServiceDep,
):
    return await service.add_hotel(payload)


@router.get("/{hotel_id}", response_model=HotelRead)
async def get_hotel(hotel_id: int, service: HotelServiceDep):
    return await service.get_hotel(hotel_id)


@router.patch("/{hotel_id}", response_model=HotelRead)
async def update_hotel(hotel_id: int, payload: HotelUpdate, service: HotelServiceDep):
    return await service.update_hotel(hotel_id, payload)


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int, service: HotelServiceDep):
    await service.delete_hotel(hotel_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
