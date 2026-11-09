#!/usr/bin/python3
# Programa para analisar log e trazer um resultado com base na entrada do usuário
# Formatos aceitos: raw, arquivo de texto, CSV, json, xml. 
# Modo de uso: ./pyLOG.py <nome do arquivo> 'palavra-chave'

import re
import os
import sys
import json
from datetime import datetime

### FUNÇÃO PARA VALIDAR ARGUMENTOS
def validar_argumentos():
    if len(sys.argv) != 3:
        print("Uso: ./pyLOG.py <nome_do_arquivo> <palavra-chave>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

### FUNÇÃO PARA FILTRAR O CONTEÚDO DO ARQUIVO COM BASE NA PALAVRA-CHAVE
def filtrar_log(arquivo, palavra_chave):
    padrao = re.compile(re.escape(palavra_chave), re.IGNORECASE)
    resultados = []
    
    try:
        with open(arquivo, 'r', encoding='utf-8', errors='ignore') as file:
            for numero_linha, linha in enumerate(file, start=1):
                if padrao.search(linha):
                    resultados.append({
                        "linha": numero_linha,
                        "match": linha.strip()
                    })
    except FileNotFoundError:
        print(f"[-] Erro: O arquivo '{arquivo}' não foi encontrado.")
        sys.exit(1)
    except PermissionError:
        print(f"[-] Erro: Sem permissão para ler o arquivo '{arquivo}'.")
        sys.exit(1)
        
    return resultados

### FUNÇÃO PARA TRANSFORMAR A SAÍDA EM UM ARQUIVO JSON ESTRUTURADO
def gerar_relatorio_json(resultados, palavra_chave, nome_arquivo):
    relatorio = {
        "metadados": {
            "arquivo_alvo": nome_arquivo,
            "termo_buscado": palavra_chave,
            "total_matches": len(resultados),
            "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "resultados": resultados
    }
    
    nome_saida = f"report_{palavra_chave}_{os.path.basename(nome_arquivo)}.json"
    
    with open(nome_saida, 'w', encoding='utf-8') as json_file:
        json.dump(relatorio, json_file, indent=4, ensure_ascii=False)
        
    return nome_saida

### FLUXO PRINCIPAL DO PROGRAMA
def main():
    arquivo, palavra_chave = validar_argumentos()
    
    print(f"[*] Iniciando parse do arquivo '{arquivo}' buscando por '{palavra_chave}'...")
    matches = filtrar_log(arquivo, palavra_chave)
    
    if not matches:
        print("[-] Nenhuma ocorrência encontrada para a palavra-chave.")
        sys.exit(0)
        
    print(f"[+] Sucesso! Foram encontradas {len(matches)} ocorrências:\n")
    
    # Exibe o resultado na tela
    for match in matches:
        print(f"-> Linha {match['linha']}: {match['match']}")
        
    # Pergunta ao usuário se deseja salvar o resultado
    print("\n" + "-"*50)
    salvar = input("[?] Deseja gerar um relatório estruturado em .json com esses resultados? (s/n): ").strip().lower()
    
    if salvar in ['s', 'sim', 'y', 'yes']:
        arquivo_gerado = gerar_relatorio_json(matches, palavra_chave, arquivo)
        print(f"[+] Relatório salvo com sucesso em: {arquivo_gerado}")
    else:
        print("[*] Busca finalizada. Nenhum arquivo foi gerado no disco.")

# Garante o funcionamento do programa dentro do CLI ou módulo importado.
if __name__ == "__main__":
    main()
