from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Vlan(Base):
    __tablename__ = "vlans"

    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("roteadores.id", ondelete="CASCADE"))

    vlan_id = Column(Integer, nullable=False)
    vlan_name = Column(String, nullable=False)

    router = relationship("Roteador", back_populates="vlans")
