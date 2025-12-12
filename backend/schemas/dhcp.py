from pydantic import BaseModel

class DhcpBase(BaseModel):
    pool_name: str
    network: str
    mask: str
    gateway: str
    dns: str

class DhcpCreate(DhcpBase):
    router_id: int

class DhcpUpdate(DhcpBase):
    pass

class DhcpOut(DhcpBase):
    id: int
    router_id: int

    class Config:
        from_attributes = True
