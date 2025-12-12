from pydantic import BaseModel

class StaticRouteBase(BaseModel):
    network: str
    mask: str
    next_hop: str


class StaticRouteCreate(StaticRouteBase):
    router_id: int


class StaticRouteUpdate(BaseModel):
    network: str | None = None
    mask: str | None = None
    next_hop: str | None = None


class StaticRouteOut(StaticRouteBase):
    id: int
    router_id: int

    class Config:
        from_attributes = True
