from fastapi import APIRouter, Depends, Response, status

from app.dependencies import AmenityServiceDep, get_current_admin
from app.schemas.amenities import AmenityCreate, AmenityRead

router = APIRouter(prefix="/amenities", tags=["Amenities"])


@router.get("/", response_model=list[AmenityRead])
async def get_amenities(service: AmenityServiceDep):
    return await service.list_amenities()


@router.post(
    "/",
    response_model=AmenityRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
async def add_amenity(payload: AmenityCreate, service: AmenityServiceDep):
    return await service.add_amenity(payload)


@router.get("/{amenity_id}", response_model=AmenityRead)
async def get_amenity(amenity_id: int, service: AmenityServiceDep):
    return await service.get_amenity(amenity_id)


@router.put(
    "/{amenity_id}",
    response_model=AmenityRead,
    dependencies=[Depends(get_current_admin)],
)
async def update_amenity(
    amenity_id: int, payload: AmenityCreate, service: AmenityServiceDep
):
    return await service.update_amenity(amenity_id, payload)


@router.delete(
    "/{amenity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
async def delete_amenity(amenity_id: int, service: AmenityServiceDep):
    await service.delete_amenity(amenity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
