# services/dhcp.py

from backend.services.router import send_to_router
from pydantic import BaseModel, Field
from typing import Optional, List


# -----------------------------
# MODELO PROFISSIONAL DHCP
# -----------------------------
class ExcludedRange(BaseModel):
    start_ip: str
    end_ip: Optional[str] = None  # pode excluir só 1 IP ou um range


class DhcpConfig(BaseModel):
    pool_name: str = Field(..., min_length=1)
    network: str
    mask: str
    gateway: str
    dns_primary: str
    dns_secondary: Optional[str] = None
    lease_days: Optional[int] = 1
    lease_hours: Optional[int] = 0
    lease_minutes: Optional[int] = 0
    excluded_ranges: Optional[List[ExcludedRange]] = None
    remark: Optional[str] = None


# -----------------------------
# FUNÇÃO DE CONFIGURAÇÃO DHCP
# -----------------------------
def configure_dhcp(cfg: DhcpConfig):
    """Configura DHCP completo no roteador Cisco"""

    commands = []

    # 1. Excluir faixas (antes do pool)
    if cfg.excluded_ranges:
        for r in cfg.excluded_ranges:
            if r.end_ip:
                commands.append(f"ip dhcp excluded-address {r.start_ip} {r.end_ip}")
            else:
                commands.append(f"ip dhcp excluded-address {r.start_ip}")

    # 2. Criar o pool DHCP
    commands.append(f"ip dhcp pool {cfg.pool_name}")

    # 3. Configurar rede e máscara
    commands.append(f"network {cfg.network} {cfg.mask}")

    # 4. Default gateway
    commands.append(f"default-router {cfg.gateway}")

    # 5. DNS primário e secundário
    dns_cmd = f"dns-server {cfg.dns_primary}"
    if cfg.dns_secondary:
        dns_cmd += f" {cfg.dns_secondary}"
    commands.append(dns_cmd)

    # 6. Lease time
    commands.append(
        f"lease {cfg.lease_days} {cfg.lease_hours} {cfg.lease_minutes}"
    )

    # 7. Remark opcional
    if cfg.remark:
        commands.append(f"remark {cfg.remark}")

    return send_to_router(commands)
