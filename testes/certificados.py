import json
import os
import subprocess
import re

# Para um uso mais dinamico vamos usar os.path, assim conseguimos pegar o ponto atual 
# do nosso script e dai encotrar mais facilmente outros arquivo que vamos precisar
#obtendo o caminho do script certificados
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

#caminho do nosso arquivo json
caminhoJson = os.path.join(diretorio_atual, "..", "json", "dominios.json")
caminhoSSL = os.path.join(diretorio_atual, "..", "testssl", "testssl.sh")


#abrir o arquivo, usamos o with para encerrar o processo após lermos o arquivo
with open(caminhoJson, "r", encoding="utf-8") as arquivo:
    dominiosjson = json.load(arquivo)

#Aqui pecorremos o json de dominios
for dominio in dominiosjson:
    # print(f"Sistema: {dominio['sistema']}, URL: {dominio['url']}")

    #agora iremos realizar o teste do ssl
    
    #definindo comando do testessl
    comandossl = [caminhoSSL, dominio["url"]]

    #aqui definimos o nome do relatorio para cada dominio, assim cada relatorio tem um nome único
    arquivo_resultado = f"./testes/resultado_testssl_{dominio['url'].replace('https://', '').replace('.', '_')}.txt"

    #execultando o testessl
    processoSSL = subprocess.Popen(comandossl, stdout=subprocess.PIPE, text=True)
    print("Iniciando testeSSL")

    #aguardando o testessl terminar de rodar
    processoSSL.wait()

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

        for linha in linhas_relatorio:
            #regex que filtra o dominio
            relatorio_dominio = re.search(r'-->> \d+\.\d+\.\d+\.\d+:\d+ \(([^)]+)\) <<--', linha)
            if relatorio_dominio:
                dominio = relatorio_dominio.group(1)
                if dominio not in dominios_encotrados:
                    dominios_encotrados.add(dominio)
                    print(dominio)

            #regex que filtra a data de expiração
            relatorio_dias_restantes = re.search(r'ok > (\d+) days', linha) 
            if relatorio_dias_restantes:
                dias_restantes = relatorio_dias_restantes.group(1)
                if dias_restantes not in dias_de_expiracao:
                    dias_de_expiracao.add(dias_restantes)
                    print(dias_restantes)
                
       
