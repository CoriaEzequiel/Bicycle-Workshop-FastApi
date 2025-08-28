from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.service_bike import ServiceBikeCreate, ServiceBikeRead, ServiceBikeUpdate
from app.services.service_bike_service import ServiceBikeService
from app.api.deps import get_service_bike_service, get_current_user
from app.core.security import require_roles
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=list[ServiceBikeRead], dependencies=[Depends(require_roles("admin", "superadmin"))])
async def list_service_bikes(service: ServiceBikeService = Depends(get_service_bike_service)):
    return await service.list()

@router.get("/{service_bike_id}", response_model=ServiceBikeRead)
async def get_service_bike(
    service_bike_id: int,
    service: ServiceBikeService = Depends(get_service_bike_service),
    current_user: User = Depends(get_current_user)
):
    service_bike = await service.get_by_id(service_bike_id)
    if not service_bike:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ServiceBike not found")

    # checkéo si el rol es Admin o SuperAdmin
    user_roles = [role.role_name for role in current_user.roles]
    if service_bike.user_id != current_user.id and not any(role in user_roles for role in ["admin", "superadmin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return service_bike

@router.post("/", response_model=ServiceBikeRead)
async def create_service_bike(
    service_bike_data: ServiceBikeCreate,
    service: ServiceBikeService = Depends(get_service_bike_service),
    current_user: User = Depends(get_current_user)
):
    service_bike_data.user_id = current_user.id
    return await service.create(service_bike_data)

@router.put("/{service_bike_id}", response_model=ServiceBikeRead, dependencies=[Depends(require_roles("admin", "superadmin"))])
async def update_service_bike(service_bike_id: int, service_bike: ServiceBikeUpdate, service: ServiceBikeService = Depends(get_service_bike_service)):
    updated_service_bike = await service.update(service_bike_id, service_bike)
    if not updated_service_bike:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ServiceBike not found")
    return updated_service_bike

@router.delete("/{service_bike_id}", status_code=204, dependencies=[Depends(require_roles("superadmin"))])
async def delete_service_bike(service_bike_id: int, service: ServiceBikeService = Depends(get_service_bike_service)):
    await service.delete(service_bike_id)
    return
