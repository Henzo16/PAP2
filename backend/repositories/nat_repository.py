from sqlalchemy.orm import Session
from backend.models.nat import NatConfig

class NatRepository:

    @staticmethod
    def create(db: Session, data):
        nat = NatConfig(**data)
        db.add(nat)
        db.commit()
        db.refresh(nat)
        return nat

    @staticmethod
    def get_all(db: Session):
        return db.query(NatConfig).all()

    @staticmethod
    def get_by_router(db: Session, router_id: int):
        return db.query(NatConfig).filter(NatConfig.router_id == router_id).all()

    @staticmethod
    def update(db: Session, nat_id: int, data):
        nat = db.query(NatConfig).filter(NatConfig.id == nat_id).first()
        if not nat:
            return None
        for key, value in data.items():
            setattr(nat, key, value)
        db.commit()
        db.refresh(nat)
        return nat

    @staticmethod
    def delete(db: Session, nat_id: int):
        nat = db.query(NatConfig).filter(NatConfig.id == nat_id).first()
        if not nat:
            return False
        db.delete(nat)
        db.commit()
        return True
