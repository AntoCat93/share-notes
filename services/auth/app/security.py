from datetime import datetime, timedelta
from jose import jwt
from passlib.hash import bcrypt
from app.config import JWT_SECRET, JWT_REFRESH_SECRET, ACCESS_TTL_MIN, REFRESH_TTL_MIN

def hash_password(pwd: str) -> str:
    return bcrypt.hash(pwd)

def verify_password(pwd: str, pwd_hash: str) -> bool:
    return bcrypt.verify(pwd, pwd_hash)

def make_access_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TTL_MIN)
    return jwt.encode({"sub": sub, "exp": exp}, JWT_SECRET, algorithm="HS256")

def make_refresh_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=REFRESH_TTL_MIN)
    return jwt.encode({"sub": sub, "exp": exp}, JWT_REFRESH_SECRET, algorithm="HS256")
