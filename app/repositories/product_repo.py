from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)

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
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, product_id: int) -> None:
        obj = await self.session.get(Product, product_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
