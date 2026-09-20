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
    INSERT INTO insumos (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade, preco_unitario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome, codigo, uni_medi, custo, data_cadastro, fornecedor, telefone, email, comentario, quantidade, preco_unitario))
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

def calcular_custo_total_produto(codigo_produto):
    
    query = """
        SELECT 
            p.nome_produto,
            SUM(CAST(p.nova_qtd AS REAL) * i.preco_unitario) AS custo_total
        FROM produtos p
        JOIN insumos i ON i.id = CAST(p.novo_insumo AS INTEGER)
        WHERE CAST(p.novo_codigo AS VARCHAR) = %s
        GROUP BY p.novo_codigo, p.nome_produto;
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (str(codigo_produto),))
                resultado = cursor.fetchone()
                
                if resultado:
                    return {
                        "nome_produto": resultado[0],
                        "custo_total": round(resultado[1], 4)
                    }
                return {"nome_produto": "Não encontrado", "custo_total": 0.0}
    except Exception as e:
        print(f"Erro ao calcular custo: {e}")
        return {"nome_produto": "Erro no banco", "custo_total": 0.0}




def buscar_produto(e):

        resultado_container.controls.clear()

        termo_busca = txt_busca.value.strip()

        if not termo_busca:
            resultado_container.controls.append(
                ft.Text("Por favor, digite o nome de um produto.", color="red")
            )
            page.update()
            return

        conn = sqlite3.connect("produtos.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, categoria, preco FROM produtos WHERE nome LIKE ?",
            (f"%{termo_busca}%",),
        )
        produtos = cursor.fetchall()
        conn.close()

        if produtos:
    
            tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Categoria")),
                    ft.DataColumn(ft.Text("Preço (R$)")),
                ],
                rows=[],
            )

            
            for prod in produtos:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(prod[0]))),
                            ft.DataCell(ft.Text(prod[1])),
                            ft.DataCell(ft.Text(prod[2])),
                            ft.DataCell(
                                ft.Text(f"{prod[3]:.2f}")
                            ),  
                        ]
                    )
                )

            resultado_container.controls.append(tabela)
        else:
            resultado_container.controls.append(
                ft.Text("Nenhum produto encontrado.", color="orange")
            )

        
        page.update()
