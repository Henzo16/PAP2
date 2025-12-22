from sqlalchemy.orm import Session
from backend.models.dhcp import DhcpConfig
from backend.schemas.dhcp import DhcpCreate, DhcpUpdate
from backend.services.cisco_executor import execute_commands

# -----------------------------
# CREATE DHCP
# -----------------------------
def create_dhcp(db: Session, data: DhcpCreate):
    # 1. Cria no banco
    new = DhcpConfig(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    # 2. Comandos Cisco
    commands = [
        f"ip dhcp pool {new.pool_name}",
        f"network {new.network} {new.mask}",
        f"default-router {new.gateway}",
        f"dns-server {new.dns}"
    ]

    # 3. Executa no roteador
    execute_commands(db, new.router_id, commands)

    return new


# -----------------------------
# LISTAR DHCP POR ROTEADOR
# -----------------------------
def get_dhcp_by_router(db: Session, router_id: int):
    return db.query(DhcpConfig).filter(DhcpConfig.router_id == router_id).all()


# -----------------------------
# UPDATE DHCP
# -----------------------------
def update_dhcp(db: Session, dhcp_id: int, data: DhcpUpdate):
    dhcp = db.query(DhcpConfig).filter(DhcpConfig.id == dhcp_id).first()
    if not dhcp:
        return None

    # Guarda o nome antigo para remover config anterior
    old_pool = dhcp.pool_name

    # Atualiza no banco
    for key, value in data.dict().items():
        setattr(dhcp, key, value)

    db.commit()
    db.refresh(dhcp)

    # Remove configuração antiga
    remove_commands = [
        f"no ip dhcp pool {old_pool}"
    ]
    execute_commands(db, dhcp.router_id, remove_commands)

    # Cria nova configuração
    new_commands = [
        f"ip dhcp pool {dhcp.pool_name}",
        f"network {dhcp.network} {dhcp.mask}",
        f"default-router {dhcp.gateway}",
        f"dns-server {dhcp.dns}"
    ]
    execute_commands(db, dhcp.router_id, new_commands)

    return dhcp


# -----------------------------
# DELETE DHCP
# -----------------------------
def delete_dhcp(db: Session, dhcp_id: int):
    dhcp = db.query(DhcpConfig).filter(DhcpConfig.id == dhcp_id).first()
    if not dhcp:
        return False

    # Comando Cisco para remover pool
    commands = [f"no ip dhcp pool {dhcp.pool_name}"]

    execute_commands(db, dhcp.router_id, commands)

    # Remover do banco
    db.delete(dhcp)
    db.commit()

    return True
