import subprocess
import time
import os

#buscando o diretorio atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

#caminho dos testes
disponibilidade_teste = os.path.join(diretorio_atual, ".", "testes", "disponibilidade_sistemas.py")

#definindo o intervalo de tempo que os testes acontecem
tempo_disponibilidade_teste = 2 * 60

def teste_disponibilidade(disponibilidade_teste, tempo_disponibilidade_teste):
    while True:
        try:
            #rodando teste
            subprocess.run(["python3", disponibilidade_teste], check=True)
            print(f"Teste disponibilidade realizado com sucesso as: {time.ctime()}") 
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar teste de disponibilidade as: {time.ctime()} erro: {e}")

        #aguardando intervalo de tempo
        time.sleep(tempo_disponibilidade_teste)

#chamando a função que roda o teste disponibilidade
teste_disponibilidade(disponibilidade_teste, tempo_disponibilidade_teste)