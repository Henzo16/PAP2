from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str

    class Config:
        from_attributes = True
