from fastapi import FastAPI
from app.api import products, service_bikes  # rutas

app = FastAPI(title="Bicicletos API")



# routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(service_bikes.router, prefix="/service_bikes", tags=["ServiceBikes"])

@app.get("/")
async def root():
    return {"message": "Bicicletos API funcionando "}