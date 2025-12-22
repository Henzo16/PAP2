from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class OspfRoute(Base):
    __tablename__ = "ospf_routes"

    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("roteadores.id", ondelete="CASCADE"))

    process_id = Column(Integer, nullable=False)
    network = Column(String, nullable=False)
    wildcard_mask = Column(String, nullable=False)
    area = Column(Integer, nullable=False)

    router = relationship("Roteador", back_populates="ospf_routes")
