import json
import os
import subprocess
import re
import time

# 📌 Define o caminho absoluto do JSON de domínios
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

# 📌 Caminho correto para o testssl.sh
testssl_path = os.path.join(script_dir, "../testssl/testssl.sh")

# 📌 Tempo máximo permitido para cada teste SSL (segundos)
SSL_TIMEOUT = 120  

# 📌 Função para verificar SSL de um sistema
def verificar_ssl(sistema, url):
    print(f"\n🔍 Testando: {sistema} ({url})...")

    try:
        # ⏳ Executa testssl.sh com timeout
        process = subprocess.run(
            [testssl_path, url],
            text=True,
            capture_output=True,
            timeout=SSL_TIMEOUT  # 🔥 Timeout definido
        )

        output = process.stdout

        # 🔎 Extraindo informações importantes
        cert_common_name_match = re.search(r"Common Name \(CN\)\s+([\S]+)", output)
        cert_days_left_match = re.search(r"expires < \d+ days \((\d+)\)", output)
        cert_trust_status_match = re.search(r"Trust \(hostname\)\s+(.+)", output)

        # 🔎 Capturando a nota SSL (Overall Grade)
        overall_grade_match = re.search(r"Overall Grade\s+([A-F]\+?)", output)

        # 📌 Capturando Final Score como alternativa, caso Overall Grade não esteja disponível
        final_score_match = re.search(r"Final Score\s+(\d+)", output)

        # 🔎 Extraindo cabeçalhos de segurança da resposta HTTP
        hsts_match = re.search(r"Strict Transport Security\s+([\S ]+)", output)
        x_frame_options_match = re.search(r"X-Frame-Options:\s+([\S ]+)", output)
        xss_protection_match = re.search(r"X-XSS-Protection:\s+([\S ]+)", output)

        # 📌 Processando os dados capturados
        cert_common_name = cert_common_name_match.group(1) if cert_common_name_match else "N/A"
        cert_days_left = cert_days_left_match.group(1) if cert_days_left_match else "N/A"
        cert_trust_status = cert_trust_status_match.group(1).strip() if cert_trust_status_match else "N/A"
        overall_grade = overall_grade_match.group(1).strip() if overall_grade_match else "Não disponível"
        if overall_grade == "Não disponível" and final_score_match:
            overall_grade = f"Score: {final_score_match.group(1)}"

        hsts_status = hsts_match.group(1) if hsts_match else "Não implementado"
        x_frame_options = x_frame_options_match.group(1) if x_frame_options_match else "Não definido"
        xss_protection = xss_protection_match.group(1) if xss_protection_match else "Não definido"

        # 📌 Evitar saída duplicada - agora garantimos que apenas um bloco será impresso
        print("\n✅ **Resumo do Teste SSL** ✅")
        print(f"- Host: {url}")
        print(f"- Certificado Comum: {cert_common_name}")
        print(f"- Dias até Expiração: {cert_days_left}")
        print(f"- Status de Confiança: {cert_trust_status}")
        print(f"- Nota Geral do SSL: {overall_grade}")

        print("\n🛡 **Segurança HTTP** 🛡")
        print(f"- Strict Transport Security (HSTS): {hsts_status}")
        print(f"- X-Frame-Options: {x_frame_options}")
        print(f"- X-XSS-Protection: {xss_protection}")

        # 🚨 Filtrando vulnerabilidades reais (removendo "not vulnerable")
        vulnerabilities = re.findall(r"(?:potentially NOT ok|vulnerable).*", output)
        vulnerabilities = [vuln.strip() for vuln in vulnerabilities if "(OK)" not in vuln]

        if vulnerabilities:
            print("\n⚠ **Vulnerabilidades Encontradas:**")
            for vuln in vulnerabilities:
                print(f"- {vuln}")
        else:
            print("\n✅ Nenhuma vulnerabilidade crítica encontrada.")

    except subprocess.TimeoutExpired:
        print(f"⏳ {sistema} demorou muito para responder. Timeout após {SSL_TIMEOUT}s!")
    except Exception as e:
        print(f"❌ Erro ao executar testssl.sh para {sistema}: {e}")

# 📌 Executando os testes para cada sistema no JSON
for sistema in sistemas:
    verificar_ssl(sistema["sistema"], sistema["url"])
    time.sleep(2)  # ⏳ Pequeno intervalo entre testes para evitar sobrecarga

print("\n✅ Testes concluídos!")
