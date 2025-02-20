import json
import os
import requests
import time
import urllib3

# 📌 Desativa alertas de verificação SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 📌 Define o caminho absoluto do JSON
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "../json/dominios.json")

# 📌 Lendo o JSON de domínios
try:
    with open(json_path, "r", encoding="utf-8") as file:
        sistemas = json.load(file)
        if not sistemas:
            print("⚠ Nenhum domínio encontrado no JSON.")
            exit(1)
except Exception as e:
    print(f"❌ Erro ao carregar o JSON: {e}")
    exit(1)

# 📌 Define cabeçalhos HTTP para simular um navegador real, evitando bloqueios de sites
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

# 📌 Define o timeout máximo para cada requisição
TIMEOUT = 15  

# 📌 Função para verificar o status do site
def verificar_status(sistema, url):
    print(f"\n🔍 Testando: {sistema} ({url})...")

    try:
        # ⏳ Faz a requisição com timeout
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)  
        status_code = response.status_code

        # ✅ Site acessível
        if status_code == 200:
            print(f"✅ {sistema} está no ar! (HTTP {status_code})")
        elif status_code == 403:
            print(f"🚫 {sistema} bloqueou o acesso (HTTP 403). Talvez precise de autenticação ou outro User-Agent.")
        elif status_code == 404:
            print(f"❌ {sistema} não encontrado (HTTP 404). Verifique a URL.")
        elif status_code == 400:
            print(f"⚠ {sistema} retornou erro 400 (Bad Request). O site pode estar protegendo contra bots.")
        else:
            print(f"⚠ {sistema} respondeu com status inesperado: {status_code}")

    # 🔥 Tratamento de erros
    except requests.exceptions.SSLError:
        print(f"❌ {sistema}: Certificado SSL inválido, mas o site pode estar online.")
    except requests.exceptions.Timeout:
        print(f"⏳ {sistema} demorou muito para responder. Timeout após {TIMEOUT}s! O teste foi cancelado.")
    except requests.exceptions.ConnectionError:
        print(f"❌ {sistema}: Não foi possível conectar ao site. Pode estar offline.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar {sistema}: {e}")

# 📌 Executando os testes para cada sistema no JSON
for sistema in sistemas:
    verificar_status(sistema["sistema"], sistema["url"])
    time.sleep(2)  # ⏳ Pequeno intervalo entre testes para evitar sobrecarga

print("\n✅ Testes concluídos!")
