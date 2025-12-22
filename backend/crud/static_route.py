from sqlalchemy.orm import Session
from backend.models.static_route import StaticRoute
from backend.schemas.static_route import StaticRouteCreate, StaticRouteUpdate
from backend.services.cisco_static_builder import build_static_route_commands
from backend.services.cisco_executor import execute_commands


def create_static_route(db: Session, data: StaticRouteCreate):
    new = StaticRoute(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    commands = build_static_route_commands(new, "create")
    execute_commands(db, new.router_id, commands)

    return new


def get_static_routes_by_router(db: Session, router_id: int):
    return db.query(StaticRoute).filter(StaticRoute.router_id == router_id).all()


def update_static_route(db: Session, route_id: int, data: StaticRouteUpdate):
    route = db.query(StaticRoute).filter(StaticRoute.id == route_id).first()
    if not route:
        return None

    # Backup da rota antiga para remover do roteador
    old_route = StaticRoute(**route.__dict__)

    for key, value in data.dict().items():
        if value is not None:
            setattr(route, key, value)

    db.commit()
    db.refresh(route)

    # Remover rota antiga e criar nova no roteador
    execute_commands(db, route.router_id, build_static_route_commands(old_route, "remove"))
    execute_commands(db, route.router_id, build_static_route_commands(route, "create"))

    return route


def delete_static_route(db: Session, route_id: int):
    route = db.query(StaticRoute).filter(StaticRoute.id == route_id).first()
    if not route:
        return False

    execute_commands(db, route.router_id, build_static_route_commands(route, "remove"))

    db.delete(route)
    db.commit()
    return True
