import flet as ft
from janela1 import janel1
from janela2 import janel2
from janela3 import janel3
from janela4 import janel4

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
                    on_click=abrir_vendas1,
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
                    on_click=abrir_vendas2,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=510,  
                    top=10, 
                ),
                #cadastrar insumo
                ft.Container(
                    content=ft.Image(src="a1.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=abrir_vendas,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=720,  
                    top=10, 
                ),
                #buscar insumo
                ft.Container(
                    content=ft.Image(src="c1.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=abrir_vendas3,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=930,  
                    top=10, 
                ),
                #lista de compras
                ft.Container(
                    content=ft.Image(src="listvendas.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=on_btn1_click,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK),
                    left=300,  
                    top=220, 
                ),
                #fornecedores
                ft.Container(
                    content=ft.Image(src="forne.jpeg", width=150, height=150),
                    padding=13,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    on_click=on_btn1_click,
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
    def abrir_vendas(e):
        page.clean()
        conteudo_vendas = janel1(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
    #cadastro de produto
    def abrir_vendas1(e):
        page.clean()
        conteudo_vendas = janel2(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
    #buscar produto
    def abrir_vendas2(e):
        page.clean()
        conteudo_vendas = janel3(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()
    #buscar insumo
    def abrir_vendas3(e):
        page.clean()
        conteudo_vendas = janel4(page, layout_principal)
        page.add(conteudo_vendas)
        page.update()

    
     
    layout_principal()
    
    

ft.app(target=main)
