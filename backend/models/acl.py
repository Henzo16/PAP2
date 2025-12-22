from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Acl(Base):
    __tablename__ = "acls"

    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("roteadores.id", ondelete="CASCADE"))

    acl_type = Column(String, nullable=False)  # standard | extended | named
    acl_number = Column(Integer, nullable=True)
    action = Column(String, nullable=False)  # permit | deny
    ip_address = Column(String, nullable=True)
    wildcard = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    dest_ip = Column(String, nullable=True)
    dest_wildcard = Column(String, nullable=True)
    acl_name = Column(String, nullable=True)

    router = relationship("Roteador", back_populates="acls")
