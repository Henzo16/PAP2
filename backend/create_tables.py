from database import Base, engine

# IMPORTAR TODOS OS MODELS
from models.router import Roteador
from models.dhcp import DhcpConfig
from models.nat import NatConfig
from models.vlan import Vlan
from models.acl import Acl
from models.static_route import StaticRoute
from models.ospf import OspfRoute
from models.user import User
from models.log import Log

print("📡 Criando tabelas no PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
