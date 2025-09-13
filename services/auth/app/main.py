from fastapi import FastAPI
from .database import engine, Base
from .routers_auth import router as auth_router

app = FastAPI(title="Auth API")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
async def readyz():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
