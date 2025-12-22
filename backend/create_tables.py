from backend.database import Base, engine

# IMPORTAR TODOS OS MODELS
from backend.models.router import Roteador
from backend.models.dhcp import DhcpConfig
from backend.models.nat import NatConfig
from backend.models.vlan import Vlan
from backend.models.acl import Acl
from backend.models.static_route import StaticRoute
from backend.models.ospf import OspfRoute
from backend.models.user import User
from backend.models.log import Log

print("📡 Criando tabelas no PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
