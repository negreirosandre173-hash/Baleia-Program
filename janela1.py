import flet as ft
from database import salvar_no_banco


#===============================================================

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
        e.control.update()

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

#======================================================= 


txt_nome = ft.TextField( hint_text="Ex: Açúcar", width=320)

txt_codigo= ft.TextField( hint_text="Ex: 12", width=225, on_change=validar_numeros)

txt_uni_medi= ft.Dropdown(   
                            options=[
                                    ft.dropdown.Option("KG"),
                                    ft.dropdown.Option("UNID"),
                                    ft.dropdown.Option("ML")
                                     ]
                            )
txt_custo= ft.TextField(hint_text="Ex: 12,99", width=205, on_change=on_change_custo)

txt_data=  ft.TextField(
                            hint_text="DD/MM/AAAA",
                            width=205,
                            keyboard_type=ft.KeyboardType.NUMBER,
                            on_change=on_change_data)

txt_fornecedor=ft.TextField(hint_text="Ex: BaleiaLtda",width=180)

txt_telefone= ft.TextField(hint_text="(61) 9 9999-9999 ", width=180, on_change=on_change_telefone)

txt_email=ft.TextField(hint_text="Ex: BaleiaPrograma173@gmail.com:", width=180)

txt_comentario=ft.TextField(hint_text="Ex: Produto comprado com desconto", width=350)

#==========================================================================================

lbl_status = ft.Text(value="", color=ft.Colors.GREEN)

def enviar_clicado(e):

        page = e.page

        nome = txt_nome.value.upper() if txt_nome.value else ""
        codigo = txt_codigo.value
        uni_medi= txt_uni_medi.value
        custo = txt_custo.value
        data_cadastro= txt_data.value
        fornecedor = txt_fornecedor.value
        telefone = txt_telefone.value
        email = txt_email.value
        comentario = txt_comentario.value


        
        if not nome or not codigo or not uni_medi or not custo or not data_cadastro:
            lbl_status.value = "Preencha os campos obrigatórios!"
            lbl_status.color = ft.Colors.RED
            page.update()
            return

        try:
            custo_limpo = custo.replace(".","").replace(",", ".")
            custo_float = float(custo_limpo)
            codigo_int = int(codigo)


            salvar_no_banco(nome, codigo_int, uni_medi, custo_float, data_cadastro, fornecedor, telefone, email, comentario)
            lbl_status.value = "Insumo cadastrado!"
            lbl_status.color = ft.Colors.GREEN
            
            
            txt_nome.value = ""
            txt_codigo.value = ""
            txt_uni_medi.value = None
            txt_custo.value = ""
            txt_data.value = ""
            txt_fornecedor.value = ""
            txt_telefone.value = ""
            txt_email.value = ""
            txt_comentario.value = ""


        except Exception as erro:
            lbl_status.value = f"Erro ao salvar: {erro}"
            lbl_status.color = ft.Colors.RED

        page.update()

#=================================================================================================

def janel1 (page: ft.Page, voltar):
     return ft.Container( 
        ft.Stack(
           controls=[
              ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
              ft.Container(
                height=600,
                width=600,
                padding=20,
                bgcolor="white",
                top= 60,
                left=400,
                border_radius=10,
                shadow=ft.BoxShadow(
                     spread_radius=1,blur_radius=10,color=ft.Colors.BLACK,
                     offset=ft.Offset(0,1),),
                     content= ft.Column(
                            scroll=ft.ScrollMode.ALWAYS,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(""),
                                        ft.Text("Cadastro de Insumo", size=35,)
                                    ], spacing = 50
                                ),
                                ft.Divider(height=10, thickness=1,color=ft.Colors.BLUE,),
                                ft.Row(
                                    controls=[
                                        ft.Text("Nome:",weight=ft.FontWeight.BOLD),
                                        ft.Text("Código:", weight=ft.FontWeight.BOLD,),
                                    ], spacing=50
                                ),
                                ft.Row(
                                    controls=[
                                        txt_nome,
                                        txt_codigo,   
                                    ], 
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Medida:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("Custo:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("Data:",weight=ft.FontWeight.BOLD),
                                    ], spacing=70
                                ),
                                ft.Row(
                                    controls=[
                                        txt_uni_medi,
                                        txt_custo,
                                        txt_data                                 
                                    ],
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Fornecedor:", weight=ft.FontWeight.BOLD, ),
                                        ft.Text("Telefone:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("E-Mail:",weight=ft.FontWeight.BOLD, )
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        txt_fornecedor,
                                        txt_telefone,
                                        txt_email,
                                    ]
                                ),
                                ft.Row(
                                    controls=[      
                                         ft.Text(""),                                  
                                         ft.Text("Comentário:", weight=ft.FontWeight.BOLD)
                                ], spacing=180),
                                ft.Row(
                                    controls=[
                                        
                                        ft.Text(""),
                                        txt_comentario,           
                                 ], spacing= 100
                                ),
                                lbl_status,
                                ft.Container(
                                  content=ft.Row(
                                     controls=[
                                        ft.ElevatedButton("Cancelar", on_click=voltar),
                                        ft.FilledButton("Salvar", on_click=enviar_clicado)
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






