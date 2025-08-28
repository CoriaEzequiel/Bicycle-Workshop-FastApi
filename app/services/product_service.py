from app.repositories.product_repo import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.db.models.product import Product

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.repo.get_by_id(product_id)

    async def list(self) -> list[Product]:
        return await self.repo.list()

    async def create(self, data: ProductCreate) -> Product:
        return await self.repo.create(data)

    async def update(self, product_id: int, data: ProductUpdate) -> Product | None:
        return await self.repo.update(product_id, data)

    async def delete(self, product_id: int) -> None:
        return await self.repo.delete(product_id)
