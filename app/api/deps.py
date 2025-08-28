from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.product_service import ProductService
from app.repositories.product_repo import ProductRepository
from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from app.services.role_service import RoleService
from app.repositories.role_repo import RoleRepository
from app.services.service_bike_service import ServiceBikeService
from app.repositories.service_bike_repo import ServiceBikeRepository
from app.core.security import validate_jwt
from app.db.models.user import User
from app.schemas.user import UserCreate

def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    repo = ProductRepository(session)
    return ProductService(repo)

def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repo = UserRepository(session)
    role_repo = RoleRepository(session)
    return UserService(user_repo, role_repo)

def get_role_service(session: AsyncSession = Depends(get_session)) -> RoleService:
    repo = RoleRepository(session)
    return RoleService(repo)

def get_service_bike_service(session: AsyncSession = Depends(get_session)) -> ServiceBikeService:
    repo = ServiceBikeRepository(session)
    return ServiceBikeService(repo)

async def get_current_user(
    token: dict = Depends(validate_jwt),
    user_service: UserService = Depends(get_user_service)
) -> User:
    auth0_sub = token.get("sub")
    if not auth0_sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user identifier")

    user = await user_service.get_by_auth0_sub(auth0_sub)
    if not user:
        # Creo usuario si no existe.
        user_email = token.get("email")
        new_user_data = UserCreate(auth0_sub=auth0_sub, email=user_email)
        user = await user_service.create(new_user_data)

        # Assigno rol "Cliente" (Client role)
        try:
            await user_service.assign_role(user.id, "Cliente")
        except Exception as e:
            
            print(f"Could not assign 'Cliente' role to new user {user.id}: {e}")

    return user
