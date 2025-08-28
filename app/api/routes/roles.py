from fastapi import APIRouter, Depends, HTTPException
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.services.role_service import RoleService
from app.api.deps import get_role_service
from app.core.security import require_roles

router = APIRouter()

@router.get("/", response_model=list[RoleRead], dependencies=[Depends(require_roles("admin", "superadmin"))])
async def list_roles(service: RoleService = Depends(get_role_service)):
    return await service.list()

@router.post("/", response_model=RoleRead, dependencies=[Depends(require_roles("superadmin"))])
async def create_role(role: RoleCreate, service: RoleService = Depends(get_role_service)):
    return await service.create(role)

@router.put("/{role_name}", response_model=RoleRead, dependencies=[Depends(require_roles("superadmin"))])
async def update_role(role_name: str, role: RoleUpdate, service: RoleService = Depends(get_role_service)):
    updated_role = await service.update(role_name, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

@router.delete("/{role_name}", status_code=204, dependencies=[Depends(require_roles("superadmin"))])
async def delete_role(role_name: str, service: RoleService = Depends(get_role_service)):
    await service.delete(role_name)
    return
