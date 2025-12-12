# services/routing.py

from services.router import send_to_router
from pydantic import BaseModel, Field
from typing import List, Optional


# -----------------------------
# 1. ROTAS ESTÁTICAS
# -----------------------------
class StaticRoute(BaseModel):
    network: str
    mask: str
    next_hop: str
    distance: Optional[int] = None  # AD opcional
    remark: Optional[str] = None


class StaticRouteConfig(BaseModel):
    routes: List[StaticRoute]


def configure_static_route(cfg: StaticRouteConfig):
    """Configura múltiplas rotas estáticas."""
    commands = []

    for r in cfg.routes:
        if r.remark:
            commands.append(f"! {r.remark}")

        cmd = f"ip route {r.network} {r.mask} {r.next_hop}"
        if r.distance:
            cmd += f" {r.distance}"

        commands.append(cmd)

    return send_to_router(commands)



# -----------------------------
# 2. OSPF AVANÇADO
# -----------------------------
class OspfNetwork(BaseModel):
    network: str
    wildcard: str
    area: str


class OspfConfig(BaseModel):
    process_id: int
    router_id: Optional[str] = None
    passive_interfaces: Optional[List[str]] = None
    networks: List[OspfNetwork]


def configure_ospf(cfg: OspfConfig):
    """Configura OSPF de forma profissional."""
    commands = [f"router ospf {cfg.process_id}"]

    if cfg.router_id:
        commands.append(f"router-id {cfg.router_id}")

    if cfg.passive_interfaces:
        for intf in cfg.passive_interfaces:
            commands.append(f"passive-interface {intf}")

    for net in cfg.networks:
        commands.append(
            f"network {net.network} {net.wildcard} area {net.area}"
        )

    return send_to_router(commands)



# -----------------------------
# 3. INTER-VLAN ROUTING (ROUTER-ON-A-STICK)
# -----------------------------
class SubInterface(BaseModel):
    vlan_id: int
    ip_address: str
    mask: str
    description: Optional[str] = None


class InterVlanRoutingConfig(BaseModel):
    physical_interface: str
    subinterfaces: List[SubInterface]


def configure_inter_vlan_routing(cfg: InterVlanRoutingConfig):
    """Cria várias subinterfaces para roteamento inter-VLAN."""
    commands = []

    # ativar interface física
    commands.append(f"interface {cfg.physical_interface}")
    commands.append("no shutdown")

    for sub in cfg.subinterfaces:
        commands.append(f"interface {cfg.physical_interface}.{sub.vlan_id}")
        commands.append(f"encapsulation dot1Q {sub.vlan_id}")
        commands.append(f"ip address {sub.ip_address} {sub.mask}")

        if sub.description:
            commands.append(f"description {sub.description}")

        commands.append("no shutdown")

    return send_to_router(commands)
