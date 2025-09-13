from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
