import flet as ft
from cadastrar_insumo import cadastrar_insumo
from cadastrar_produto import cadastrar_produto
from buscar_produto import buscar_produto
from editar_produto import cadastrar_produto_editado
from buscar_insumo import buscar_insumo




def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.window_full_screen = True

    def on_btn1_click(e):
        page.clean()
        page.add(janel1())
        page.update()
 
    def layout_principal(e=None):
      page.clean()
      page.add(
      ft.Container(
        content=ft.Stack(
            controls=[
              
                ft.Image(src="fundooriginal.jpg", width=1600, height=790,),
                #cadastrar produto
                ft.Container(
                    content=ft.Image(src="a2.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=janela_cadastrar_produto,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=300,  
                    top=10, 
                ),
                #buscar produto
                ft.Container(
                    content=ft.Image(src="a3.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=janela_buscar_produto,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=510,  
                    top=10, 
                ),
                #cadastrar insumo
                ft.Container(
                    content=ft.Image(src="cadastrarinsumo.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=janela_cadastrar_insumo,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=930,  
                    top=10, 
                ),
                #buscar insumo
                ft.Container(
                    content=ft.Image(src="c1.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=janela_buscar_insumo,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=300,  
                    top=220, 
                ),
                #editar produto
                ft.Container(
                    content=ft.Image(src="editarproduto.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=janela_editar_prooduto,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=720,  
                    top=10, 
                ),
                ft.Container(
                    content=ft.Image(src="editarinsumo.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=janela_editar_insumo,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=510,  
                    top=220, 
                ),
                
                #sair
                ft.Container(
                    content=ft.Image(src="sair.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=on_btn1_click,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=1150,  
                    top=520, 
                ),              
            
            ]
        )
    )
 )
   
      page.update()

    #cadastro de insumo
    def janela_cadastrar_insumo(e):
        page.clean()
        conteudo_vendas =cadastrar_insumo(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
    #cadastro de produto
    def janela_cadastrar_produto(e):
        page.clean()
        conteudo_vendas = cadastrar_produto(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
    #buscar produto
    def janela_buscar_produto(e):
        page.clean()
        conteudo_vendas = buscar_produto(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
        
    #editar produto
    def janela_editar_prooduto():
        page.clean()
        conteudo_vendas = cadastrar_produto_editado(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()

    def janela_buscar_insumo():
        page.clean()
        conteudo_vendas = buscar_insumo(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()

    def janela_editar_insumo():
        page.clean()
        conteudo_vendas = cadastrar_insumo(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
    
     
    layout_principal()
    
    

ft.run(main)
