from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repositories.vlan_repository import VlanRepository
from backend.services.vlan import configure_vlan

router = APIRouter(prefix="/api/vlan", tags=["VLAN"])

@router.post("/")
def create_vlan(data: dict, db: Session = Depends(get_db)):
    vlan = VlanRepository.create(db, data)
    configure_vlan(data)
    return vlan

@router.get("/{router_id}")
def get_vlans(router_id: int, db: Session = Depends(get_db)):
    return VlanRepository.get_by_router(db, router_id)

@router.put("/{vlan_id}")
def update_vlan(vlan_id: int, data: dict, db: Session = Depends(get_db)):
    updated = VlanRepository.update(db, vlan_id, data)
    if not updated:
        raise HTTPException(404, "VLAN não encontrada")
    configure_vlan(data)
    return updated

@router.delete("/{vlan_id}")
def delete_vlan(vlan_id: int, db: Session = Depends(get_db)):
    deleted = VlanRepository.delete(db, vlan_id)
    if not deleted:
        raise HTTPException(404, "VLAN não encontrada")
    return {"message": "VLAN removida"}
