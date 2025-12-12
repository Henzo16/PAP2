from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.router_repository import RouterRepository
from services.router_auto_detect import detect_router

# Router principal para CRUD
router = APIRouter(prefix="/api/routers", tags=["Roteadores"])


# ---------- CRUD DE ROTEADORES ----------

@router.post("/")
def create_router(data: dict, db: Session = Depends(get_db)):
    return RouterRepository.create(db, data)


@router.get("/")
def list_routers(db: Session = Depends(get_db)):
    return RouterRepository.get_all(db)


@router.get("/{router_id}")
def get_router(router_id: int, db: Session = Depends(get_db)):
    r = RouterRepository.get_by_id(db, router_id)
    if not r:
        raise HTTPException(404, "Roteador não encontrado")
    return r


@router.put("/{router_id}")
def update_router(router_id: int, data: dict, db: Session = Depends(get_db)):
    updated = RouterRepository.update(db, router_id, data)
    if not updated:
        raise HTTPException(404, "Roteador não encontrado")
    return updated


@router.delete("/{router_id}")
def delete_router(router_id: int, db: Session = Depends(get_db)):
    deleted = RouterRepository.delete(db, router_id)
    if not deleted:
        raise HTTPException(404, "Roteador não encontrado")
    return {"message": "Roteador removido com sucesso"}


# ---------- AUTO-DETECÇÃO DE ROUTER ----------
@router.get("/auto-detect")
def auto_detect(username: str, password: str, db: Session = Depends(get_db)):
    result = detect_router(db, username, password)
    return result
