# Utiliza uma imagem base do Python
FROM python:3.9-slim

# Diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o código da aplicação e o arquivo de configuração
COPY exporter.py exporter.py
COPY endpoints.yml endpoints.yml

# Expõe a porta 5000 para o Flask e 8000 para o Prometheus HTTP server
EXPOSE 5000 8000

# Comando para iniciar o exporter
CMD ["python", "exporter.py"]
