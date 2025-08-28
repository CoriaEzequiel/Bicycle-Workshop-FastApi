from app.repositories.role_repo import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.db.models.user_role import Role

class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def list(self) -> list[Role]:
        return await self.repo.get_all()

    async def get_by_name(self, name: str) -> Role | None:
        return await self.repo.get_by_name(name)

    async def create(self, data: RoleCreate) -> Role:
        return await self.repo.create(data)

    async def update(self, role_name: str, data: RoleUpdate) -> Role | None:
        return await self.repo.update(role_name, data)

    async def delete(self, role_name: str) -> None:
        return await self.repo.delete(role_name)
