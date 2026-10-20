import flet as ft 
from cadastrar_insumo import cadastrar_insumo 
from buscar_insumo import buscar_insumo
from editar_insumo import editar_insumo
from cadastrar_produto import cadastrar_produto
from buscar_produto import buscar_produto
from editar_produto import cadastrar_produto_editado
from calcular_estoque_compra import calcular_estoque_compra
from lista_de_compras import lista_de_compras

def main(page: ft.Page): 
    page.padding = 0 
    page.window_full_screen = True 
    
    azul = "#1E3A8A" 
    azul_claro = "#E7F0F7" 
    
    def clicar(e): 
        print("clicado") 
        
    def janela_cadastrar_insumo(e): 
        conteudo_vendas = cadastrar_insumo(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()
    
    def janela_buscar_insumo(e): 
        conteudo_vendas = buscar_insumo(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()

    def janela_editar_insumo(e): 
        conteudo_vendas = editar_insumo(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()
    
    def janela_cadastrar_produto(e): 
        conteudo_vendas = cadastrar_produto(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()
    
    def janela_buscar_produto(e): 
        conteudo_vendas = buscar_produto(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()

    def janela_editar_produto(e): 
        conteudo_vendas = cadastrar_produto_editado(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()

    def janela_calcular_estoque(e): 
        conteudo_vendas = calcular_estoque_compra(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()

    def janela_lista_de_compras(e): 
        conteudo_vendas = lista_de_compras(page) 
        
        conteudo_principal.content = conteudo_vendas
        conteudo_principal.update()



    conteudo_principal = ft.Container( 
        expand=True, 
        height=800, 
        bgcolor=azul_claro, 
        content=ft.Text("Bem-vindo ao sistema", size=24, color=azul) 
    )

    grid = ft.Row( 
        controls=[ 
            ft.Container( 
                bgcolor=azul, 
                width=330, 
                padding=20, 
                margin=0, 
                height=800, 
                content=ft.Column( 
                    controls=[ 
                        ft.Row( 
                            controls=[ 
                                ft.Image(src="baleialogo.png", width=100, margin=0), 
                                ft.Column( 
                                    controls=[ 
                                        ft.Text("Baleia", size=30, color="white"), 
                                        ft.Text("Gestao de Estoques", size=15, color="white") 
                                    ], 
                                    spacing=0, 
                                ) 
                            ] 
                        ), 
                        ft.Container(width=200, height=30), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_cadastrar_insumo, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Cadastrar Insumo", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_buscar_insumo, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.SEARCH, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Buscar Insumo", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_editar_insumo, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.EDIT, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Editar Insumo", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_cadastrar_produto, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.ADD_BUSINESS_OUTLINED, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Cadastrar Produto", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_buscar_produto, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.CONTENT_PASTE_SEARCH, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Buscar Produto", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_editar_produto, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.EDIT_SQUARE, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Editar Produto", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_calcular_estoque, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.GRAPHIC_EQ, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Simular Estoque", size=20, color="white") 
                            ])
                        ), 
                        ft.Container(
                            padding=10, border_radius=10, width=300, height=60, 
                            ink=True, on_click=janela_lista_de_compras, 
                            content=ft.Row(controls=[ 
                                ft.Icon(ft.Icons.ADD_SHOPPING_CART, color=ft.Colors.WHITE, size=25), 
                                ft.Text("Lista de Compras", size=20, color="white") 
                            ])
                        ), 
                        
                    ], 
                    margin=0, 
                    spacing=0
                ) 
            ), 
            conteudo_principal 
        ], 
        spacing=0
    ) 
    
    page.add(grid) 

ft.run(main) 
