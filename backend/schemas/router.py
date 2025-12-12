from pydantic import BaseModel

class RoteadorBase(BaseModel):
    hostname: str
    ip_address: str
    username: str
    password: str
    model: str

class RoteadorCreate(RoteadorBase):
    pass

class RoteadorResponse(RoteadorBase):
    id: int
    status: str

    class Config:
        from_attributes = True
