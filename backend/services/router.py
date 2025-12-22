# services/router.py

import logging
from fastapi import HTTPException
from netmiko import ConnectHandler
from backend.config import ROUTER
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException



# -----------------------------
# CONFIGURAÇÃO DE LOGS
# -----------------------------
logger = logging.getLogger("router-service")


# -----------------------------
# FUNÇÃO BASE PARA CONEXÃO
# -----------------------------
def _connect():
    """Conecta ao roteador ou entra em modo simulado."""
    
    # Modo simulado (quando não existe roteador fisico/virtual)
    if ROUTER.get("host") == "simulate":
        logger.warning("Modo SIMULAÇÃO ativado. Nenhum comando real será enviado ao roteador.")
        return None  # usado para simulação

    try:
        conn = ConnectHandler(**ROUTER)
        conn.enable()
        return conn
    except NetmikoTimeoutException:
        raise HTTPException(status_code=504, detail="Timeout ao conectar ao roteador.")
    except NetmikoAuthenticationException:
        raise HTTPException(status_code=401, detail="Falha de autenticação no roteador.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao conectar: {str(e)}")



# -----------------------------
# ENVIO DE COMANDOS
# -----------------------------
def send_to_router(commands):
    """
    Envia comandos de configuração ao roteador.
    Suporta modo real e simulado.
    """

    logger.info(f"Enviando comandos para o roteador: {commands}")

    # SIMULADO
    if ROUTER.get("host") == "simulate":
        return {
            "mode": "simulation",
            "commands_sent": commands,
            "output": "Simulação: comandos não foram enviados ao roteador real."
        }

    # REAL
    conn = _connect()

    try:
        output = conn.send_config_set(commands)
        conn.save_config()
        conn.disconnect()
        return {
            "mode": "real",
            "commands_sent": commands,
            "output": output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar comandos: {str(e)}")



# -----------------------------
# SHOW RUNNING-CONFIG
# -----------------------------
def check_current_config():
    logger.info("Consultando running-config do roteador...")

    if ROUTER.get("host") == "simulate":
        return "Simulação: running-config fictício...."

    conn = _connect()

    try:
        conn.send_command("terminal length 0")
        output = conn.send_command("show running-config")
        conn.disconnect()
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar configuração: {str(e)}")



# -----------------------------
# LIMPAR CONFIG E RELOAD
# -----------------------------
def clear_router_config():
    """
    Limpa TODA a configuração do roteador e reinicia.
    """

    logger.warning("ATENÇÃO: Enviando comando de ERASE + RELOAD ao roteador!")

    if ROUTER.get("host") == "simulate":
        return "Simulação: router seria apagado e reiniciado."

    conn = _connect()

    try:
        conn.send_command("write erase")
        conn.send_command("reload", expect_string=r'\[confirm\]')
        conn.send_command("\n")  # ENTER confirma reload
        conn.disconnect()

        return "Configurações apagadas. Roteador reiniciando..."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao reiniciar roteador: {str(e)}")
