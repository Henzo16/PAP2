from sqlalchemy.orm import Session
from backend.models.router import Roteador

class RouterRepository:

    @staticmethod
    def create(db: Session, router_data):
        router = Roteador(**router_data)
        db.add(router)
        db.commit()
        db.refresh(router)
        return router

    @staticmethod
    def get_all(db: Session):
        return db.query(Roteador).all()

    @staticmethod
    def get_by_id(db: Session, router_id: int):
        return db.query(Roteador).filter(Roteador.id == router_id).first()

    @staticmethod
    def update(db: Session, router_id: int, update_data):
        router = db.query(Roteador).filter(Roteador.id == router_id).first()
        if not router:
            return None
        for key, value in update_data.items():
            setattr(router, key, value)
        db.commit()
        db.refresh(router)
        return router

    @staticmethod
    def delete(db: Session, router_id: int):
        router = db.query(Roteador).filter(Roteador.id == router_id).first()
        if not router:
            return False
        db.delete(router)
        db.commit()
        return True
