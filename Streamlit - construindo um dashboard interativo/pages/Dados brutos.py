import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso', icon= "✅")
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS:')

## Buscando dados
url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
with st.sidebar.expander('Categoria do produto'):
    categoria_produto = st.multiselect('Selecione a categoria do produtos', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco =st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander('Frete'):
    frete =st.slider('Selecione o frete', 0, 24, (0,1000))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))        
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.multiselect('Selecione a avaliação da compra', dados['Avaliação da compra'].unique(), dados['Avaliação da compra'].unique())
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    parcelas =st.multiselect('Selecione a quantidade de parcelas', dados['Quantidade de parcelas'].unique(), dados['Quantidade de parcelas'].unique())


query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria_produto and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local_compra and \
`Avaliação da compra` in @avaliacao and \
`Tipo de pagamento` in @tipo_pagamento and \
`Quantidade de parcelas` in @parcelas 
'''    
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]
st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility= 'collapsed', value= 'dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name= nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)    
