from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DhcpConfig(Base):
    __tablename__ = "dhcp_configs"

    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("roteadores.id"))
    pool_name = Column(String)
    network = Column(String)
    mask = Column(String)
    gateway = Column(String)
    dns = Column(String)

    router = relationship("Roteador", back_populates="dhcp_configs")
