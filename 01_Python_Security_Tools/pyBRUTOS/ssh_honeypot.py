#!/usr/bin/env python3
# By Claude.
"""
SSH Honeypot simples - Projeto de portfolio em ciberseguranca.

Simula um servidor SSH que aceita conexoes, registra as credenciais
utilizadas pelo cliente (usuario/senha/IP/porta/horario) e NUNCA concede
acesso real de shell. E uma isca para fins de estudo e monitoramento,
nao um servidor SSH funcional.

Requisitos:
    pip install paramiko

Uso:
    python3 ssh_honeypot.py --host 0.0.0.0 --port 2222

Nota: a porta 22 exige privilegios de root/admin no SO. Para testes,
use uma porta alta (ex: 2222) e, se quiser expor como se fosse a 22,
faca o redirecionamento na camada de firewall/roteador.
"""

import argparse
import logging
import socket
import threading
from datetime import datetime

import paramiko

# Credenciais "isca" exibidas no README/baseline do projeto.
# O honeypot loga TODAS as tentativas, nao apenas essa combinacao.
BAIT_USERNAME = "admin"
BAIT_PASSWORD = "admin123"

LOG_FILE = "ssh_honeypot.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("ssh_honeypot")

# Chave de host do servidor falso (gerada uma vez e reutilizada)
HOST_KEY = paramiko.RSAKey.generate(2048)


class HoneypotServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        timestamp = datetime.now().isoformat(timespec="seconds")
        is_bait = username == BAIT_USERNAME and password == BAIT_PASSWORD

        logger.info(
            "TENTATIVA DE LOGIN | ip=%s | usuario=%r | senha=%r | isca_correspondida=%s",
            self.client_ip, username, password, is_bait,
        )

        # Sempre rejeita - o honeypot nunca concede acesso real,
        # mesmo quando a credencial isca e usada.
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        logger.info(
            "TENTATIVA COM CHAVE PUBLICA | ip=%s | usuario=%r | fingerprint=%s",
            self.client_ip, username, key.get_fingerprint().hex(),
        )
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password,publickey"

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED


def handle_connection(client_socket, client_addr):
    client_ip = client_addr[0]
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(HOST_KEY)
        # Banner falso para parecer um servidor SSH comum
        transport.local_version = "SSH-2.0-OpenSSH_8.9"

        server = HoneypotServer(client_ip)
        transport.start_server(server=server)

        # Mantem a conexao aberta por pouco tempo so para registrar
        # possiveis tentativas adicionais, depois encerra.
        channel = transport.accept(5)
        if channel is not None:
            channel.close()

    except Exception as exc:
        logger.debug("Conexao de %s encerrada: %s", client_ip, exc)
    finally:
        try:
            transport.close()
        except Exception:
            pass


def run_honeypot(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)

    logger.info("Honeypot SSH rodando em %s:%d (credencial isca: %s/%s)",
                host, port, BAIT_USERNAME, BAIT_PASSWORD)
    logger.info("Logs sendo gravados em: %s", LOG_FILE)

    try:
        while True:
            client_socket, client_addr = sock.accept()
            thread = threading.Thread(
                target=handle_connection,
                args=(client_socket, client_addr),
                daemon=True,
            )
            thread.start()
    except KeyboardInterrupt:
        logger.info("Encerrando honeypot...")
    finally:
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Honeypot SSH simples para portfolio de ciberseguranca.")
    parser.add_argument("--host", default="0.0.0.0", help="Endereco de escuta (padrao: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=2222, help="Porta de escuta (padrao: 2222)")
    args = parser.parse_args()

    run_honeypot(args.host, args.port)