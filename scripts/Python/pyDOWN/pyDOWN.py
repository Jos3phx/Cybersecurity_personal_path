#!/usr/bin/python3
# Programa para baixar arquivos da internet ou de servidores locai
# PDF e TXT

import os
import re
import requests

# Regex para filtrar links válidos de arquivos .pdf ou .txt
URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http://, https://, ftp://, ftps://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domínio
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
    r'(?::\d+)?'  # Porta opcional
    r'(?:/?|[/?]\S+)\.(?:pdf|txt)(?:\?.*)?$',  # Aceita apenas extensões .pdf ou .txt (com ou sem parâmetros na URL)
    re.IGNORECASE,
)

### FUNÇÃO PARA VALIDAR A URL COM RE.
def validar_url(url):
    #Retorna True se a URL for válida e terminar em .pdf ou .txt.
    return URL_REGEX.match(url) is not None

### FUNÇÃO PARA PEGAR O NOME DO ARQUIVO PRESENTE NA URL
def extrair_nome_arquivo(url):
    #Extrai o nome do arquivo a partir da URL.
    nome_limpo = url.split('?')[0]  # Remove parâmetros de query string
    nome = nome_limpo.split('/')[-1]
    return nome if nome else 'arquivo_baixado'

### FUNÇÃO PARA VERIFICAR SE HÁ UM ARQUIVO PDF OU TXT PARA DOWNLOAD.
def baixar_arquivo(url):
    # 1. Validação da URL com Expressão Regular
    if not validar_url(url):
        print(
            '❌ Erro: URL inválida ou o link não aponta para um arquivo .pdf ou .txt.'
        )
        return

    print('🔍 URL válida! Conectando ao servidor...')

    # 2. Tenta baixar o arquivo e trata alguns erros comuns.
    try:
        # stream=True permite baixar arquivos maiores em blocos sem carregar tudo na memória
        resposta = requests.get(url, stream=True, timeout=15)
        resposta.raise_for_status()  # Levanta exceção para códigos HTTP 4xx ou 5xx

        nome_arquivo = extrair_nome_arquivo(url)

        # 3. Escrita do arquivo no disco em modo binário ('wb')
        with open(nome_arquivo, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=8192):
                if chunk:
                    arquivo.write(chunk)

        caminho_completo = os.path.abspath(nome_arquivo)
        print(f'✅ Arquivo baixado com sucesso!\n📁 Salvo em: {caminho_completo}')

    except requests.exceptions.HTTPError as err:
        print(f'❌ Erro HTTP: {err.response.status_code} - {err.response.reason}')
    except requests.exceptions.ConnectionError:
        print('❌ Erro de conexão: Não foi possível alcançar o servidor.')
    except requests.exceptions.Timeout:
        print('❌ Erro de tempo limite: O servidor demorou muito para responder.')
    except requests.exceptions.RequestException as err:
        print(f'❌ Erro ao realizar a requisição: {err}')
    except IOError as err:
        print(f'❌ Erro ao salvar o arquivo localmente: {err}')

### FUNÇÃO PARA EXECUTAR O PROGRAMA.
def main():
    url_input = input('Digite a URL para download do arquivo (.pdf ou .txt): ').strip()
    if url_input:
        baixar_arquivo(url_input)
    else:
        print('❌ Nenhuma URL foi informada.')

main()