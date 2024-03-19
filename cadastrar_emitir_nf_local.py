import pandas as pd
from utils import conectar_db, remover_mascara, consultar_clientes_local

nome_do_arquivo = 'Planilhas/Projecao-01.xlsx'

df_projecao = pd.read_excel(nome_do_arquivo)

def verificar_nf(df):
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        nf = row['NF']
        cnpj_cliente = row['CNPJ']
        
        cliente_local = consultar_clientes_local(cnpj_cliente)
        if nf == "SIM":
            pass
        else:
            pass
           
verificar_nf(df_projecao)

