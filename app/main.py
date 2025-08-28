from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Bicicleteria API")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Bicicleteria API is running"}
