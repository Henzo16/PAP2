from sqlalchemy.orm import Session
from backend.models.ospf import OspfRoute

class OspfRepository:

    @staticmethod
    def create(db: Session, data):
        ospf = OspfRoute(**data)
        db.add(ospf)
        db.commit()
        db.refresh(ospf)
        return ospf

    @staticmethod
    def get_all(db: Session):
        return db.query(OspfRoute).all()

    @staticmethod
    def get_by_router(db: Session, router_id: int):
        return db.query(OspfRoute).filter(OspfRoute.router_id == router_id).all()

    @staticmethod
    def update(db: Session, ospf_id: int, data):
        ospf = db.query(OspfRoute).filter(OspfRoute.id == ospf_id).first()
        if not ospf:
            return None
        for key, value in data.items():
            setattr(ospf, key, value)
        db.commit()
        db.refresh(ospf)
        return ospf

    @staticmethod
    def delete(db: Session, ospf_id: int):
        ospf = db.query(OspfRoute).filter(OspfRoute.id == ospf_id).first()
        if not ospf:
            return False
        db.delete(ospf)
        db.commit()
        return True
