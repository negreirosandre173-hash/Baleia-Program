import os
import psycopg2
from dotenv import load_dotenv
import flet as ft

load_dotenv()


# def geral para conexao
def obter_conexao():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

# aqui recolhe os dados para salvar
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

# envia os dados do cadastro de insumos para o banco de dados
def enviar_clicado(
    e, 
    txt_nome,
    txt_codigo,
    txt_uni_medi,
    txt_custo,
    txt_data,
    txt_fornecedor,
    txt_telefone,
    txt_email,
    txt_comentario,
    txt_qtd,
    lbl_status
):
    page = e.page
    nome = txt_nome.value.upper() if txt_nome.value else ""
    codigo = txt_codigo.value
    uni_medi = txt_uni_medi.value
    custo = txt_custo.value
    data_cadastro = txt_data.value
    fornecedor = txt_fornecedor.value.upper() if txt_fornecedor.value else ""
    telefone = txt_telefone.value
    email = txt_email.value
    comentario = txt_comentario.value
    quantidade = txt_qtd.value

    if not nome or not codigo or not uni_medi or not custo or not data_cadastro:
        lbl_status.value = "Preencha os campos obrigatórios!"
        lbl_status.color = ft.Colors.RED
        page.update()
        return

    try:
        custo_limpo = custo.replace(".", "").replace(",", ".")
        custo_float = float(custo_limpo)
        codigo_int = int(codigo)

        salvar_no_banco(nome, codigo_int, uni_medi, custo_float, data_cadastro, fornecedor, telefone, email, comentario, quantidade)
        
        lbl_status.value = "Insumo cadastrado!"
        lbl_status.color = ft.Colors.GREEN
        
        txt_nome.value = ""
        txt_codigo.value = ""
        txt_uni_medi.value = None
        txt_custo.value = ""
        txt_data.value = ""
        txt_fornecedor.value = ""
        txt_telefone.value = ""
        txt_email.value = ""
        txt_comentario.value = ""
        txt_qtd.value = ""

    except Exception as erro:
        lbl_status.value = f"Erro ao salvar: {erro}"
        lbl_status.color = ft.Colors.RED

    page.update()

# lista todos os insumos do cadastro de produtos
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

# def que lista produtos e suas respectivas informacoes
def obter_produtos():
    
    comando_sql_produtos = "SELECT DISTINCT novo_codigo, nome_produto FROM produtos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql_produtos)
                resultados_produtos = cursor.fetchall()
                return [{"novo_codigo": linha[0], "nome_produto": linha[1]} for linha in resultados_produtos]
    except Exception as erro:
        print(f"Erro ao buscar produtos: {erro}")
        return []


# def responsavel pelos cadastros dos produtos
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

# def que lista informacoes operacionais de produtos
def obter_detalhes_receita_view(nome_produto):
    query = 'SELECT "Ingrediente", "Quantidade", "Unidade", "Custo" FROM vw_relatorio_custos WHERE "Produto" = %s;'
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome_produto,))
                return cursor.fetchall()  
    except Exception as e:
        print(f"Erro ao buscar detalhes da view para {nome_produto}: {e}")
        return None



# def busca produto para edicao
def obter_todos_produtos():
    comando_sql_produtos = "SELECT DISTINCT novo_codigo, nome_produto FROM produtos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql_produtos)
                resultados_produtos = cursor.fetchall()
                return [{"novo_codigo": linha[0], "nome_produto": linha[1]} for linha in resultados_produtos]
    except Exception as erro:
        print(f"Erro ao buscar produtos: {erro}")
        return []





# def que busca o nome do produto para edicao
def obter_nome_produto():
    query = 'SELECT DISTINCT "nome_produto" FROM produtos ORDER BY "nome_produto";'
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                return [nome_produto[0] for nome_produto in cursor.fetchall()]
    except Exception as e:
        print(f"deu erro:{e}")
        return []

# ALTERAÇÃO: Agora a função é pura de banco, recebe o nome direto como texto string
def deletar_produto_por_nome(nome_produto):
    if not nome_produto:
        raise ValueError("Nenhum produto selecionado.")

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            sql_delete = "DELETE FROM produtos WHERE nome_produto = %s"
            cursor.execute(sql_delete, (nome_produto,))
            conexao.commit()


