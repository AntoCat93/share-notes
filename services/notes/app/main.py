from fastapi import FastAPI
from app.health import router as health_router

app = FastAPI(title="Notes API")
app.include_router(health_router)