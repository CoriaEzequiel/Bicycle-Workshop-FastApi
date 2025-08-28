from fastapi import APIRouter
from app.api.routes import products, roles, users, service_bikes

router = APIRouter()

router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(roles.router, prefix="/roles", tags=["roles"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(service_bikes.router, prefix="/service-bikes", tags=["service_bikes"])
