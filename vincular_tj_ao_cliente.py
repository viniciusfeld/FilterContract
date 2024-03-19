from utils import conectar_db

def adicionar_coluna_empresa():
    conn, cursor = conectar_db()
    
    cursor.execute("PRAGMA table_info(contratos);")
    colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]

    if 'Empresa' not in colunas_existentes:
        # A coluna 'Empresa' não existe, então podemos adicioná-la
        cursor.execute("ALTER TABLE contratos ADD COLUMN Empresa TEXT")

        conn.commit()
        print("Coluna 'Empresa' adicionada com sucesso.")
    else:
        print("A coluna 'Empresa' já existe na tabela.")

    conn.close()

    
   
adicionar_coluna_empresa()
