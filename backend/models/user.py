from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)          # <-- ADICIONADO
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)         # <-- ADICIONADO
    tipo = Column(String, default="normal")        # <-- ADICIONADO (opcional)

    logs = relationship("Log", back_populates="user")
