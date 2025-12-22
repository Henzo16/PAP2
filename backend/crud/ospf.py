from sqlalchemy.orm import Session
from backend.models.ospf import OspfRoute
from backend.schemas.ospf import OspfCreate, OspfUpdate
from backend.services.cisco_ospf_builder import build_ospf_commands
from backend.services.cisco_executor import execute_commands


def create_ospf(db: Session, data: OspfCreate):
    new = OspfRoute(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    commands = build_ospf_commands(new, "create")
    execute_commands(db, new.router_id, commands)

    return new


def get_ospf_by_router(db: Session, router_id: int):
    return db.query(OspfRoute).filter(OspfRoute.router_id == router_id).all()


def update_ospf(db: Session, ospf_id: int, data: OspfUpdate):
    ospf = db.query(OspfRoute).filter(OspfRoute.id == ospf_id).first()
    if not ospf:
        return None

    old = OspfRoute(**ospf.__dict__)

    for key, value in data.dict().items():
        if value is not None:
            setattr(ospf, key, value)

    db.commit()
    db.refresh(ospf)

    # Remove rota antiga
    execute_commands(db, ospf.router_id, build_ospf_commands(old, "remove"))
    # Adiciona nova rota
    execute_commands(db, ospf.router_id, build_ospf_commands(ospf, "create"))

    return ospf


def delete_ospf(db: Session, ospf_id: int):
    ospf = db.query(OspfRoute).filter(OspfRoute.id == ospf_id).first()
    if not ospf:
        return False

    execute_commands(db, ospf.router_id, build_ospf_commands(ospf, "remove"))

    db.delete(ospf)
    db.commit()

    return True
