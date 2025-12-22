# services/vlan.py

from backend.services.router import send_to_router
from pydantic import BaseModel, Field
from typing import List, Optional


# -----------------------------
# MODELO DE VLAN INDIVIDUAL
# -----------------------------
class Vlan(BaseModel):
    vlan_id: int = Field(..., ge=1, le=4094)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    svi_ip: Optional[str] = None
    svi_mask: Optional[str] = None


# -----------------------------
# MODELO DE CONFIGURAÇÃO MULTI-VLAN
# -----------------------------
class VlanConfig(BaseModel):
    vlans: List[Vlan]


# -----------------------------
# FUNÇÃO PRINCIPAL
# -----------------------------
def configure_vlan(cfg: VlanConfig):
    """
    Configura múltiplas VLANs e SVIs opcionalmente.
    """

    commands = []

    for vlan in cfg.vlans:
        # Criar VLAN
        commands.append(f"vlan {vlan.vlan_id}")
        commands.append(f"name {vlan.name}")

        if vlan.description:
            commands.append(f"description {vlan.description}")

        # Criar SVI (interface VLAN)
        if vlan.svi_ip and vlan.svi_mask:
            commands.append(f"interface vlan {vlan.vlan_id}")
            commands.append(f"ip address {vlan.svi_ip} {vlan.svi_mask}")
            commands.append("no shutdown")

    return send_to_router(commands)
