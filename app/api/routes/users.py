from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.api.deps import get_user_service, get_current_user
from app.core.security import require_roles
from app.db.models.user import User

router = APIRouter()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    # Compruebo si el usuario está solicitando sus propios datos o es un admin/superadmin.
    user_roles = [role.role_name for role in current_user.roles]
    if current_user.id != user_id and not any(role in user_roles for role in ["admin", "superadmin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

@router.post("/{user_id}/assign-role/{role_name}", response_model=UserRead, dependencies=[Depends(require_roles("superadmin"))])
async def assign_role_to_user(user_id: int, role_name: str, service: UserService = Depends(get_user_service)):
    user = await service.assign_role(user_id, role_name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or role not found")
    return user
