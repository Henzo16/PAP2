from pydantic import BaseModel
from typing import Optional

class NatBase(BaseModel):
    type: str  # estatico, dinamico, overload
    internal_ip: Optional[str] = None
    external_ip: Optional[str] = None
    access_list: Optional[str] = None
    pool_name: Optional[str] = None
    outside_interface: Optional[str] = None

class NatCreate(NatBase):
    router_id: int

class NatUpdate(NatBase):
    pass

class NatOut(NatBase):
    id: int
    router_id: int

    class Config:
        from_attributes = True
