from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Lê a URL do banco a partir do .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não encontrado no arquivo .env")

# Conexão com PostgreSQL
engine = create_engine(DATABASE_URL)

# Sessão do BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para modelos ORM
Base = declarative_base()

# Dependência para FastAPI injeção de sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
