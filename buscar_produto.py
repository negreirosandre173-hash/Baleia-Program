import flet as ft
from database import obter_detalhes_receita_view, obter_todos_produtos

txt_buscar_produto = None
resultado_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

def buscar_produto(page: ft.Page):
    global txt_buscar_produto

    dados_produtos = obter_todos_produtos()
    
    sugestoes_autocomplete = [
        ft.AutoCompleteSuggestion(key=produto["nome_produto"], value=produto["nome_produto"]) for produto in dados_produtos
    ]

    def realizar_busca(e):
        if hasattr(e, "selection") and e.selection:
            nome_selecionado = e.selection.value if hasattr(e.selection, "value") else str(e.selection)
        else:
            nome_selecionado = txt_buscar_produto.value
        
        nome_selecionado = str(nome_selecionado).strip()
        
        if not nome_selecionado:
            resultado_container.controls = [ft.Text("Selecione ou digite o nome do produto.", color="red")]
            page.update()
            return
            
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

        componentes_resultado = [
            ft.Divider(height=10, thickness=1, color=ft.Colors.GREY_300),
            ft.Row(controls=[ft.Text(f"{nome_selecionado.upper()}", size=18, weight="bold", color="green",)],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[
                ft.Text("    "),
                ft.Text("Insumos:", size=14, weight=ft.FontWeight.BOLD, color="blue",),
                ft.Text("                      "),
                ft.Text(" qtd:", size=14, weight=ft.FontWeight.BOLD, color="blue"),
                ft.Text("     "),
                ft.Text(" unid:", size=14, weight=ft.FontWeight.BOLD, color="blue"),
                ft.Text("                 "),
                ft.Text(" preço:", size=14, weight=ft.FontWeight.BOLD, color="blue"),
            ], )
        ]
        
        for ingrediente, quantidade, unidade, custo in linhas_receita:
            if ingrediente == "TOTAL RECEITA:":
                componentes_resultado.insert(
                    2, 
                    ft.Text(f"Custo Total: R$ {custo:.2f}", size=20, weight="bold", color="green")
                )
            else:
                componentes_resultado.append(
                    ft.Container(
                        padding=ft.Padding(left=15, right=10, top=0, bottom=0),
                        content=ft.Row(
                            controls=[
                                ft.Container(ft.Text(f"• {ingrediente}", size=14, color="black", weight=ft.FontWeight.W_500), width=180),
                                ft.Container(ft.Text(f"{quantidade}", size=14, color="black", weight=ft.FontWeight.W_500), width=60),
                                ft.Container(ft.Text(f"{unidade}", size=14, color="black", weight=ft.FontWeight.W_500), width=120),
                                ft.Container(ft.Text(f"R$ {custo:.2f}", size=14, color="black", weight=ft.FontWeight.W_500), width=120)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
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
                                    ft.Button("Buscar", on_click=realizar_busca)
                                ]
                            ),
                            ft.Container(content=resultado_container, expand=True),
                            ft.Divider(color=ft.Colors.WHITE, height=5),
                            ft.Row(
                                controls=[
                                    ft.Button("Cancelar")
                                ], 
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    )         
                ),
            ]
        )
    )
