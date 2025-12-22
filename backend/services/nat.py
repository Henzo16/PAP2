from backend.services.router import send_to_router
from pydantic import BaseModel, Field
from typing import Optional

# 1. Configuração de NAT Estático
class StaticNatConfig(BaseModel):
    internal_ip: str
    external_ip: str

def configure_static_nat(nat_config: StaticNatConfig):
    """Configura NAT Estático (Static NAT)"""
    commands = [
        f"ip nat inside source static {nat_config.internal_ip} {nat_config.external_ip}"
    ]
    return send_to_router(commands)

# 2. Configuração de NAT Dinâmico
class DynamicNatConfig(BaseModel):
    access_list: str
    pool_name: str

def configure_dynamic_nat(nat_config: DynamicNatConfig):
    """Configura NAT Dinâmico (Dynamic NAT)"""
    commands = [
        f"ip nat inside source list {nat_config.access_list} pool {nat_config.pool_name}"
    ]
    return send_to_router(commands)


# 3. Configuração de NAT Overload / PAT
class NatOverloadConfig(BaseModel):
    access_list: str
    outside_interface: str
    protocol: Optional[str] = Field(default=None, pattern="^(tcp|udp)$")

def configure_nat_overload(nat_config: NatOverloadConfig):
    """Configura NAT Overload (PAT)"""
    commands = [
        f"access-list {nat_config.access_list} permit any",
        f"ip nat inside source list {nat_config.access_list} interface {nat_config.outside_interface} overload"
    ]
    return send_to_router(commands)
