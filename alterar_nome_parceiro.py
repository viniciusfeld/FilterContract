import pandas as pd
from utils import conectar_db
import logging


def configurar_logger(name_file):
    logging.basicConfig(filename=f'{name_file}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    
def alterar_nome_parceiro(nome_parceiro, novo_nome_parceiro):
    conn, cursor = conectar_db()
    
    cursor.execute(f'SELECT * FROM contratos WHERE Parceiro = ?', (nome_parceiro,))
    parceiro = cursor.fetchone()
    
    if parceiro:
        cursor.execute(f'UPDATE contratos SET Parceiro = ? WHERE Parceiro = ?', (novo_nome_parceiro, nome_parceiro))
        conn.commit()
        print("Nome alterado")
    else: 
        logging.error(f""" Parceiro não localizado: {nome_parceiro}""")
   
    conn.close()

def atualizar():
    configurar_logger("log_errors_atualiza_nome_parceiro")
    df = pd.read_excel("Planilhas/AlteracaoNomeParceiros.xlsx")
    
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
            nome_parceiro = str(row['Nome antigo'])
            novo_nome_parceiro = str(row['Nome novo'])
            alterar_nome_parceiro(nome_parceiro, novo_nome_parceiro)
    print("\n")

# atualizar()
alterar_nome_parceiro("GENTIL APARICIO - ANNONI ", "GENTIL APARICIO - ANNONI")