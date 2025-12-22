from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Roteador(Base):
    __tablename__ = "roteadores"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    model = Column(String, nullable=True)
    status = Column(String, default="offline")
    last_configured = Column(DateTime, default=datetime.utcnow)

    # RELACIONAMENTOS
    dhcp_configs = relationship("DhcpConfig", back_populates="router", cascade="all, delete-orphan")
    vlans = relationship("Vlan", back_populates="router", cascade="all,delete")
    acls = relationship("Acl", back_populates="router", cascade="all,delete")
    static_routes = relationship("StaticRoute", back_populates="router", cascade="all,delete")
    ospf_routes = relationship("OspfRoute", back_populates="router", cascade="all,delete")
    logs = relationship("Log", back_populates="router")
   





