# services/cisco_executor.py

from netmiko import ConnectHandler
from fastapi import HTTPException
from models.router import Roteador
from sqlalchemy.orm import Session

from services.logger import save_log

def execute_commands(db, router_id: int, commands: list[str], user_id: int | None = 1):
    """
    Executa comandos no Cisco e registra logs automaticamente.
    user_id = ID do usuário autenticado (por enquanto default = 1)
    """
    router = db.query(Roteador).filter(Roteador.id == router_id).first()
    if not router:
        raise Exception("Roteador não encontrado")

    device = {
        "device_type": "cisco_ios",
        "host": router.ip_address,
        "username": router.username,
        "password": router.password,
        "secret": router.password
    }

    connection = ConnectHandler(**device)
    connection.enable()

    output = connection.send_config_set(commands)
    connection.save_config()
    connection.disconnect()

    # 🔥 Salvar log no banco
    save_log(db, user_id, router_id, action="Execução de comandos", commands=commands, output=output)

    return output
