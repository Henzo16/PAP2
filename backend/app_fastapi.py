from fastapi import FastAPI, HTTPException
from schemas.router import RoteadorCreate, RoteadorResponse
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException
import logging
from fastapi import Depends
from services.detector import detect_router
from middleware.auth_middleware import AuthMiddleware
from routes.router_routes import router as router_routes
from starlette.responses import JSONResponse
from auth.deps import get_current_user
from database import get_db
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.router import Roteador
from crud.dhcp import create_dhcp, get_dhcp_by_router, update_dhcp, delete_dhcp
from schemas.dhcp import DhcpCreate, DhcpUpdate, DhcpOut
from schemas.nat import NatCreate, NatUpdate, NatOut
from crud.nat import create_nat, get_nat_by_router, update_nat, delete_nat
from crud.vlan import (
    create_vlan,
    get_vlans_by_router as get_vlan_by_router,
    update_vlan,
    delete_vlan
)

from schemas.vlan import VlanCreate, VlanUpdate, VlanOut
from crud.acl import (
    create_acl,
    get_acls_by_router as get_acl_by_router,
    update_acl,
    delete_acl
)

from schemas.acl import AclCreate, AclUpdate, AclOut
from crud.static_route import create_static_route, get_static_routes_by_router, update_static_route, delete_static_route
from schemas.static_route import StaticRouteCreate, StaticRouteUpdate, StaticRouteOut
from crud.ospf import create_ospf, get_ospf_by_router, update_ospf, delete_ospf
from schemas.ospf import OspfCreate, OspfUpdate, OspfOut
from fastapi.responses import FileResponse
from models.log import Log
from services.pdf_generator import generate_log_pdf
from routes import auth

from routes.router_routes import router as routers_routes
from routes.dhcp_routes import router as dhcp_routes
from routes.nat_routes import router as nat_routes
from routes.vlan_routes import router as vlan_routes
from routes.acl_routes import router as acl_routes
from routes.static_route_routes import router as static_routes
from routes.ospf_routes import router as ospf_routes
from auth.deps import get_current_user

# Importação dos serviços e modelos melhores
from services.dhcp import DhcpConfig, configure_dhcp
from services.nat import StaticNatConfig, DynamicNatConfig, NatOverloadConfig, configure_static_nat, configure_dynamic_nat, configure_nat_overload
from services.routing import StaticRouteConfig, OspfConfig, InterVlanRoutingConfig, configure_static_route, configure_ospf, configure_inter_vlan_routing
from services.vlan import VlanConfig, configure_vlan
from services.acl import (
    StandardAclRule,
    ExtendedAclRule,
    NamedAclRule,
    configure_standard_acl,
    configure_extended_acl,
    configure_named_acl,
)

from services.router import check_current_config, clear_router_config
from fastapi import Depends
from dependencies import get_db
from fastapi.middleware.cors import CORSMiddleware
from routes import auth

PUBLIC_PATHS = [
   "/api/auth/login",
    "/api/auth/register",
    "/api/auth/me",     # <-- ADICIONE ISTO!!!
    "/openapi.json",
    "/docs",
    "/redoc",
    "/api/router/auto-detect",
]


# ---------------------------------
# Inicializar Aplicação FastAPI
# ---------------------------------
app = FastAPI(
    title="Cisco Automation API",
    description="API profissional para configuração automatizada de roteadores Cisco",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← depois podemos restringir
    allow_credentials=True,
    allow_methods=["*"],  # ← ESSENCIAL! Permite OPTIONS
    allow_headers=["*"],  # ← ESSENCIAL! Permite Authorization
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Rotas públicas -> ignorar token
        if any(path.startswith(pub) for pub in PUBLIC_PATHS):
            return await call_next(request)

        # Extrair Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = None

        # Guardar token no request para a rota consumir
        request.state.token = token

        return await call_next(request)

# ---------------------------------
# Handlers de erro
# ---------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_type": "ValidationError",
            "detail": exc.errors()
        }
    )

@app.exception_handler(NetmikoTimeoutException)
async def timeout_handler(request, exc):
    return JSONResponse(
        status_code=504,
        content={
            "success": False,
            "error_type": "Timeout",
            "detail": "Tempo esgotado ao tentar conectar ao roteador."
        }
    )

@app.exception_handler(NetmikoAuthenticationException)
async def auth_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error_type": "AuthenticationError",
            "detail": "Falha de autenticação ao acessar o roteador."
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_type": "InternalError",
            "detail": str(exc)
        }
    )

# ---------------------------------------------------------
# CRUD DHCP
# ---------------------------------------------------------

# ---------------------- DHCP --------------------------

@app.post("/api/dhcp", response_model=DhcpOut)
def criar_dhcp(config: DhcpCreate, db: Session = Depends(get_db)):
    return create_dhcp(db, config)


@app.get("/api/dhcp/{router_id}", response_model=list[DhcpOut])
def listar_dhcp(router_id: int, db: Session = Depends(get_db)):
    return get_dhcp_by_router(db, router_id)


@app.put("/api/dhcp/{dhcp_id}", response_model=DhcpOut)
def atualizar_dhcp(dhcp_id: int, config: DhcpUpdate, db: Session = Depends(get_db)):
    result = update_dhcp(db, dhcp_id, config)
    if not result:
        raise HTTPException(status_code=404, detail="DHCP não encontrado")
    return result


@app.delete("/api/dhcp/{dhcp_id}")
def remover_dhcp(dhcp_id: int, db: Session = Depends(get_db)):
    ok = delete_dhcp(db, dhcp_id)
    if not ok:
        raise HTTPException(status_code=404, detail="DHCP não encontrado")
    return {"success": True, "message": "Configuração DHCP removida"}


# ---------------------------------------------------------
# CRUD NAT
# ---------------------------------------------------------

# ---------------------- NAT --------------------------

@app.post("/api/nat", response_model=NatOut)
def criar_nat(config: NatCreate, db: Session = Depends(get_db)):
    return create_nat(db, config)


@app.get("/api/nat/{router_id}", response_model=list[NatOut])
def listar_nat(router_id: int, db: Session = Depends(get_db)):
    return get_nat_by_router(db, router_id)


@app.put("/api/nat/{nat_id}", response_model=NatOut)
def atualizar_nat(nat_id: int, config: NatUpdate, db: Session = Depends(get_db)):
    result = update_nat(db, nat_id, config)
    if not result:
        raise HTTPException(status_code=404, detail="NAT não encontrado")
    return result


@app.delete("/api/nat/{nat_id}")
def remover_nat(nat_id: int, db: Session = Depends(get_db)):
    ok = delete_nat(db, nat_id)
    if not ok:
        raise HTTPException(status_code=404, detail="NAT não encontrado")
    return {"success": True, "message": "NAT removido com sucesso"}


@app.post("/api/vlan", response_model=VlanOut)
def criar_vlan(data: VlanCreate, db: Session = Depends(get_db)):
    return create_vlan(db, data)


@app.get("/api/vlan/{router_id}", response_model=list[VlanOut])
def listar_vlans(router_id: int, db: Session = Depends(get_db)):
    return get_vlan_by_router(db, router_id)


@app.put("/api/vlan/{vlan_id}", response_model=VlanOut)
def atualizar_vlan(vlan_id: int, data: VlanUpdate, db: Session = Depends(get_db)):
    vlan = update_vlan(db, vlan_id, data)
    if not vlan:
        raise HTTPException(status_code=404, detail="VLAN não encontrada")
    return vlan




@app.post("/api/acl", response_model=AclOut)
def criar_acl(data: AclCreate, db: Session = Depends(get_db)):
    return create_acl(db, data)


# ------------------ ACL -----------------------

@app.post("/api/acl", response_model=AclOut)
def criar_acl(config: AclCreate, db: Session = Depends(get_db)):
    return create_acl(db, config)


@app.get("/api/acl/{router_id}", response_model=list[AclOut])
def listar_acl(router_id: int, db: Session = Depends(get_db)):
    return get_acls_by_router(db, router_id)


@app.put("/api/acl/{acl_id}", response_model=AclOut)
def atualizar_acl(acl_id: int, config: AclUpdate, db: Session = Depends(get_db)):
    result = update_acl(db, acl_id, config)
    if not result:
        raise HTTPException(status_code=404, detail="ACL não encontrada")
    return result


@app.delete("/api/acl/{acl_id}")
def remover_acl(acl_id: int, db: Session = Depends(get_db)):
    ok = delete_acl(db, acl_id)
    if not ok:
        raise HTTPException(status_code=404, detail="ACL não encontrada")
    return {"success": True, "message": "ACL removida"}

# ------------------ STATIC ROUTES -----------------------

@app.post("/api/static-route", response_model=StaticRouteOut)
def criar_static_route(config: StaticRouteCreate, db: Session = Depends(get_db)):
    return create_static_route(db, config)


@app.get("/api/static-route/{router_id}", response_model=list[StaticRouteOut])
def listar_static_routes(router_id: int, db: Session = Depends(get_db)):
    return get_static_routes_by_router(db, router_id)


@app.put("/api/static-route/{route_id}", response_model=StaticRouteOut)
def atualizar_static_route(route_id: int, config: StaticRouteUpdate, db: Session = Depends(get_db)):
    result = update_static_route(db, route_id, config)
    if not result:
        raise HTTPException(status_code=404, detail="Rota estática não encontrada")
    return result


@app.delete("/api/static-route/{route_id}")
def remover_static_route(route_id: int, db: Session = Depends(get_db)):
    ok = delete_static_route(db, route_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Rota estática não encontrada")
    return {"success": True, "message": "Rota estática removida"}


# ----------------- OSPF ROUTES ---------------------

@app.post("/api/ospf", response_model=OspfOut)
def criar_ospf(config: OspfCreate, db: Session = Depends(get_db)):
    return create_ospf(db, config)


@app.get("/api/ospf/{router_id}", response_model=list[OspfOut])
def listar_ospf(router_id: int, db: Session = Depends(get_db)):
    return get_ospf_by_router(db, router_id)


@app.put("/api/ospf/{ospf_id}", response_model=OspfOut)
def atualizar_ospf(ospf_id: int, config: OspfUpdate, db: Session = Depends(get_db)):
    result = update_ospf(db, ospf_id, config)
    if not result:
        raise HTTPException(status_code=404, detail="Entrada OSPF não encontrada")
    return result


@app.delete("/api/ospf/{ospf_id}")
def remover_ospf(ospf_id: int, db: Session = Depends(get_db)):
    ok = delete_ospf(db, ospf_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Entrada OSPF não encontrada")
    return {"success": True, "message": "Configuração OSPF removida"}



# ------------------ VLAN -----------------------

@app.post("/api/vlan", response_model=VlanOut)
def criar_vlan(config: VlanCreate, db: Session = Depends(get_db)):
    return create_vlan(db, config)


@app.get("/api/vlan/{router_id}", response_model=list[VlanOut])
def listar_vlan(router_id: int, db: Session = Depends(get_db)):
    return get_vlans_by_router(db, router_id)


@app.put("/api/vlan/{vlan_id}", response_model=VlanOut)
def atualizar_vlan(vlan_id: int, config: VlanUpdate, db: Session = Depends(get_db)):
    res = update_vlan(db, vlan_id, config)
    if not res:
        raise HTTPException(status_code=404, detail="VLAN não encontrada")
    return res


@app.delete("/api/vlan/{vlan_id}")
def remover_vlan(vlan_id: int, db: Session = Depends(get_db)):
    ok = delete_vlan(db, vlan_id)
    if not ok:
        raise HTTPException(status_code=404, detail="VLAN não encontrada")
    return {"success": True, "message": "VLAN removida"}




# ---------------------------------
# Logging
# ---------------------------------
logging.basicConfig(level=logging.INFO, format="%(message)s")


# ---------------------------------
# Rotas da API
# ---------------------------------

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/", tags=["Status"])
async def home():
    logging.info("API inicializada com sucesso 🚀")
    return {"success": True, "message": "Cisco Automation API is running!"}

@app.get("/api/test", tags=["Status"])
async def test():
    return {"success": True, "message": "Server alive and operational"}


# DHCP
@app.post("/api/dhcp", tags=["DHCP"])
async def dhcp(config: DhcpConfig):
    result = configure_dhcp(config)
    return {"success": True, "output": result}


# NAT
@app.post("/api/nat/static", tags=["NAT"])
async def nat_static(config: StaticNatConfig):
    return {"success": True, "output": configure_static_nat(config)}

@app.post("/api/nat/dynamic", tags=["NAT"])
async def nat_dynamic(config: DynamicNatConfig):
    return {"success": True, "output": configure_dynamic_nat(config)}

@app.post("/api/nat/overload", tags=["NAT"])
async def nat_overload(config: NatOverloadConfig):
    return {"success": True, "output": configure_nat_overload(config)}


# Routing
@app.post("/api/route/static", tags=["Routing"])
async def route_static(config: StaticRouteConfig):
    return {"success": True, "output": configure_static_route(config)}

@app.post("/api/route/ospf", tags=["Routing"])
async def route_ospf(config: OspfConfig):
    return {"success": True, "output": configure_ospf(config)}

@app.post("/api/route/intervlan", tags=["Routing"])
async def intervlan(config: InterVlanRoutingConfig):
    return {"success": True, "output": configure_inter_vlan_routing(config)}


# VLAN
@app.post("/api/vlan", tags=["VLAN"])
async def vlan(config: VlanConfig):
    return {"success": True, "output": configure_vlan(config)}


# ACL
@app.post("/api/acl/standard")
async def acl_standard(config: StandardAclRule):
    result = configure_standard_acl(config)
    return {"status": "success", "output": result}


@app.post("/api/acl/extended")
async def acl_extended(config: ExtendedAclRule):
    result = configure_extended_acl(config)
    return {"status": "success", "output": result}


@app.post("/api/acl/named")
async def acl_named(config: NamedAclRule):
    result = configure_named_acl(config)
    return {"status": "success", "output": result}


# Router commands
@app.get("/api/router/config", tags=["Router"])
async def router_config():
    return {"success": True, "output": check_current_config()}

@app.post("/api/router/clear", tags=["Router"])
async def clear_config():
    return {"success": True, "output": clear_router_config()}

@app.get("/teste")
def test_db(db = Depends(get_db)):
    result = db.execute("SELECT NOW()").fetchone()
    return {"conexao": str(result)}

@app.get("/db/teste")
def testar_conexao(db = Depends(get_db)):
    r = db.execute("SELECT 1").fetchone()
    return {"status": "ok", "resultado": r}


@app.get("/api/routers")
def listar_roteadores(db: Session = Depends(get_db)):
    roteadores = db.query(Roteador).all()
    return roteadores


@app.post("/api/routers")
def criar_roteador(roteador: RoteadorCreate, db: Session = Depends(get_db)):
    novo = Roteador(
        hostname=roteador.hostname,
        ip_address=roteador.ip_address,
        username=roteador.username,
        password=roteador.password,
        model=roteador.model,
        status="offline"
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

app.include_router(routers_routes)
app.include_router(dhcp_routes)
app.include_router(nat_routes)
app.include_router(vlan_routes)
app.include_router(acl_routes)
app.include_router(static_routes)
app.include_router(ospf_routes)
app.include_router(router_routes)


@app.get("/api/report/{router_id}")
def gerar_relatorio(router_id: int, db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.router_id == router_id).all()
    filename = generate_pdf(logs)
    return FileResponse(filename, media_type="application/pdf")

from services.cisco_executor import execute_commands

@app.post("/api/test/execute")
def testar_execucao(router_id: int, db: Session = Depends(get_db)):
    commands = ["interface loopback99", "description TESTE_API", "ip address 10.99.99.1 255.255.255.0"]
    return execute_commands(db, router_id, commands)

@app.get("/api/logs/{log_id}/pdf")
def baixar_relatorio(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Log).filter(Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")

    user = log.user
    router = log.router

    pdf_path = generate_log_pdf(log, user, router)

    return FileResponse(path=pdf_path, filename=f"relatorio_log_{log_id}.pdf")


app.include_router(auth.router, prefix="/api/auth")

@app.get("/api/router/auto-detect")
async def auto_detect(ip: str, username: str, password: str, db: Session = Depends(get_db)):
    return detect_router(ip, username, password)




app.include_router(auth.router)




