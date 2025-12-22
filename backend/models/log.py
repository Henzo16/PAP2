from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    router_id = Column(Integer, ForeignKey("roteadores.id"), nullable=False)

    action = Column(String, nullable=False)
    commands = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")
    router = relationship("Roteador", back_populates="logs")
