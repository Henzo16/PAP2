from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from database import Base
import enum

class NatType(enum.Enum):
    estatico = "estatico"
    dinamico = "dinamico"
    overload = "overload"

class NatConfig(Base):
    __tablename__ = "nat_configs"

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("roteadores.id"))
    type = Column(Enum(NatType), nullable=False)
    internal_ip = Column(String(15))
    external_ip = Column(String(15))
    access_list = Column(String(50))
    pool_name = Column(String(50))
    outside_interface = Column(String(50))
