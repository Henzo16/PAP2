from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repositories.ospf_repository import OspfRepository
from backend.services.routing import configure_ospf

router = APIRouter(prefix="/api/ospf", tags=["OSPF"])

@router.post("/")
def create_ospf(data: dict, db: Session = Depends(get_db)):
    ospf = OspfRepository.create(db, data)
    configure_ospf(data)
    return ospf

@router.get("/{router_id}")
def list_ospf(router_id: int, db: Session = Depends(get_db)):
    return OspfRepository.get_by_router(db, router_id)

@router.put("/{ospf_id}")
def update_ospf(ospf_id: int, data: dict, db: Session = Depends(get_db)):
    updated = OspfRepository.update(db, ospf_id, data)
    if not updated:
        raise HTTPException(404, "OSPF não encontrado")
    configure_ospf(data)
    return updated

@router.delete("/{ospf_id}")
def delete_ospf(ospf_id: int, db: Session = Depends(get_db)):
    deleted = OspfRepository.delete(db, ospf_id)
    if not deleted:
        raise HTTPException(404, "OSPF não encontrado")
    return {"message": "OSPF removido"}
