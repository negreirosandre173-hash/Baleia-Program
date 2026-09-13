import flet as ft



def on_change_telefone(e):
    value = e.control.value
    digits = "".join([c for c in value if c.isdigit()])
    digits = digits[:11]
    
    new_val = ""
    tam = len(digits)
    
    if tam <= 2:
        new_val = f"({digits}" if tam > 0 else ""
    elif tam <= 6:
        new_val = f"({digits[:2]}) {digits[2:]}"
    elif tam <= 10:
        new_val = f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    else:
        new_val = f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        
    e.control.value = new_val
    e.control.update()


def validar_numeros(e):
    
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()

def on_change_data(e):

        value = e.control.value
        
        digits = "".join([c for c in value if c.isdigit()])
        
       
        new_val = ""
        if len(digits) <= 2:
            new_val = digits
        elif len(digits) <= 4:
            new_val = f"{digits[:2]}/{digits[2:]}"
        else:
            new_val = f"{digits[:2]}/{digits[2:4]}/{digits[4:8]}"
        e.control.value = new_val

def on_change_custo(e):
    value = e.control.value
    
    digits = "".join([c for c in value if c.isdigit()])
    
    if not digits:
        e.control.value = ""
        e.control.update()
        return

    integer_value = int(digits)
    float_value = integer_value / 100
    new_val = f"{float_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    if value != new_val:
        e.control.value = new_val
        e.control.update()

        

def janel1 (page: ft.Page, voltar):
     return ft.Container( 
        ft.Stack(
           controls=[
              ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
              ft.Container(
                height=630,
                width=450,
                padding=20,
                bgcolor="white",
                top= 60,
                left=455,
                border_radius=10,
                shadow=ft.BoxShadow(
                     spread_radius=1,blur_radius=10,color=ft.Colors.BLACK,
                     offset=ft.Offset(0,1),),
                     content= ft.Column(
                            scroll=ft.ScrollMode.ALWAYS,
                            controls=[
                                ft.Text("Cadastro de Isumo", size=35,),
                                ft.Divider(height=10, thickness=1,color=ft.Colors.BLUE,),
                                ft.Text("Informações Básicas:", size=20, weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    controls=[
                                        ft.Text("Nome:",weight=ft.FontWeight.BOLD),
                                        ft.Text("Código:", weight=ft.FontWeight.BOLD,),
                                    ], spacing=265
                                ),
                                ft.Row(
                                    controls=[
                                        ft.TextField( hint_text="Ex:Açúcar"),
                                        ft.TextField( hint_text="Ex:123", width=90, on_change=validar_numeros),
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Quantidade:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("Custo:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("Data:",weight=ft.FontWeight.BOLD),


                                    ], spacing=60
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Dropdown(   
                                         options=[
                                         ft.dropdown.Option("KG"),
                                         ft.dropdown.Option("UNID"),
                                         ft.dropdown.Option("ML")
                                         ]
                                        ),
                                        ft.TextField(hint_text="Ex:12,99", width=100, on_change=on_change_custo),
                                        ft.TextField(
                                              hint_text="DD/MM/AAAA",
                                              width=150,
                                              keyboard_type=ft.KeyboardType.NUMBER,
                                              on_change=on_change_data)                                 
                                    ],
                                ),
                                ft.Divider(height=10, thickness=1,color=ft.Colors.BLUE,),
                                ft.Text("Informações Adicionais:",weight=ft.FontWeight.BOLD, size=20),
                                ft.Text("Fornecedor:",weight=ft.FontWeight.BOLD, ),
                                ft.TextField(hint_text="Ex: BaleiaLtda",width=400),

                                ft.Row(
                                    controls=[                                        
                                        ft.Text("Telefone:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("E-Mail:",weight=ft.FontWeight.BOLD, )

                                ], spacing=95),
                                ft.Row(
                                    controls=[
                                        
                                        ft.TextField(hint_text="(xx) xxxxx-xxxx", width=150, on_change=on_change_telefone),
                                        ft.TextField(hint_text="Ex: BaleiaPrograma173@gmail.com:", width=240)
                                 ]
                                ),
                                ft.Text("Comentário:",weight=ft.FontWeight.BOLD),
                                ft.TextField(hint_text="Ex:Produto comprado com desconto", width=400),
                                ft.Container(
                                  content=ft.Row(
                                     controls=[
                                        ft.ElevatedButton("Cancelar", on_click=voltar),
                                        ft.FilledButton("Salvar")
                                    ],                                     
                                      alignment=ft.CrossAxisAlignment.END
                                   ), padding=10
                                )                              
                            ]                  
                        )                     
                    ),
                ]
            )
        )






