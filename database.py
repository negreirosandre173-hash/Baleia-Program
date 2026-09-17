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

def salvar_no_banco(nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario):
    query = """
    INSERT INTO insumos (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario))
    except Exception as erro:
        print(f"Erro ao inserir insumo no banco de dados: {erro}")
        raise erro

def obter_insumos():
    comando_sql = "SELECT nome FROM insumos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql)
                resultados = cursor.fetchall()
                return [linha[0] for linha in resultados]
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
                    # 1. Pega o valor digitado e limpa os espaços
                    qtd_original = str(insumo["quantidade"]).strip()
                    
                    # 2. Se o usuário usar vírgula (ex: 2,5), padroniza para ponto (2.5)
                    qtd_original = qtd_original.replace(",", ".")
                    
                    # 3. Converte para float (ou deixa 0.0 se estiver vazio)
                    qtd_final = float(qtd_original) if qtd_original else 0.0

                    cursor.execute(query, (
                        produto_dados["nome"],
                        produto_dados["codigo"],
                        insumo["nome"],
                        insumo["categoria"],
                        qtd_final # Envia o valor exato para o banco
                    ))
        print('Produto e seus insumos inseridos com sucesso!')
    except Exception as e:
        print(f"Erro ao salvar produto no banco: {e}")
        raise e


