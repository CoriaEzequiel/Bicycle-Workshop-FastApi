from fastapi import APIRouter, Depends, HTTPException
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import ProductService
from app.api.deps import get_product_service
from app.core.security import require_roles

router = APIRouter()

@router.get("/", response_model=list[ProductOut])
async def list_products(service: ProductService = Depends(get_product_service)):
    return await service.list()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    product = await service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut, dependencies=[Depends(require_roles("admin", "superadmin"))])
async def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    return await service.create(product)

@router.put("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_roles("admin", "superadmin"))])
async def update_product(product_id: int, product: ProductUpdate, service: ProductService = Depends(get_product_service)):
    updated_product = await service.update(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", status_code=204, dependencies=[Depends(require_roles("admin", "superadmin"))])
async def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    await service.delete(product_id)
    return
