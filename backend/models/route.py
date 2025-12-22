from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base

class StaticRoute(Base):
    __tablename__ = "static_routes"

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("roteadores.id"))
    network = Column(String(15), nullable=False)
    mask = Column(String(15), nullable=False)
    next_hop = Column(String(15), nullable=False)
