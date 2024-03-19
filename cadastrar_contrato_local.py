import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from utils import conectar_db, remover_mascara

def criar_tabelas():
    conn, cursor = conectar_db()
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            Id INTEGER PRIMARY KEY,
            Parceiro TEXT NOT NULL,
            Cliente TEXT NOT NULL,
            Cliente_cnpj TEXT,
            Produto TEXT,
            Percentual_honorario_produto TEXT
        )
    ''')

    conn.commit()
    conn.close()
           
def adicionar_na_tabela(parceiro, cliente, cliente_cnpj, produto, percentual_honorario_produto):
    conn, cursor = conectar_db()
    cliente_cnpj = remover_mascara(cliente_cnpj)

    cursor.execute(f'SELECT * FROM contratos WHERE Cliente_cnpj = ? AND Parceiro = ? AND produto = ?', (cliente_cnpj, parceiro, produto))
    resultado = cursor.fetchone()
    
    if resultado is None and cliente_cnpj and cliente_cnpj != '0' and cliente_cnpj != '':
        cursor.execute(f"""
                    INSERT INTO contratos 
                    (Parceiro, Cliente, Cliente_cnpj, Produto, Percentual_honorario_produto) 
                    VALUES (?, ?, ?, ?, ?)""", 
                    (parceiro, cliente, cliente_cnpj, produto, percentual_honorario_produto)
        )
                    
        print(f'Adicionado na tabela contratos. Parceiro: {parceiro} | Cliente: {cliente} - {cliente_cnpj} | Produto: {produto}')
    else:
        print(f'Duplicado ou inválido. Parceiro: {parceiro} | Cliente: {cliente} - {cliente_cnpj} | Produto: {produto}')

    conn.commit()
    conn.close()

def cadastrar_entidades(df):
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        compensacao = row['COMPENSAÇÃO']
        if pd.notna(compensacao) and compensacao != 0 and compensacao != "":
            parceiro = str(row['PARCEIRO'])
            cliente = str(row['EMPRESA'])
            cliente_cnpj = str(row['CNPJ'])
            produto = str(row['PRODUTO'])
            percentual_honorario_produto = str(row['%'])
            
            adicionar_na_tabela(parceiro, cliente, cliente_cnpj, produto, percentual_honorario_produto)
    print("\n")

nome_do_arquivo = 'Planilhas/Planilha_-_Comissoes_-_2023-Copy.xlsx'
nome_da_planilha = 'DEZ 13-2023'

df_comissoes = pd.read_excel(nome_do_arquivo, sheet_name=nome_da_planilha)

criar_tabelas()

cadastrar_entidades(df_comissoes)

print('Concluído! As empresas foram adicionadas ao banco de dados, as divergentes foram salvas em Clientes_divergentes.txt. Os dados completos foram exportados para dados_empresas.txt.')
