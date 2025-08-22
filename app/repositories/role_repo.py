from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import Role

class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Role]:
        res = await self.session.execute(select(Role))
        return list(res.scalars().all())

    async def get_by_name(self, name: str) -> Role | None:
        res = await self.session.execute(select(Role).where(Role.name == name))
        return res.scalars().first()
