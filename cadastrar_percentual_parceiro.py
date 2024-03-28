import pandas as pd
from utils import conectar_db, remover_mascara, consultar_clientes_local


def criar_tabelas():
    conn, cursor = conectar_db()
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratosPercentualModelo (
            Id INTEGER PRIMARY KEY,
            Parceiro TEXT NOT NULL,
            Cliente_cnpj TEXT,
            Produto TEXT,
            Percentual_honorario_produto TEXT,
            Percentual_honorario_parceiro TEXT,
            Mes_faturado DATE
        )
    ''')

    conn.commit()
    conn.close()

def cadastrar_empresa_tj_local(id_contrato_local, cnpj_empresa):
    conn, cursor = conectar_db()
    cursor.execute(f'UPDATE contratos SET Empresa = {cnpj_empresa} WHERE Id = {id_contrato_local}')
    conn.commit()
    conn.close()

def cadastrar_entidades(df):
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        cnpj_cliente = row['CNPJ']
        parceiro = row['PARCEIRO']
        produto = row['PRODUTO']
        percentual_produto = row["%"]
        valor_honorario = row['HONORARIOS']
        
        
        
        if pd.notna(cnpj) and cnpj != 0 and cnpj != "":
            cnpj_sem_mascara = remover_mascara(cnpj)
            clientes = consultar_clientes_local(cnpj_sem_mascara)
            
            print("Consulta:", clientes)
            
            if len(clientes) != 0:
                for cliente in clientes:
                    id_item_contrato_local = cliente[0]
                    produto_contrato_local = cliente[4]
                    percentual_contrato_local = float(cliente[5])
                    if empresa == 'MAW':
                        cnpj_empresa_tj = "38661672000110"
                    if empresa == 'TJT':
                        cnpj_empresa_tj = "51979018000118"
                    else:
                        cnpj_empresa_tj = "30317269000167"
                    
                    if produto_contrato_local == produto and percentual_contrato_local == percentual:
                        cadastrar_empresa_tj_local(id_item_contrato_local, cnpj_empresa_tj)
                        
    print("\n")    

nome_do_arquivo = 'C:\tributo\FilterContract\Planilhas\Planilhas\Planilha_-_Comissoes_-_2023-Copy.xlsx'
nome_da_planilha = 'FEVEREIRO-012023'

df_comissoes = pd.read_excel(nome_do_arquivo, sheet_name=nome_da_planilha)

cadastrar_entidades(df_comissoes)

criar_tabelas()
print('Concluído! As empresas foram adicionadas ao banco de dados, as divergentes foram salvas em Clientes_divergentes.txt. Os dados completos foram exportados para dados_empresas.txt.')

# Tratar produtos da minha tabela comprasoft para a planilha 'Clientes_por_empresa'
# comparar itens da planilha para cadastrar as vendas
