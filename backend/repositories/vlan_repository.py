from sqlalchemy.orm import Session
from backend.models.vlan import Vlan

class VlanRepository:

    @staticmethod
    def create(db: Session, data):
        vlan = Vlan(**data)
        db.add(vlan)
        db.commit()
        db.refresh(vlan)
        return vlan

    @staticmethod
    def get_all(db: Session):
        return db.query(Vlan).all()

    @staticmethod
    def get_by_router(db: Session, router_id: int):
        return db.query(Vlan).filter(Vlan.router_id == router_id).all()

    @staticmethod
    def update(db: Session, vlan_id: int, data):
        vlan = db.query(Vlan).filter(Vlan.id == vlan_id).first()
        if not vlan:
            return None
        for key, value in data.items():
            setattr(vlan, key, value)
        db.commit()
        db.refresh(vlan)
        return vlan

    @staticmethod
    def delete(db: Session, vlan_id: int):
        vlan = db.query(Vlan).filter(Vlan.id == vlan_id).first()
        if not vlan:
            return False
        db.delete(vlan)
        db.commit()
        return True
