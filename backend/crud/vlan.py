from sqlalchemy.orm import Session
from backend.models.vlan import Vlan
from backend.schemas.vlan import VlanCreate, VlanUpdate
from backend.services.cisco_executor import execute_commands


# COMMAND BUILDER -----------------------------------------
def build_vlan_commands(vlan: Vlan, mode: str):
    if mode == "create":
        return [
            f"vlan {vlan.vlan_id}",
            f"name {vlan.vlan_name}"
        ]
    else:  # remove
        return [
            f"no vlan {vlan.vlan_id}"
        ]


# CRUD ------------------------------------------------------
def create_vlan(db: Session, data: VlanCreate):
    new = Vlan(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    commands = build_vlan_commands(new, "create")
    execute_commands(db, new.router_id, commands)

    return new


def get_vlans_by_router(db: Session, router_id: int):
    return db.query(Vlan).filter(Vlan.router_id == router_id).all()


def update_vlan(db: Session, vlan_id: int, data: VlanUpdate):
    vlan = db.query(Vlan).filter(Vlan.id == vlan_id).first()
    if not vlan:
        return None

    old = Vlan(**vlan.__dict__)

    for key, value in data.dict().items():
        setattr(vlan, key, value)

    db.commit()
    db.refresh(vlan)

    # Remove old config
    execute_commands(db, vlan.router_id, build_vlan_commands(old, "remove"))

    # Apply new config
    execute_commands(db, vlan.router_id, build_vlan_commands(vlan, "create"))

    return vlan


def delete_vlan(db: Session, vlan_id: int):
    vlan = db.query(Vlan).filter(Vlan.id == vlan_id).first()
    if not vlan:
        return False

    execute_commands(db, vlan.router_id, build_vlan_commands(vlan, "remove"))

    db.delete(vlan)
    db.commit()
    return True
