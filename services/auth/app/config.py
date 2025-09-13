import os

JWT_SECRET = os.getenv("JWT_SECRET", "jwt-test")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET", "jwt-refresh-test")
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN", "15"))
REFRESH_TTL_MIN = int(os.getenv("REFRESH_TTL_MIN", "10080"))  # 7 giorni

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://app:app@postgres:5432/notes")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
