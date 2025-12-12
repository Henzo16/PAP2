from sqlalchemy.orm import Session
from models.static_route import StaticRoute

class StaticRouteRepository:

    @staticmethod
    def create(db: Session, data):
        route = StaticRoute(**data)
        db.add(route)
        db.commit()
        db.refresh(route)
        return route

    @staticmethod
    def get_all(db: Session):
        return db.query(StaticRoute).all()

    @staticmethod
    def get_by_router(db: Session, router_id: int):
        return db.query(StaticRoute).filter(StaticRoute.router_id == router_id).all()

    @staticmethod
    def update(db: Session, route_id: int, data):
        route = db.query(StaticRoute).filter(StaticRoute.id == route_id).first()
        if not route:
            return None
        for key, value in data.items():
            setattr(route, key, value)
        db.commit()
        db.refresh(route)
        return route

    @staticmethod
    def delete(db: Session, route_id: int):
        route = db.query(StaticRoute).filter(StaticRoute.id == route_id).first()
        if not route:
            return False
        db.delete(route)
        db.commit()
        return True
