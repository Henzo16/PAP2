from sqlalchemy.orm import Session
from models.acl import Acl

class AclRepository:

    @staticmethod
    def create(db: Session, data):
        acl = Acl(**data)
        db.add(acl)
        db.commit()
        db.refresh(acl)
        return acl

    @staticmethod
    def get_all(db: Session):
        return db.query(Acl).all()

    @staticmethod
    def get_by_router(db: Session, router_id: int):
        return db.query(Acl).filter(Acl.router_id == router_id).all()

    @staticmethod
    def update(db: Session, acl_id: int, data):
        acl = db.query(Acl).filter(Acl.id == acl_id).first()
        if not acl:
            return None
        for key, value in data.items():
            setattr(acl, key, value)
        db.commit()
        db.refresh(acl)
        return acl

    @staticmethod
    def delete(db: Session, acl_id: int):
        acl = db.query(Acl).filter(Acl.id == acl_id).first()
        if not acl:
            return False
        db.delete(acl)
        db.commit()
        return True
