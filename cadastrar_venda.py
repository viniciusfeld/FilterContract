import requests
from utils import conectar_db, buscar_todos_registros

def alterar_produto():
    conn, cursor = conectar_db()
    cursor.execute("UPDATE contratos SET Produto = 'PIS/FOLHA PERSE' WHERE Produto = 'PIS-FOLHA'")
    conn.commit()
    conn.close()

def buscar_produto_nome(nome_produto):
    conn, cursor = conectar_db()
    cursor.execute(f'SELECT * FROM Produtos WHERE Nome = ?', (nome_produto, ))
    
    return cursor.fetchone()

def buscar_pessoa(url):
    response = requests.get(url)

    if response.status_code == 200:
        dados_api = response.json()
        return dados_api
    
    print(f"Falha ao obter dados de busca. Código de resposta: {response.status_code}")
    return None

def cadastrar_entidades():
    cadastros = buscar_todos_registros()
    
    for cadastro in cadastros:
        cnpj_client = cadastro[3]
        cnpj_tj = cadastro[6]
        produto = cadastro[4]
        
        produtoDb = buscar_produto_nome(produto)
        
        
        if cnpj_tj != None:
            clienteComprasoft = buscar_pessoa(f'http://localhost:5046/api/Person/buscar-cpfCnpj/{cnpj_client}')
            tjComprasoft = buscar_pessoa(f'http://localhost:5046/api/Person/buscar-cpfCnpj/{cnpj_tj}')
          
            venda = {
                "ClientId": clienteComprasoft['id'],
                "CompanyId": tjComprasoft['id']
            }
                
            response_venda = requests.post('http://localhost:5046/api/Sales', json=venda)
            
            if response_venda.status_code == 200:
                dados_api = response_venda.json()
                item_venda = {
                    "SaleId": dados_api['id'],
                    "ProductId": produtoDb[0],
                    "PercentHonoraryProduct": float(cadastro[5])
                }
                
                response_item_venda = requests.post('http://localhost:5046/api/SaleItems', json=item_venda)
                
                if response_item_venda.status_code == 200:
                    print("✅ venda item cadastrada")
                else:
                    print("❌ erro ao cadastrar venda item")
            else:
                print("❌ erro ao cadastrar venda")
        else:
            print("❌ Não cnpj da TJ")

cadastrar_entidades()
