from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis.asyncio as redis
import jwt
from jwt import InvalidTokenError

from .database import SessionLocal
from .models import User
from .security import hash_password, verify_password, make_access_token, make_refresh_token
from .config import REDIS_URL, JWT_REFRESH_SECRET

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

class UserCreate(BaseModel):
    username: str
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshIn(BaseModel):
    refresh_token: str

async def get_redis():
    r = redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield r
    finally:
        await r.close()

@router.post("/register", status_code=201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=422, detail="username e password richiesti")
    exists = await db.scalar(select(User).where(User.username == payload.username))
    if exists:
        raise HTTPException(status_code=409, detail="username già esistente")
    user = User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user); await db.commit()
    return {"id": user.id, "username": user.username}

@router.post("/login", response_model=TokenPair)
async def login(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await db.scalar(select(User).where(User.username == payload.username))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="credenziali non valide")
    return TokenPair(
        access_token=make_access_token(str(user.id)),
        refresh_token=make_refresh_token(str(user.id)),
    )

@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshIn, r = Depends(get_redis)):
    rt = body.refresh_token
    if await r.sismember("refresh_blacklist", rt):
        raise HTTPException(status_code=401, detail="refresh token revocato")
    try:
        payload = jwt.decode(rt, JWT_REFRESH_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            raise InvalidTokenError("no sub")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="refresh token non valido")
    return TokenPair(
        access_token=make_access_token(sub),
        refresh_token=make_refresh_token(sub),
    )

@router.post("/logout", status_code=204)
async def logout(body: RefreshIn, r = Depends(get_redis)):
    await r.sadd("refresh_blacklist", body.refresh_token)
    return
