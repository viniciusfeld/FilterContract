import pprint
import requests
import logging
from utils import conectar_db
from pprint import pprint

def configurar_logger(name_file):
    logging.basicConfig(filename=f'{name_file}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def buscar_pessoa(url):
    response = requests.get(url)

    if response.status_code == 200:
        dados_api = response.json()
        return dados_api
    
    print(f"Falha ao obter dados de busca. Código de resposta: {response.status_code}")
    logging.error(f"""
            Erro ao buscar: {url}.
            Error: {response.text}
    """)
    return None

def buscar_por_nome(parceiro_nome):
    url_api = f'http://localhost:5046/api/Person/buscar-nome/{parceiro_nome}'
    
    return buscar_pessoa(url_api)

def buscar_por_cpf_cnpj(cpf_cnpj):
    url_api = f'http://localhost:5046/api/Person/buscar-cpfCnpj/{cpf_cnpj}'
    
    return buscar_pessoa(url_api)

def cadastrar_contrato_comprasoft():
    conn, cursor = conectar_db()
    
    cursor.execute(f'SELECT * FROM contratos')
    contratos = cursor.fetchall()
    
    for contrato in contratos:
        parceiro = contrato[1]
        cnpj_cliente = contrato[3]
        
        parceiro_comprasoft = buscar_por_nome(parceiro)
        if parceiro_comprasoft != None:
            cliente_comprasoft = buscar_por_cpf_cnpj(cnpj_cliente)
            if cliente_comprasoft != None:
                print("Cliente: ", cliente_comprasoft)
                print("\n")
       
    conn.close()
    
    
    print("\n")

configurar_logger("log_errors_cadatrar_contrato_comprasoft")
cadastrar_contrato_comprasoft()