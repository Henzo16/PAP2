import socket
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from models.router import Roteador
from sqlalchemy.orm import Session

# Lista de IPs mais prováveis
POSSIBLE_IPS = [
    "192.168.1.1",
    "192.168.0.1",
    "10.0.0.1",
    "172.16.0.1"
]

# -----------------------------
# TESTE DE PORTA TCP (ALTA PERFORMANCE)
# -----------------------------
def is_port_open(ip: str, port: int, timeout: float = 0.5) -> bool:
    """Retorna True se a porta TCP estiver aberta (melhor que ping no Mac)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        return True
    except:
        return False


# -----------------------------
# DETECTOR DE ROTEADOR CISCO
# -----------------------------
def detect_router(db: Session, username: str, password: str):
    """Detecta roteador Cisco *sem travar*, com timeout REAL."""

    for ip in POSSIBLE_IPS:
        print(f"🔎 Testando {ip}...")

        # 1️⃣ Testa porta 22 (SSH) — muito mais preciso que ping
        if not is_port_open(ip, 22):
            print(f"❌ Porta 22 fechada em {ip}. Ignorando...")
            continue

        print(f"📡 Porta 22 aberta em {ip}! Testando SSH...")

        try:
            conn = ConnectHandler(
                device_type="cisco_ios",
                host=ip,
                username=username,
                password=password,
                timeout=3,        # ⏱ Timeout real da sessão
                conn_timeout=3
            )

            # 2️⃣ Identificar o modelo do roteador
            model_output = conn.send_command(
                "show version | include Cisco",
                expect_string=r"#"
            )

            model = model_output.strip() if model_output else "Cisco Router"

            conn.disconnect()

            # 3️⃣ Verifica se já existe no BD
            router = db.query(Roteador).filter(Roteador.ip_address == ip).first()

            if not router:
                router = Roteador(
                    hostname=f"Router-{ip}",
                    ip_address=ip,
                    username=username,
                    password=password,
                    model=model,
                    status="online"
                )
                db.add(router)
            else:
                router.status = "online"

            db.commit()
            db.refresh(router)

            return {
                "detected": True,
                "ip": ip,
                "model": model,
                "router_id": router.id
            }

        except NetmikoTimeoutException:
            print(f"⏳ Timeout SSH em {ip}.")
        except NetmikoAuthenticationException:
            print(f"🔑 Falha de autenticação SSH em {ip}.")
        except Exception as e:
            print(f"⚠️ Erro SSH inesperado em {ip}: {e}")

    # Nenhum roteador encontrado
    return {"detected": False}
