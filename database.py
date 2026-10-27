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
def salvar_no_banco(nome, uni_medi, custo, fornecedor, telefone, email, comentario, quantidade):
    
    try:
        qtd_float = float(quantidade) if quantidade else 1.0
        if qtd_float == 0: qtd_float = 1.0
        preco_unitario = float(custo) / qtd_float
    except Exception:
        preco_unitario = 0.0

    query = """
    INSERT INTO insumos (nome, uni_medi, custo, fornecedor, telefone, email, comentario, quantidade )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome, uni_medi, custo, fornecedor, telefone, email, comentario, quantidade))
    except Exception as erro:
        print(f"Erro ao inserir insumo: {erro}")
        raise erro

# envia os dados do cadastro de insumos para o banco de dados
def enviar_clicado(
    e, 
    txt_nome,
    txt_uni_medi,
    txt_custo,
    txt_fornecedor,
    txt_telefone,
    txt_email,
    txt_comentario,
    txt_qtd,
    lbl_status
):
    page = e.page
    nome = txt_nome.value.upper() if txt_nome.value else ""
    uni_medi = txt_uni_medi.value
    custo = txt_custo.value
    fornecedor = txt_fornecedor.value.upper() if txt_fornecedor.value else ""
    telefone = txt_telefone.value
    email = txt_email.value
    comentario = txt_comentario.value
    quantidade = txt_qtd.value

    if not nome or not uni_medi or not custo:
        lbl_status.value = "Preencha os campos obrigatórios!"
        lbl_status.color = ft.Colors.RED
        page.update()
        return

    try:
        custo_limpo = custo.replace(".", "").replace(",", ".")
        custo_float = float(custo_limpo)


        salvar_no_banco(nome, uni_medi, custo_float, fornecedor, telefone, email, comentario, quantidade)
        
        lbl_status.value = "Insumo cadastrado!"
        lbl_status.color = ft.Colors.GREEN
        
        txt_nome.value = ""
        txt_uni_medi.value = None
        txt_custo.value = ""
        txt_fornecedor.value = ""
        txt_telefone.value = ""
        txt_email.value = ""
        txt_comentario.value = ""
        txt_qtd.value = ""

    except Exception as erro:
        print(f"{erro}")
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

# Def que salva os dados do produto no db

def salvar_dados(e, nome_produto,
                    lista_referencias_insumos,
                    coluna_insumos,
                    sugestoes,
                    validar_numeros,
                    dados_banco
                    ):
    page = e.control.page

    produto_final = {
        "nome": nome_produto.value.upper(),
        "insumos": []
    }
    
    for insumo in lista_referencias_insumos:
        nome_valor = insumo["nome"].value if insumo["nome"].value else ""
        
        if nome_valor:
            id_insumo = None
            for item in dados_banco:
                if item["nome"] == nome_valor:
                    id_insumo = item["id"]
                    break
            
            insumo_identificador = id_insumo if id_insumo is not None else nome_valor
            
            qtd_texto = insumo["qtd"].value if insumo["qtd"].value else "0"
            qtd_limpa = qtd_texto.replace(",", ".")
            
            produto_final["insumos"].append({
                "insumo_id": insumo_identificador,  
                "categoria": insumo["categoria"].value,
                "quantidade": qtd_limpa
            })
    
    salvar_produto(produto_final)
  
    nome_produto.value = ""
    lista_referencias_insumos.clear()
    coluna_insumos.controls.clear()
    
    novo_nome = ft.AutoComplete(suggestions=sugestoes, width=200)
    nova_categoria = ft.Dropdown(
        label="categoria", 
        options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")]
    )

    nova_qtd = ft.TextField(label="QTD", width=80, on_change=validar_numeros)
    lista_referencias_insumos.append({
        "nome": novo_nome,
        "categoria": nova_categoria,
        "qtd": nova_qtd
    })
    coluna_insumos.controls.append(ft.Row([novo_nome, nova_categoria, nova_qtd]))
    
    if page:
        page.update()

        
# def responsavel pelos cadastros dos produtos
def salvar_produto(produto_dados):
    query = """
    INSERT INTO produtos (nome_produto, novo_insumo, nova_categoria, nova_qtd)
    VALUES (%s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                for insumo in produto_dados["insumos"]:
                    qtd_original = str(insumo["quantidade"]).strip()

                    cursor.execute(query, (
                        produto_dados["nome"],
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
    comando_sql_produtos = "SELECT DISTINCT nome_produto FROM produtos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql_produtos)
                resultados_produtos = cursor.fetchall()
                return [{"nome_produto": linha[0]} for linha in resultados_produtos]
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

# def que deleta o produto
def deletar_produto_por_nome(nome_produto):
    if not nome_produto:
        raise ValueError("Nenhum produto selecionado.")

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            sql_delete = "DELETE FROM produtos WHERE nome_produto = %s"
            cursor.execute(sql_delete, (nome_produto,))
            conexao.commit()


# def edita o produto
def salvar_produto_editado(produto_dados, nome_produto_antigo):
    
    query_buscar_codigo = "SELECT novo_codigo FROM produtos WHERE nome_produto = %s LIMIT 1;"
    query_delete = "DELETE FROM produtos WHERE nome_produto = %s;"
    
    
    query_insert = """
    INSERT INTO produtos (nome_produto, novo_codigo, novo_insumo, nova_categoria, nova_qtd)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query_buscar_codigo, (nome_produto_antigo,))
                resultado = cursor.fetchone()
            
                codigo_fixo = resultado[0] if resultado else 1
                
                cursor.execute(query_delete, (nome_produto_antigo,))
                
                for insumo in produto_dados["insumos"]:
                    cursor.execute(query_insert, (
                        produto_dados["nome"],         
                        codigo_fixo,                   
                        insumo["insumo_id"],           
                        insumo["categoria"],           
                        insumo["quantidade"]          
                    ))
        print('Produto atualizado com sucesso no banco!')
        return True
    except Exception as e:
        print(f"Erro ao editar no banco: {e}")
        raise e



# def que traz os detalhes dos insumos
def obter_detalhes_insumos(nome):

        query = """
            SELECT "uni_medi", "quantidade", "custo", "fornecedor", "telefone", "email", "comentario", "data_cadastro" 
            FROM insumos 
            WHERE "nome" = %s;
        """
        try:
            with obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(query, (nome,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar detalhes para {nome}: {e}")
            return None

# def que exclui os insumos
def deletar_insumo_por_nome(nome):
    if not nome:
        raise ValueError("Nenhum produto selecionado.")

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            sql_delete = "DELETE FROM insumos WHERE nome = %s"
            cursor.execute(sql_delete, (nome,))
            conexao.commit()

# def que salva alteraçoes dos insumos
def salvar_alteracoes_insumo(e, 
                            txt_buscar_insumo, 
                            nome_selecionado_insumo, 
                            lbl_status, 
                            txt_uni_medi,
                            txt_qtd,
                            txt_fornecedor,
                            txt_telefone,
                            txt_email,
                            txt_comentario,
                            txt_custo
                            ):
    page = e.page
   

    nome_insumo = nome_selecionado_insumo if nome_selecionado_insumo else (txt_buscar_insumo.value.strip() if txt_buscar_insumo.value else "")

    if not nome_insumo:
        lbl_status.value = "Nenhum insumo selecionado para alteração!"
        lbl_status.color = ft.Colors.RED
        page.update()
        return

    try:
        conn = obter_conexao()
        cursor = conn.cursor() 
        
        cursor.execute("SELECT id FROM insumos WHERE nome = %s", (nome_insumo,))
        insumo = cursor.fetchone()

        if not insumo:
            lbl_status.value = f"O insumo '{nome_insumo}' não foi encontrado no banco!"
            lbl_status.color = ft.Colors.RED
            cursor.close()
            conn.close()
            page.update()
            return

        insumo_id = insumo[0]

        sql = """
            UPDATE insumos 
            SET uni_medi = %s, custo = %s, quantidade = %s, fornecedor = %s, 
                telefone = %s, email = %s, comentario = %s
            WHERE id = %s
        """
        
        valores = (
            txt_uni_medi.value, 
            float(txt_custo.value.replace(",", ".") if txt_custo.value else 0), 
            float(txt_qtd.value if txt_qtd.value else 0), 
            txt_fornecedor.value,
            txt_telefone.value, 
            txt_email.value, 
            txt_comentario.value,
            insumo_id 
        )
        
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()

        lbl_status.value = ft.Text("Insumo atualizado!")
        lbl_status.color = ft.Colors.GREEN
        
    except Exception as erro:
        print('{erro}')
        lbl_status.value = f"Preencha os campos: medida, custo e quantidade"
        lbl_status.color = ft.Colors.RED
    
    page.update()


# def que realiza a lista de compras 
def obter_custo_medio_insumo(nome_insumo):
    conn = obter_conexao()
    cursor = conn.cursor()
    try:
        query = """
            SELECT ROUND(AVG(h.custo_novo), 2) AS custo_medio_historico
            FROM insumos i
            JOIN historico_custos_insumos h ON i.id = h.insumo_id
            WHERE i.nome = %s
            GROUP BY i.id, i.nome;
        """
        cursor.execute(query, (nome_insumo,))
        resultado = cursor.fetchone()
        
        # Se achar o insumo, retorna a média, se não, retorna 0.0
        return float(resultado[0]) if resultado else 0.0
    except Exception as e:
        print(f"Erro ao buscar custo médio: {e}")
        return 0.0
    finally:
        cursor.close()
        conn.close()

# def que busca o preço dos insumos para o calculo de estoque

def obter_preco_insumos():
    # Adicionado o campo preco_unitario na consulta SQL
    comando_sql = "SELECT id, nome, preco_unitario, quantidade  FROM insumos;"
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(comando_sql)
                resultados = cursor.fetchall()
               
                # Mapeia a linha[2] para a chave "preco_unitario"
                return [
                    {
                        "id": linha[0], 
                        "nome": linha[1], 
                        "preco_unitario": linha[2],
                        "quantidade": linha[3]
                    } for linha in resultados
                ]
    except Exception as erro:
        print(f"Erro ao buscar insumos: {erro}")
        return []
