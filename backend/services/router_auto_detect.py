import subprocess
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

POSSIBLE_IPS = [
    "192.168.1.1",
    "192.168.0.1",
    "10.0.0.1",
    "172.16.0.1"
]

def ping(ip: str) -> bool:
    """Ping rápido compatível com macOS."""
    try:
        result = subprocess.call(
            ["ping", "-c", "1", "-t", "1", ip],  # <-- MACOS FIX
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result == 0
    except:
        return False


def detect_router(db, username: str, password: str):

    for ip in POSSIBLE_IPS:
        print(f"🔎 Testando {ip}...")

        if not ping(ip):
            print(f"❌ {ip} não respondeu ao ping.")
            continue

        print(f"📡 {ip} respondeu! Testando SSH...")

        try:
            conn = ConnectHandler(
                device_type="cisco_ios",
                host=ip,
                username=username,
                password=password,
                timeout=1,         # <-- ultra rápido
                conn_timeout=1,
                banner_timeout=1,
                auth_timeout=1
            )

            model_output = conn.send_command("show version | include Cisco", expect_string=r"#")
            model = model_output.strip() if model_output else "Cisco Router"

            conn.disconnect()

            return {
                "success": True,
                "ip": ip,
                "model": model
            }

        except Exception as e:
            print(f"❌ SSH falhou em {ip}: {e}")

    # ⚠️ Se chegar aqui, nenhum roteador foi detectado
    return {"success": False, "message": "Nenhum roteador encontrado."}
