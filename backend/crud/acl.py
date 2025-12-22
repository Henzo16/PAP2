from sqlalchemy.orm import Session
from backend.models.acl import Acl
from backend.schemas.acl import AclCreate, AclUpdate
from backend.services.cisco_acl_builder import build_acl_commands
from backend.services.cisco_executor import execute_commands


def create_acl(db: Session, data: AclCreate):
    new = Acl(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    cmds = build_acl_commands(new, "create")
    execute_commands(db, new.router_id, cmds)

    return new


def get_acls_by_router(db: Session, router_id: int):
    return db.query(Acl).filter(Acl.router_id == router_id).all()


def update_acl(db: Session, acl_id: int, data: AclUpdate):
    acl = db.query(Acl).filter(Acl.id == acl_id).first()
    if not acl:
        return None

    old_acl = Acl(**acl.__dict__)

    for key, value in data.dict().items():
        setattr(acl, key, value)

    db.commit()
    db.refresh(acl)

    # Remove old ACL
    execute_commands(db, acl.router_id, build_acl_commands(old_acl, "remove"))
    # Apply new ACL
    execute_commands(db, acl.router_id, build_acl_commands(acl, "create"))

    return acl


def delete_acl(db: Session, acl_id: int):
    acl = db.query(Acl).filter(Acl.id == acl_id).first()
    if not acl:
        return False

    execute_commands(db, acl.router_id, build_acl_commands(acl, "remove"))

    db.delete(acl)
    db.commit()
    return True
