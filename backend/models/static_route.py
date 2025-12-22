from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class StaticRoute(Base):
    __tablename__ = "static_routes"

    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("roteadores.id", ondelete="CASCADE"))

    network = Column(String, nullable=False)
    mask = Column(String, nullable=False)
    next_hop = Column(String, nullable=False)

    router = relationship("Roteador", back_populates="static_routes")
