from fastapi import APIRouter

from app.dependencies import HotelServiceDep

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, service: HotelServiceDep):
    return await service.get_by_id(hotel_id)
