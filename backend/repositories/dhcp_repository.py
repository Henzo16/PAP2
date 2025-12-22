from sqlalchemy.orm import Session
from backend.models.dhcp import DhcpConfig

class DhcpRepository:

    @staticmethod
    def create(db: Session, data):
        dhcp = DhcpConfig(**data)
        db.add(dhcp)
        db.commit()
        db.refresh(dhcp)
        return dhcp

    @staticmethod
    def get_all(db: Session):
        return db.query(DhcpConfig).all()

    @staticmethod
    def get_by_router(db: Session, router_id: int):
        return db.query(DhcpConfig).filter(DhcpConfig.router_id == router_id).all()

    @staticmethod
    def delete(db: Session, dhcp_id: int):
        dhcp = db.query(DhcpConfig).filter(DhcpConfig.id == dhcp_id).first()
        if not dhcp:
            return False
        db.delete(dhcp)
        db.commit()
        return True
