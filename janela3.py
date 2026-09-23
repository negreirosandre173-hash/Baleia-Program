import flet as ft
from database import obter_conexao


txt_buscar_produto = None
resultado_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)


def obter_todos_produtos():
    query = 'SELECT DISTINCT "Produto" FROM vw_relatorio_custos ORDER BY "Produto";'
    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                # CORREÇÃO: produto[0] extrai a string de dentro da tupla retornada pelo Postgres
                return [produto[0] for produto in cursor.fetchall()]
    except Exception as e:
        print(f"Erro ao buscar produtos para o autocomplete: {e}")
        return []



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




def janel3(page: ft.Page, voltar):
    global txt_buscar_produto

    dados_produtos = obter_todos_produtos()
    
    # Como dados_produtos agora é uma lista de strings, passamos a variável direto
    sugestoes_autocomplete = [
        ft.AutoCompleteSuggestion(key=produto, value=produto) for produto in dados_produtos
    ]

    def realizar_busca(e):
        if hasattr(e, "selection") and e.selection:
            nome_selecionado = e.selection.value if hasattr(e.selection, "value") else str(e.selection)
        else:
            nome_selecionado = txt_buscar_produto.value
        
        nome_selecionado = str(nome_selecionado).strip()
        
        if not nome_selecionado:
            resultado_container.controls = [ft.Text(" Selecione ou digite o nome do produto.", color="red")]
            page.update()
            return
            
        # Executa a nova query passando diretamente o nome selecionado
        linhas_receita = obter_detalhes_receita_view(nome_selecionado)
        
        if linhas_receita is None:
            resultado_container.controls = [
                ft.Text(" Erro interno ao calcular no banco de dados.", color="red", weight="bold")
            ]
            page.update()
            return
            
        if len(linhas_receita) == 0:
            resultado_container.controls = [
                ft.Text(f" Produto '{nome_selecionado}' não localizado no catálogo.", color="orange")
            ]
            page.update()
            return

        # Prepara a lista de componentes visuais na tela
        componentes_resultado = [
            ft.Divider(height=10, thickness=1, color=ft.Colors.GREY_300),
            ft.Text(f" Produto:  {nome_selecionado.upper()}", size=18, weight="bold", color="blue"),
            ft.Text(" Insumos Utilizados:", size=14, weight=ft.FontWeight.BOLD, color="blue"),
        ]
        
        # Vence as linhas retornadas pela View do Postgres
        for ingrediente, quantidade, unidade, custo in linhas_receita:
            if ingrediente == "TOTAL RECEITA:":
                componentes_resultado.insert(
                    2, # Injeta na segunda posição (logo abaixo do nome do produto) para manter o visual limpo
                    ft.Text(f"Custo Total: R$ {custo:.2f}", size=20, weight="bold", color="green")
                )
            else:
                
    # Cria uma linha organizada: ingrediente e quantidade na esquerda, custo na direita
                componentes_resultado.append(
                ft.Container(
                 padding=ft.padding.only(left=15, right=10),
                 content=ft.Row(
                  controls=[
                    # Bloco da Esquerda: Ingrediente e Medida
                    ft.Text(
                        f"• {ingrediente}: {quantidade} {unidade}", 
                        size=14, 
                        color="black",
                        weight=ft.FontWeight.W_500, 
                        
                    ),
        
                    # Bloco da Direita: Custo alinhado perfeitamente
                    ft.Text(
                        f"Custo: R$ {custo:.2f}", 
                        size=14, 
                        color="black",
                        weight=ft.FontWeight.W_500,
                        
                        
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                
            )
        )
    )

        
        resultado_container.controls = componentes_resultado
        page.update()

    
    txt_buscar_produto = ft.AutoComplete(
        suggestions=sugestoes_autocomplete,
        on_select=realizar_busca
    )

    return ft.Container(
        ft.Stack(
            controls=[
                ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
                ft.Container(
                    padding=20,
                    width=600,
                    height=600, 
                    bgcolor="white",
                    top=50,
                    left=455,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=10, color=ft.Colors.BLACK,
                        offset=ft.Offset(0, 1),          
                    ), 
                    content=ft.Column(
                        controls=[
                            ft.Text("Buscar Produto", size=35, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=10, thickness=1, color=ft.Colors.BLUE),
                            ft.Text("Nome do Produto", size=20, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Container(content=txt_buscar_produto, width=300),
                                    ft.ElevatedButton("Buscar", on_click=realizar_busca)
                                ]
                            ),
                            ft.Container(content=resultado_container, expand=True),
                            ft.Divider(color=ft.Colors.WHITE, height=5),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("Cancelar", on_click=voltar)
                                ], 
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    )         
                ),
            ]
        )
    )
