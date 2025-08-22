from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User, UserRole, Role
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_auth0_sub(self, auth0_sub: str) -> User | None:
        res = await self.session.execute(select(User).where(User.auth0_sub == auth0_sub))
        return res.scalars().first()

    async def create(self, data: UserCreate) -> User:
        obj = User(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        obj = await self.session.get(User, user_id)
        if not obj:
            return None
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj