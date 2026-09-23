import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def obter_conexao():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )


def salvar_no_banco(nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade):

    try:
        qtd_float = float(quantidade) if quantidade else 1.0
        if qtd_float == 0: qtd_float=1.0
        preco_unitario = float(custo)/qtd_float
    except Exception:
        preco_unitario= 0.0

    query = """
    INSERT INTO insumos (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade, preco_unitario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade, preco_unitario))
    except Exception as erro:
        print(f"Erro ao inserir insumo no banco de dados: {erro}")
        raise erro

def obter_insumos():
    comando_sql = "SELECT id FROM insumos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql)
                resultados = cursor.fetchall()
                return [{"id":linha[0],"nome":linha[1]} for linha in resultados]
    except Exception as erro:
        print(f"Erro ao buscar insumos: {erro}")
        return []


def salvar_produto(produto_dados):
    query = """
    INSERT INTO produtos (nome_produto, novo_codigo, novo_insumo, nova_categoria, nova_qtd)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                for insumo in produto_dados["insumos"]:
                    qtd_original = str(insumo["quantidade"]).strip()

                    cursor.execute(query, (
                        produto_dados["nome"],
                        produto_dados["codigo"],
                        insumo["insumo_id"],
                        insumo["categoria"],
                        qtd_original 
                    ))
        print('Produto e seus insumos inseridos com sucesso!')
    except Exception as e:
        print(f"Erro ao salvar produto no banco: {e}")
        raise e


import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def obter_conexao():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )


def salvar_no_banco(nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade):
    
    try:
        qtd_float = float(quantidade) if quantidade else 1.0
        if qtd_float == 0: qtd_float = 1.0
        preco_unitario = float(custo) / qtd_float
    except Exception:
        preco_unitario = 0.0

    query = """
    INSERT INTO insumos (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade))
    except Exception as erro:
        print(f"Erro ao inserir insumo: {erro}")
        raise erro


def obter_insumos():
    comando_sql = "SELECT id, nome FROM insumos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql)
                resultados = cursor.fetchall()
               
                return [{"id": linha[0], "nome": linha[1]} for linha in resultados]
    except Exception as erro:
        print(f"Erro ao buscar insumos: {erro}")
        return []


def salvar_produto(produto_dados):
    query = """
    INSERT INTO produtos (nome_produto, novo_codigo, novo_insumo, nova_categoria, nova_qtd)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                for insumo in produto_dados["insumos"]:
                    qtd_original = str(insumo["quantidade"]).strip()

                    cursor.execute(query, (
                        produto_dados["nome"],
                        produto_dados["codigo"],
                        insumo["insumo_id"],  
                        insumo["categoria"],
                        qtd_original 
                    ))
        print('Produto e seus insumos inseridos com sucesso!')
    except Exception as e:
        print(f"Erro ao salvar produto no banco: {e}")
        raise e









