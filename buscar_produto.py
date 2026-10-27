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
            
            ft.Container(bgcolor="#1E3A8A",
                         width=900, 
                         height=50, 
                         border_radius=10,
                         content=ft.Row(controls=[ft.Text(f"{nome_selecionado.upper()}", size=18, color="white")],alignment=ft.MainAxisAlignment.CENTER),),
            ft.Container(
                width=900,
                height=40,
                border=ft.Border.all(width=1, color=ft.Colors.GREY),
                content=ft.Column(
                    controls=[
                        ft.Row(controls=[
                        ft.Text("INSUMOS:", size=14, weight=ft.FontWeight.BOLD, width=160),
                        ft.Text("QUANTIDADE:", size=14, weight=ft.FontWeight.BOLD, width=160),
                        ft.Text("UNI/MEDIDA:", size=14, weight=ft.FontWeight.BOLD, width=160),
                        ft.Text("PREÇO:", size=14, weight=ft.FontWeight.BOLD, width=160),
                                ], spacing=40,
                                   margin=0,
                                   alignment=ft.MainAxisAlignment.CENTER ),
                        
                        
                    ]
                ),
            ),
            
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
                            width=900,
                            height=40,
                            border=ft.Border.all(width=1, color=ft.Colors.GREY),
                            content=ft.Row(
                            controls=[
                                ft.Container(ft.Text(f"{ingrediente}", size=14, color="black", weight=ft.FontWeight.W_500), width=160),
                                ft.Container(ft.Text(f"{quantidade}", size=14, color="black", weight=ft.FontWeight.W_500), width=160),
                                ft.Container(ft.Text(f"{unidade}", size=14, color="black", weight=ft.FontWeight.W_500), width=160),
                                ft.Container(ft.Text(f"R$ {custo:.2f}", size=14, color="green", weight=ft.FontWeight.W_500), width=160)
                            ],spacing=40,
                            margin=0,
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    )
                )

        resultado_container.controls = componentes_resultado
        page.update()

    txt_buscar_produto = ft.AutoComplete(
        suggestions=sugestoes_autocomplete,
        on_select=realizar_busca,
        width=760,
    )

    return ft.Container(
        ft.Stack(
            controls=[
                ft.Container(
                    padding=20,
                    width=960,
                    height=640, 
                    bgcolor="white",
                    top=20,
                    left=40,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=3, color=ft.Colors.GREY,
                        offset=ft.Offset(1, 1),          
                    ), 
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                    ft.Text("Buscar Produto", size=28),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(border=ft.Border.all(width=1, color=ft.Colors.GREY),
                                    border_radius=8,
                                    width=900,
                                    height=60,
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE, size=25, margin=10),
                                            txt_buscar_produto
                                        ],spacing=80
                                    )),
                                ]
                            ),
                            ft.Container(content=resultado_container, expand=True),
                                 
                        ]
                    )         
                ),
            ]
        )
    )
