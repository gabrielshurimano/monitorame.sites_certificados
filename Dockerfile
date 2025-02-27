# Usando uma imagem base do python
FROM python:3.9

# Aqui estamos dizendo onde é o nosso diretório de trabalho
WORKDIR /app

# Instalando as dependências que vamos precisar pra rodar tudo diretamente no Dockerfile
RUN apt-get update && apt-get install -y bsdmainutils dnsutils
RUN pip install --no-cache-dir psycopg2-binary requests python-dotenv schedule

# Copiando os diretórios e arquivos necessários para o container
COPY ./executar_testes.py ./executar_testes.py
COPY ./testes ./testes
COPY ./json ./json
COPY ./testssl ./testssl

# Defina o comando padrão para executar os scripts
CMD ["python3", "./executar_testes.py"]