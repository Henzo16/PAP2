from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repositories.acl_repository import AclRepository
from backend.services.acl import configure_standard_acl, configure_extended_acl, configure_named_acl

router = APIRouter(prefix="/api/acl", tags=["ACL"])

@router.post("/")
def create_acl(data: dict, db: Session = Depends(get_db)):
    acl = AclRepository.create(db, data)

    if acl.tipo == "standard":
        configure_standard_acl(acl)
    elif acl.tipo == "extended":
        configure_extended_acl(acl)
    elif acl.tipo == "named":
        configure_named_acl(acl)

    return acl

@router.get("/{router_id}")
def list_acl(router_id: int, db: Session = Depends(get_db)):
    return AclRepository.get_by_router(db, router_id)

@router.put("/{acl_id}")
def update_acl(acl_id: int, data: dict, db: Session = Depends(get_db)):
    acl = AclRepository.update(db, acl_id, data)
    if not acl:
        raise HTTPException(404, "ACL não encontrada")

    if acl.tipo == "standard":
        configure_standard_acl(acl)
    elif acl.tipo == "extended":
        configure_extended_acl(acl)
    elif acl.tipo == "named":
        configure_named_acl(acl)

    return acl

@router.delete("/{acl_id}")
def delete_acl(acl_id: int, db: Session = Depends(get_db)):
    deleted = AclRepository.delete(db, acl_id)
    if not deleted:
        raise HTTPException(404, "ACL não encontrada")
    return {"message": "ACL removida com sucesso"}
