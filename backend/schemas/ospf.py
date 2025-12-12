from pydantic import BaseModel

class OspfBase(BaseModel):
    process_id: int
    network: str
    wildcard_mask: str
    area: int


class OspfCreate(OspfBase):
    router_id: int


class OspfUpdate(BaseModel):
    network: str | None = None
    wildcard_mask: str | None = None
    area: int | None = None


class OspfOut(OspfBase):
    id: int
    router_id: int

    class Config:
        from_attributes = True
