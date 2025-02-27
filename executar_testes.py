import subprocess
import time
import os
from datetime import datetime

# Buscando o diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho dos testes de disponibilidade
disponibilidade_teste = os.path.join(diretorio_atual, ".", "testes", "disponibilidade_sistemas.py")

# Caminho dos testes de certificados
certificados_teste = os.path.join(diretorio_atual, ".", "testes", "certificados.py")

# Definindo o intervalo de tempo que os testes acontecem
tempo_disponibilidade_teste = 2 * 60  # 2 minutos

def teste_disponibilidade(disponibilidade_teste):
    try:
        # Rodando teste de disponibilidade
        subprocess.run(["python3", disponibilidade_teste], check=True)
        print(f"Teste de disponibilidade realizado com sucesso às: {time.ctime()}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar teste de disponibilidade às: {time.ctime()} erro: {e}")

def teste_certificados(certificados_teste):
    try:
        # Rodando teste de certificados
        subprocess.run(["python3", certificados_teste], check=True)
        print(f"Teste de certificados realizado com sucesso às: {time.ctime()}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar teste de certificados às: {time.ctime()} erro: {e}")

# Função principal para agendar e executar os testes
def executar_testes():
    ultimo_teste_certificados = None

    while True:
        # Executar teste de disponibilidade a cada 2 minutos
        teste_disponibilidade(disponibilidade_teste)
        time.sleep(tempo_disponibilidade_teste)

        # Verificar se é meia-noite para executar o teste de certificados
        agora = datetime.now()
        if agora.hour == 0 and agora.minute == 0:
            if ultimo_teste_certificados is None or ultimo_teste_certificados.date() < agora.date():
                teste_certificados(certificados_teste)
                ultimo_teste_certificados = agora

if __name__ == "__main__":
    executar_testes()