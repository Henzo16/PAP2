from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repositories.nat_repository import NatRepository
from backend.services.nat import configure_static_nat, configure_dynamic_nat, configure_nat_overload

router = APIRouter(prefix="/api/nat", tags=["NAT"])

@router.post("/")
def create_nat(data: dict, db: Session = Depends(get_db)):
    nat = NatRepository.create(db, data)

    # Envia comandos para o roteador real
    if nat.tipo == "static":
        configure_static_nat(nat)
    elif nat.tipo == "dynamic":
        configure_dynamic_nat(nat)
    elif nat.tipo == "overload":
        configure_nat_overload(nat)

    return nat

@router.get("/{router_id}")
def list_nat(router_id: int, db: Session = Depends(get_db)):
    return NatRepository.get_by_router(db, router_id)

@router.put("/{nat_id}")
def update_nat(nat_id: int, data: dict, db: Session = Depends(get_db)):
    nat = NatRepository.update(db, nat_id, data)
    if not nat:
        raise HTTPException(404, "NAT não encontrada")

    if nat.tipo == "static":
        configure_static_nat(nat)
    elif nat.tipo == "dynamic":
        configure_dynamic_nat(nat)
    elif nat.tipo == "overload":
        configure_nat_overload(nat)

    return nat

@router.delete("/{nat_id}")
def delete_nat(nat_id: int, db: Session = Depends(get_db)):
    deleted = NatRepository.delete(db, nat_id)
    if not deleted:
        raise HTTPException(404, "NAT não encontrada")
    return {"message": "NAT removida com sucesso"}
