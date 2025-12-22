from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repositories.dhcp_repository import DhcpRepository
from backend.services.dhcp import configure_dhcp

router = APIRouter(prefix="/api/dhcp", tags=["DHCP"])

@router.post("/")
def create_dhcp(data: dict, db: Session = Depends(get_db)):
    dhcp = DhcpRepository.create(db, data)
    configure_dhcp(data)  # Envia config para o roteador real
    return dhcp

@router.get("/{router_id}")
def get_dhcp_by_router(router_id: int, db: Session = Depends(get_db)):
    return DhcpRepository.get_by_router(db, router_id)

@router.put("/{dhcp_id}")
def update_dhcp(dhcp_id: int, data: dict, db: Session = Depends(get_db)):
    updated = DhcpRepository.update(db, dhcp_id, data)
    if not updated:
        raise HTTPException(404, "Config DHCP não encontrada")
    configure_dhcp(data)
    return updated

@router.delete("/{dhcp_id}")
def delete_dhcp(dhcp_id: int, db: Session = Depends(get_db)):
    deleted = DhcpRepository.delete(db, dhcp_id)
    if not deleted:
        raise HTTPException(404, "Config DHCP não encontrada")
    return {"message": "DHCP removido com sucesso"}
