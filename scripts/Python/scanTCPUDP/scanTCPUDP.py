#!/usr/bin/python3
# Programa para realizar um scan de portas TCP e UDP em IP do tipo IPv4,
# salvando os resultados em um arquivo de log externo caso haja portas abertas.
# O arquivo ports.py contém as listas com o Top 100 de portas TCP e UDP mais comuns, baseado no Nmap.

import socket
import re
import sys

### VERIFICA SE O ARQUIVO ports.py ESTÁ PRESENTE E IMPORTA AS PORTAS TCP E UDP
try:
    from ports import PORTAS_TCP_NMAP, PORTAS_UDP_NMAP
except ImportError:
    try:
        from ports import PORTAS_TCP as PORTAS_TCP_NMAP, PORTAS_UDP as PORTAS_UDP_NMAP
    except ImportError:
        print("\n[!] ERRO CRÍTICO: O arquivo 'ports.py' não foi encontrado!")
        print("[!] Certifique-se de que o arquivo 'ports.py' esteja localizado na mesma pasta do programa.")
        sys.exit(1)

### FUNÇÃO PARA VALIDAR O ENDEREÇO IP USANDO EXPRESSÃO REGULAR
def validar_ip(ip: str) -> bool:
    """Valida se a string informada é um endereço IPv4 no formato X.X.X.X (0 a 255 por octeto)."""
    padrao_ip = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(padrao_ip, ip.strip()))

### FUNÇÃO PARA OBTER O NOME DO SERVIÇO PROVÁVEL ASSOCIADO À PORTA
def obter_nome_servico(porta: int, mapa_servicos: dict | list) -> str:
    """Busca o nome do serviço provável no dicionário/lista ou via socket nativo."""
    if isinstance(mapa_servicos, dict):
        return mapa_servicos.get(porta, "desconhecido")
    try:
        return socket.getservbyport(porta)
    except Exception:
        return "desconhecido"


### FUNÇÃO PARA GUARDAR O LOG DE PORTAS ABERTAS EM UM ARQUIVO
def salvar_log(ip, portas_abertas, tipo):
    if not portas_abertas:
        print("\n[!] Nenhuma porta aberta foi encontrada para salvar no log.")
        return

    proto_nome = "TCP" if tipo == 1 else "UDP"
    ### Salva o log das portas abertas em um arquivo externo.
    with open('log_portas_abertas.txt', 'a') as arquivo:
        arquivo.write(f'IP: {ip}\n')
        arquivo.write(f'Tipo de scan: {proto_nome}\n')
        arquivo.write('Portas abertas e serviços prováveis:\n')
        for porta, servico in portas_abertas:
            arquivo.write(f' - Porta {porta}/{proto_nome}: {servico}\n')
        arquivo.write('\n')
    print("\n[+] Log das portas abertas salvo em 'log_portas_abertas.txt'!")


### FUNÇÃO PRINCIPAL PARA SCAN DE TOP 100 PORTAS TCP OU UDP
def scan_portas(ip, tipo):
    portas_abertas = []

    if tipo == 1:
        mapa_portas = PORTAS_TCP_NMAP
        print(f'\nIniciando scan TCP em {ip} ({len(mapa_portas)} portas)...')
        
        # Suporta tanto dicionário {porta: servico} quanto lista simples [portas]
        portas = mapa_portas.keys() if isinstance(mapa_portas, dict) else mapa_portas

        for porta in portas:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            resultado = sock.connect_ex((ip, porta))
            
            if resultado == 0:
                servico = obter_nome_servico(porta, mapa_portas)
                print(f'[+] Porta TCP {porta:<5} ABERTA  ---> Serviço Provável: {servico}')
                portas_abertas.append((porta, servico))
                
            sock.close()

    elif tipo == 2:
        mapa_portas = PORTAS_UDP_NMAP
        print(f'\nIniciando scan UDP em {ip} ({len(mapa_portas)} portas)...')
        
        portas = mapa_portas.keys() if isinstance(mapa_portas, dict) else mapa_portas

        for porta in portas:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2.0)
            try:
                sock.sendto(b'\x00', (ip, porta))
                data, addr = sock.recvfrom(1024)
                servico = obter_nome_servico(porta, mapa_portas)
                print(f'[+] Porta UDP {porta:<5} ABERTA  ---> Serviço Provável: {servico}')
                portas_abertas.append((porta, servico))
            except (socket.timeout, Exception):
                pass
            finally:
                sock.close()

    else:
        print('Tipo de scan inválido. Escolha 1 para TCP ou 2 para UDP.')
        return

    salvar_log(ip, portas_abertas, tipo)


### ENTRADA DE DADOS E EXECUÇÃO DO SCRIPT
if __name__ == '__main__': # Essa função garante que o código abaixo só será executado se o script for rodado diretamente, e não importado como módulo.
    ip_alvo = input('Digite o IP do host (ex: 192.168.1.1): ').strip()

    if not validar_ip(ip_alvo):
        print("\n[!] ERRO: Endereço IP inválido!")
        print("Modo de uso correto:")
        print(" - Digite um endereço IPv4 válido no formato X.X.X.X.")
        print(" - Exemplo válido: 192.168.0.1 ou 10.0.0.15\n")
        sys.exit(1)

    try:
        tipo_scan = int(input('Digite o tipo de scan (1) TCP (2) UDP: '))
        scan_portas(ip_alvo, tipo_scan)
    except ValueError:
        print("\n[!] Erro: Por favor, digite apenas números (1 para TCP ou 2 para UDP).")