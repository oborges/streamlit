# Use uma imagem base Python
FROM python:3.9

# Instale as dependências
RUN pip install streamlit pandas ibm_boto3

# Copie o código do app
COPY app.py /app/

# Defina o diretório de trabalho
WORKDIR /app

# Comando para iniciar o app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

