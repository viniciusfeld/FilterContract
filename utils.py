import sqlite3
import os
import logging

def conectar_db():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco_dados = os.path.join(caminho_atual, 'DB', 'comprasoft.db')
    os.makedirs(os.path.dirname(caminho_banco_dados), exist_ok=True)
    
    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()
    
    return conn, cursor

def remover_mascara(item):
    item = ''.join(filter(str.isdigit, item))
    
    return item

def configurar_logger(name_file):
    logging.basicConfig(filename=f'{name_file}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    
def consultar_clientes_local(cnpj):
    conn, cursor = conectar_db()

    cursor.execute(f'SELECT * FROM contratos WHERE Cliente_cnpj = {cnpj}')
    
    return cursor.fetchall()

def buscar_todos_registros():
    conn, cursor = conectar_db()
    cursor.execute(f'SELECT * FROM contratos')
    return cursor.fetchall()

     