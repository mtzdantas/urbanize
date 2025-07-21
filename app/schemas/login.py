from pydantic import BaseModel, EmailStr

class LoginCreate(BaseModel):
    username: str
    senha: str

class LoginResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

