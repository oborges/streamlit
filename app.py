import streamlit as st
import pandas as pd
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import os

# Configurações do IBM Cloud Object Storage
COS_ENDPOINT = "https://s3.br-sao.cloud-object-storage.appdomain.cloud"  # URL do seu endpoint do COS
#COS_API_KEY_ID = "YOUR_API_KEY"  # Substitua pela sua API Key
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/dd38434108cf46bfa9849bbaa8c80aac:adfe9ea8-a98d-4257-a513-c350a23d8483::"  # Substitua pelo CRN da sua instância

# Função para conectar ao IBM COS
def connect_cos():
    cos = ibm_boto3.resource(
        "s3",
        ibm_service_instance_id=COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT,
    )
    return cos

# Função para carregar dados do CSV no COS
def load_data_from_cos(cos, bucket_name, file_key):
    try:
        obj = cos.Object(bucket_name, file_key).get()
        data = pd.read_csv(obj['Body'], sep='\t')  # Separe conforme o delimitador do seu arquivo
        return data
    except ClientError as be:
        st.error(f"Erro ao acessar o arquivo: {be}")
        return pd.DataFrame()

# Função para filtrar os dados
def filter_data(df):
    st.sidebar.header("Filtros")
    categoria = st.sidebar.multiselect("Categoria da IES", options=df['CATEGORIA_DA_IES'].unique())
    situacao = st.sidebar.multiselect("Situação", options=df['SITUACAO_IES'].unique())

    if categoria:
        df = df[df['CATEGORIA_DA_IES'].isin(categoria)]
    if situacao:
        df = df[df['SITUACAO_IES'].isin(situacao)]

    return df

# Título e descrição do app
st.title("Instituições de Ensino Superior do Brasil")
st.markdown("Explore as Instituições de Ensino Superior do Brasil de forma interativa.")

# Conectando ao COS
cos = connect_cos()
bucket_name = "olavo-streamlit"
file_key = "PDA_Lista_Instituicoes_Ensino_Superior_do_Brasil_EMEC.csv"

# Carregando os dados
df = load_data_from_cos(cos, bucket_name, file_key)

# Mostrando dados filtrados
if not df.empty:
    filtered_df = filter_data(df)
    st.dataframe(filtered_df)
else:
    st.error("Erro ao carregar os dados.")


