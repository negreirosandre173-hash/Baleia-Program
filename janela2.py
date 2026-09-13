import flet as ft


coluna_insumos = ft.Column()

def validar_numeros(e):
    
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()


def adicionar_campo(e):
        nova_linha = ft.Row([
            ft.TextField(label="Insumo", width=200),
            ft.Dropdown(
                 label="categoria",
                  options=[
                  ft.dropdown.Option("KG"),
                  ft.dropdown.Option("UND"),
                  ft.dropdown.Option("ML")
      ] 
                 ),
            ft.TextField(label="Qtd", width=80, on_change=validar_numeros),
        ])

        coluna_insumos.controls.append(nova_linha)

    
def janel2(page: ft.Page, voltar):
 return ft.Container(
        ft.Stack(
            controls=[
                
                ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
                
                ft.Container(
                    width=550,
                    height=600, 
                    bgcolor="white",
                    padding=20,
                    border_radius=10,
                    top= 30,
                    left=400,
                    shadow=ft.BoxShadow(
                      spread_radius=1,blur_radius=10,color=ft.Colors.BLACK,
                      offset=ft.Offset(0,1),),
                    content= ft.Column(
                         scroll=ft.ScrollMode.ALWAYS,
                         controls=[
                              ft.Text("Cadastro de Produto", size=35, weight=ft.FontWeight.BOLD,),
                              ft.Divider(height=10, thickness=1,color=ft.Colors.BLUE),
                              ft.Text("Informações Básicas", weight=ft.FontWeight.BOLD),
                              ft.Row(
                                   controls=[
                                   ft.TextField(label="Nome:", hint_text="Ex: Cosmopolitan", width=320),
                                   ft.TextField(label="Código", hint_text="Ex: 123...", width=120, on_change=validar_numeros)
                                   ]),
                              ft.Text("Insumos:"),
                              coluna_insumos, 
                              ft.ElevatedButton("Adicionar Insumo", on_click=adicionar_campo),
                              ft.Divider(),
                              ft.Container(
                                   ft.Row(
                                        controls=[
                                        ft.ElevatedButton("Cancelar", on_click=voltar
                                        ),
                                        ft.FilledButton("Salvar")
                                         ], 
                                         alignment=ft.CrossAxisAlignment.END,
                                        ),
                                   )
                             ]
                            )
                           ), 
                         ], 
                       )
                     )
