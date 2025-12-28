from pydantic import BaseModel, EmailStr
from datetime import datetime

# ---------------------------
# Request/response models
# ---------------------------

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    api_key: str
    expires_at: datetime | None

class ItemOut(BaseModel):
    id: int
    name: str
    price: float