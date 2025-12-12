from pydantic import BaseModel

class AclBase(BaseModel):
    acl_type: str  # standard | extended | named
    action: str
    ip_address: str | None = None
    wildcard: str | None = None
    protocol: str | None = None
    acl_number: int | None = None
    dest_ip: str | None = None
    dest_wildcard: str | None = None
    acl_name: str | None = None


class AclCreate(AclBase):
    router_id: int


class AclUpdate(AclBase):
    pass


class AclOut(AclBase):
    id: int
    router_id: int

    class Config:
        from_attributes = True
