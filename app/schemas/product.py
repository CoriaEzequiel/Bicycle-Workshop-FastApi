from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    title: str
    overview: str
    drop: int
    size: str
    color: str
    category: str
    stock: bool
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int


model_config = {
"from_attributes": True
}