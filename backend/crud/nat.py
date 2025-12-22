from sqlalchemy.orm import Session
from backend.models.nat import NatConfig
from backend.schemas.nat import NatCreate, NatUpdate
from backend.services.cisco_executor import execute_commands


# ----------------------------------------------------
# CREATE NAT
# ----------------------------------------------------
def create_nat(db: Session, data: NatCreate):
    new = NatConfig(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    # COMMANDS BASE ON TYPE
    commands = build_nat_commands(new, mode="create")

    execute_commands(db, new.router_id, commands)
    return new


# ----------------------------------------------------
# GET NAT BY ROUTER
# ----------------------------------------------------
def get_nat_by_router(db: Session, router_id: int):
    return db.query(NatConfig).filter(NatConfig.router_id == router_id).all()


# ----------------------------------------------------
# UPDATE NAT
# ----------------------------------------------------
def update_nat(db: Session, nat_id: int, data: NatUpdate):
    nat = db.query(NatConfig).filter(NatConfig.id == nat_id).first()
    if not nat:
        return None

    old_config = nat

    # Update in DB
    for key, value in data.dict().items():
        setattr(nat, key, value)

    db.commit()
    db.refresh(nat)

    # REMOVE OLD CONFIG
    remove_cmds = build_nat_commands(old_config, mode="remove")
    execute_commands(db, nat.router_id, remove_cmds)

    # APPLY NEW CONFIG
    new_cmds = build_nat_commands(nat, mode="create")
    execute_commands(db, nat.router_id, new_cmds)

    return nat


# ----------------------------------------------------
# DELETE NAT
# ----------------------------------------------------
def delete_nat(db: Session, nat_id: int):
    nat = db.query(NatConfig).filter(NatConfig.id == nat_id).first()
    if not nat:
        return False

    cmds = build_nat_commands(nat, mode="remove")
    execute_commands(db, nat.router_id, cmds)

    db.delete(nat)
    db.commit()

    return True


# ----------------------------------------------------
# COMMAND BUILDER (STATIC / DYNAMIC / OVERLOAD)
# ----------------------------------------------------
def build_nat_commands(nat: NatConfig, mode: str):
    cmds = []

    # STATIC NAT
    if nat.type == "static":
        if mode == "create":
            cmds.append(f"ip nat inside source static {nat.internal_ip} {nat.external_ip}")
        else:
            cmds.append(f"no ip nat inside source static {nat.internal_ip} {nat.external_ip}")

    # DYNAMIC NAT
    elif nat.type == "dynamic":
        if mode == "create":
            cmds += [
                f"ip nat pool {nat.pool_name} {nat.external_ip} {nat.external_ip} netmask 255.255.255.0",
                f"ip nat inside source list {nat.access_list} pool {nat.pool_name}"
            ]
        else:
            cmds += [
                f"no ip nat inside source list {nat.access_list} pool {nat.pool_name}",
                f"no ip nat pool {nat.pool_name}"
            ]

    # NAT OVERLOAD (PAT)
    elif nat.type == "overload":
        if mode == "create":
            cmds += [
                f"access-list {nat.access_list} permit any",
                f"ip nat inside source list {nat.access_list} interface {nat.outside_interface} overload"
            ]
        else:
            cmds += [
                f"no ip nat inside source list {nat.access_list} interface {nat.outside_interface} overload",
                f"no access-list {nat.access_list}"
            ]

    return cmds
