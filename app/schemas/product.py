from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    title: str
    overview: str
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

    model_config = ConfigDict(from_attributes=True)
