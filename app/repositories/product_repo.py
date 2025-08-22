from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> list[Product]:
        res = await self.session.execute(select(Product))
        return list(res.scalars().all())

    async def create(self, data: ProductCreate) -> Product:
        obj = Product(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, product_id: int, data: ProductUpdate) -> Product | None:
        obj = await self.session.get(Product, product_id)
        if not obj:
            return None
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
