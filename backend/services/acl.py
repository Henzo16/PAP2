from pydantic import BaseModel, Field
from typing import Optional
from services.router import send_to_router

# -----------------------------
# 1. ACL PADRÃO (Standard ACL)
# -----------------------------

class StandardAclRule(BaseModel):
    acl_number: int
    ip_address: str
    action: str = Field(..., pattern="^(permit|deny)$")

def configure_standard_acl(acl: StandardAclRule):
    commands = [
        f"access-list {acl.acl_number} {acl.action} {acl.ip_address} 0.0.0.255"
    ]
    return send_to_router(commands)


# -----------------------------
# 2. ACL ESTENDIDA (Extended ACL)
# -----------------------------

class ExtendedAclRule(BaseModel):
    acl_number: int
    source_ip: str
    source_wildcard: str
    dest_ip: str
    dest_wildcard: str
    protocol: str = Field(..., pattern="^(tcp|udp|ip)$")
    action: str = Field(..., pattern="^(permit|deny)$")

def configure_extended_acl(acl: ExtendedAclRule):
    commands = [
        f"access-list {acl.acl_number} {acl.action} {acl.protocol} "
        f"{acl.source_ip} {acl.source_wildcard} {acl.dest_ip} {acl.dest_wildcard}"
    ]
    return send_to_router(commands)


# -----------------------------
# 3. ACL NOMEADA (Named ACL)
# -----------------------------

class NamedAclRule(BaseModel):
    acl_name: str
    action: str = Field(..., pattern="^(permit|deny)$")
    ip_address: str

def configure_named_acl(acl: NamedAclRule):
    commands = [
        f"ip access-list extended {acl.acl_name}",
        f"{acl.action} {acl.ip_address} 0.0.0.255",
    ]
    return send_to_router(commands)
