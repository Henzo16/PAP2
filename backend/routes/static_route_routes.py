from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_db
from sqlalchemy.orm import Session

from backend.repositories.static_route_repository import StaticRouteRepository
from backend.services.routing import configure_static_route

router = APIRouter(prefix="/api/static-routes", tags=["Static Routes"])

@router.post("/")
def create_route(data: dict, db: Session = Depends(get_db)):
    route = StaticRouteRepository.create(db, data)
    configure_static_route(data)
    return route

@router.get("/{router_id}")
def list_routes(router_id: int, db: Session = Depends(get_db)):
    return StaticRouteRepository.get_by_router(db, router_id)

@router.put("/{route_id}")
def update_route(route_id: int, data: dict, db: Session = Depends(get_db)):
    updated = StaticRouteRepository.update(db, route_id, data)
    if not updated:
        raise HTTPException(404, "Rota não encontrada")
    configure_static_route(data)
    return updated

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    deleted = StaticRouteRepository.delete(db, route_id)
    if not deleted:
        raise HTTPException(404, "Rota não encontrada")
    return {"message": "Rota removida"}
