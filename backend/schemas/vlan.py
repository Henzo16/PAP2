from pydantic import BaseModel

class VlanBase(BaseModel):
    vlan_id: int
    vlan_name: str

class VlanCreate(VlanBase):
    router_id: int

class VlanUpdate(VlanBase):
    pass

class VlanOut(VlanBase):
    id: int
    router_id: int

    class Config:
        from_attributes = True
