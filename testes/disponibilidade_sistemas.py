import json
import os
import requests
import time
import urllib3
import psycopg2
from datetime import datetime

# Desativa alertas de verificação SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define o caminho absoluto do JSON
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "../json/dominios.json")

# Lendo o JSON de domínios
try:
    with open(json_path, "r", encoding="utf-8") as file:
        sistemas = json.load(file)
        if not sistemas:
            print("Nenhum domínio encontrado no JSON.")
            exit(1)
except Exception as e:
    print(f"Erro ao carregar o JSON: {e}")
    exit(1)

# Define cabeçalhos HTTP para simular um navegador real, evitando bloqueios de sites
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",  # Do Not Track
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

# Define o timeout máximo para cada requisição
TIMEOUT = 15  

# Conectar ao banco de dados PostgreSQL
conexao = psycopg2.connect(
    dbname="monitoramento_aplicacoes",
    user="user",
    password="123456789",
    host="localhost",
    port="5432"
)
conexao_banco = conexao.cursor()
print("Conexão com o banco de dados aberta com sucesso")

# Função para verificar o status do site
def verificar_status(sistema, url):
    print(f"Testando: {sistema} ({url})...")

    data_hora_teste = datetime.now()
    status = False
    tempo_resposta = None
    erro = None

    try:
        inicio_teste = time.time()
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)  
        tempo_resposta = time.time() - inicio_teste
        tempo_resposta = round(tempo_resposta, 2)  # Formatar para duas casas decimais
        status_code = response.status_code

        if status_code == 200:
            status = True
            print(f"{sistema} está no ar! (HTTP {status_code})")
        else:
            erro = f"Status inesperado: {status_code}"
            print(f"{sistema} respondeu com status inesperado: {status_code}")

    except Exception as e:
        erro = str(e)
        print(f"Erro ao acessar {sistema}: {e}")

    # Inserir os resultados no banco de dados
    conexao_banco.execute(
        "INSERT INTO disponibilidade_sistemas (sistema, url, data_hora_teste, status, tempo_resposta, erro) VALUES (%s, %s, %s, %s, %s, %s)",
        (sistema, url, data_hora_teste, status, tempo_resposta, erro)
    )
    conexao.commit()

# Executando os testes para cada sistema no JSON
for sistema in sistemas:
    verificar_status(sistema["sistema"], sistema["url"])
    time.sleep(2)  # Pequeno intervalo entre testes para evitar sobrecarga

print("Testes concluídos!")

# Fechar a conexão com o banco de dados
conexao_banco.close()
conexao.close()
print("Conexão com o banco de dados fechada com sucesso")