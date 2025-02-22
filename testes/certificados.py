import json
import os
import subprocess
import re
import psycopg2
from datetime import datetime

# Para um uso mais dinamico vamos usar os.path, assim conseguimos pegar o ponto atual 
# do nosso script e dai encotrar mais facilmente outros arquivo que vamos precisar
#obtendo o caminho do script certificados
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

#caminho do nosso arquivo json
caminhoJson = os.path.join(diretorio_atual, "..", "json", "dominios.json")
caminhoSSL = os.path.join(diretorio_atual, "..", "testssl", "testssl.sh")

#Aqui fazemos o conectamento com o banco de dados
conexao = psycopg2.connect(
    dbname="monitoramento_aplicacoes",
    user="user",
    password="123456789",
    host="localhost",
    port="5432"
)
conexao_banco = conexao.cursor()
print("Abrindo conexão com o banco de dados")

#abrir o arquivo, usamos o with para encerrar o processo após lermos o arquivo
with open(caminhoJson, "r", encoding="utf-8") as arquivo:
    dominiosjson = json.load(arquivo)

# Função para remover caracteres ANSI
def remover_ansi(texto):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', texto)

#Aqui pecorremos o json de dominios
for dominio in dominiosjson:
    # print(f"Sistema: {dominio['sistema']}, URL: {dominio['url']}")

    #agora iremos realizar o teste do ssl
    
    #definindo comando do testessl
    comandossl = [caminhoSSL, dominio["url"]]

    # Nome do arquivo de saída específico para cada domínio
    arquivo_resultado = f"./testes/resultado_testssl_{dominio['url'].replace('https://', '').replace('.', '_')}.txt"

    #execultando o testessl
    try:
        processoSSL = subprocess.Popen(comandossl, stdout=subprocess.PIPE, text=True)
        print("Iniciando testeSSL")

        #aguardando o testessl terminar de rodar com timeout de 150 segundos (2,5 minutos)
        processoSSL.wait(timeout=300)

        #fazendo o salvamento da saida
        #com o with podemos encerrar o processo de abrir e salvar o arquivo
        with open(arquivo_resultado, "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(processoSSL.stdout.read())
            print("Relatório salvo com sucesso", arquivo_resultado)

        #Abrindo o arquivo para filtrar os dados que queremos
        with open(arquivo_resultado, "r", encoding="utf-8") as relatorio:
            linhas_relatorio = relatorio.readlines()
            print("Lendo relatorio para aplicar filtro")

            #aconteceu de haver mais de um dado do tipo que queremos selecionar, para evitar repetições
            #adicionamos esse controle para armazenar  apenas uma vez, assim se um valor existir mais de uma
            #vez no relatorio ele será salvo apenas uma vez
            dominios_encotrados = set()
            dias_de_expiracao = set()
            vulnerabilidades_encontradas = set()
            #Variaveis de armazenamento dos dados
            falhas_seguranca = False
            hora_inicio_teste = None
            dias_restantes = None
            nota = None

            for linha in linhas_relatorio:
                #regex que filtra o dominio
                relatorio_dominio = re.search(r'-->> \d+\.\d+\.\d+\.\d+:\d+ \(([^)]+)\) <<--', linha)
                if relatorio_dominio:
                    dominio_teste = relatorio_dominio.group(1)
                    if dominio_teste not in dominios_encotrados:
                        dominios_encotrados.add(dominio_teste)
                        print("Dominio do teste:", dominio_teste)

                #regex tempo de inicio do teste
                relatorio_start = re.search(r'\[7m Start (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', linha)
                if relatorio_start:
                    hora_inicio_teste = relatorio_start.group(1)
                    print("Horario de inicio", hora_inicio_teste)        

                #regex que filtra a data de expiração
                relatorio_dias_restantes = re.search(r'ok > (\d+) days', linha) 
                if relatorio_dias_restantes:
                    dias_restantes = relatorio_dias_restantes.group(1)
                    if dias_restantes not in dias_de_expiracao:
                        dias_de_expiracao.add(dias_restantes)
                        print("Dias restantes do certificado", dias_restantes)

                #regex para extrair a nota geral do teste
                relatorio_nota = re.search(r'Overall Grade\s+(\S+)' , linha)
                if relatorio_nota:
                    nota = relatorio_nota.group(1)
                    nota = remover_ansi(nota)  # Remover caracteres ANSI
                    print("Nota geral do teste", nota)

                #regex onde pegamos as vulnerabilidades
                relatorio_vulnerabilidade = re.search(r'(potentially NOT ok|VULNERABLE)', linha)
                if relatorio_vulnerabilidade:
                    vulnerabilidade = remover_ansi(linha.strip())  # Remover caracteres ANSI
                    vulnerabilidades_encontradas.add(vulnerabilidade)

            #verificando se alguma vulnerabilidade foi encontrada
            if vulnerabilidades_encontradas:
                falhas_seguranca = True
                print("Falhas de segurança:", falhas_seguranca)
                vulnerabilidades_concatenadas = "\n".join(vulnerabilidades_encontradas)
                conexao_banco.execute(
                    "INSERT INTO ssl_test_results (dominio, hora_inicio_teste, dias_restantes, nota, vulnerabilidade, vulneravel, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (dominio["url"], hora_inicio_teste, dias_restantes, nota, vulnerabilidades_concatenadas, True, None)
                )
                print("////////// TESTE CONCLUIDO ///////////")
            else:
                print("sem vulnerabilidade")
                conexao_banco.execute(
                    "INSERT INTO ssl_test_results (dominio, hora_inicio_teste, dias_restantes, nota, vulnerabilidade, vulneravel, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (dominio["url"], hora_inicio_teste, dias_restantes, nota, None, False, None)
                )
                print("////////// TESTE CONCLUIDO ///////////")

            #apagando o arquivo relatório que foi gerado
            if os.path.exists(arquivo_resultado):
                os.remove(arquivo_resultado)
                print("Relatório apagado com sucesso")

    except subprocess.TimeoutExpired:
        print(f"Timeout: O teste SSL para {dominio['url']} demorou mais de 5 minutos e foi cancelado.")
        processoSSL.kill()
        hora_inicio_teste = datetime.now()
        conexao_banco.execute(
            "INSERT INTO ssl_test_results (dominio, hora_inicio_teste, dias_restantes, nota, vulnerabilidade, vulneravel, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (dominio["url"], hora_inicio_teste, None, None, None, False, "Timeout: O teste SSL demorou mais de 5 minutos e foi cancelado.")
        )
        if os.path.exists(arquivo_resultado):
            os.remove(arquivo_resultado)

#commit e fechamento da conexão com o banco
conexao.commit()
conexao_banco.close()
conexao.close()
print("Fechando conexão com o banco de dados")




