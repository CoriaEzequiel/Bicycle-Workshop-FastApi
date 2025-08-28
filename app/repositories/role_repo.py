from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user_role import Role
from app.schemas.role import RoleCreate, RoleUpdate

class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Role]:
        res = await self.session.execute(select(Role))
        return list(res.scalars().all())

    async def get_by_name(self, name: str) -> Role | None:
        res = await self.session.execute(select(Role).where(Role.name == name))
        return res.scalars().first()

    async def create(self, data: RoleCreate) -> Role:
        obj = Role(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, role_name: str, data: RoleUpdate) -> Role | None:
        obj = await self.get_by_name(role_name)
        if not obj:
            return None
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, role_name: str) -> None:
        await self.session.execute(delete(Role).where(Role.name == role_name))
        await self.session.commit()
