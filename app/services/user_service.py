from app.repositories.user_repo import UserRepository
from app.repositories.role_repo import RoleRepository
from app.schemas.user import UserCreate, UserUpdate
from app.db.models.user import User
from app.db.models.user_role import Role

class UserService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.user_repo.get_by_id(user_id)

    async def get_by_auth0_sub(self, auth0_sub: str) -> User | None:
        return await self.user_repo.get_by_auth0_sub(auth0_sub)

    async def create(self, data: UserCreate) -> User:
        return await self.user_repo.create(data)

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        return await self.user_repo.update(user_id, data)

    async def assign_role(self, user_id: int, role_name: str) -> User | None:
        user = await self.user_repo.get_by_id(user_id)
        role = await self.role_repo.get_by_name(role_name)
        if user and role:
            await self.user_repo.assign_role(user, role)
            return user
        return None
