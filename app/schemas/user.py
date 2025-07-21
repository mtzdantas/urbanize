from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas.login import LoginCreate, LoginResponse

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    celular: str
    id_login: LoginCreate

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    celular: Optional[str] = None
    id_login: Optional[LoginCreate] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    celular: str
    login: LoginResponse

    class Config:
        orm_mode = True