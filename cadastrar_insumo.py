import flet as ft
from database import salvar_no_banco
from database import enviar_clicado


#=========================================================================================================

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


txt_nome = ft.TextField( hint_text="Ex: Açúcar", width=430)

txt_uni_medi= ft.Dropdown(   
                            options=[
                                    ft.dropdown.Option("KG"),
                                    ft.dropdown.Option("UNID"),
                                    ft.dropdown.Option("ML")
                                     ], width=430
                            )
txt_custo= ft.TextField(hint_text="Ex: 12,99", width=430, on_change=on_change_custo)

txt_qtd = ft.TextField(label="QTD", width=430, on_change=validar_numeros)

txt_fornecedor=ft.TextField(hint_text="Ex: BaleiaLtda",width=285)

txt_telefone= ft.TextField(hint_text="(61) 9 9999-9999 ", width=285, on_change=on_change_telefone)

txt_email=ft.TextField(hint_text="Ex: BaleiaPrograma173@gmail.com:", width=285)

txt_comentario=ft.TextField(hint_text="Ex: Produto comprado com desconto", width=700, )

lbl_status = ft.Text(value="", color=ft.Colors.GREEN)


btn_salvar = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=lambda e: enviar_clicado(  e,
                                        txt_nome,
                                        txt_uni_medi,
                                        txt_custo,
                                        txt_fornecedor,
                                        txt_telefone,
                                        txt_email,
                                        txt_comentario,
                                        txt_qtd,
                                        lbl_status),
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.SAVE, color="white"),
            ft.Text("Salvar", color="white")
        ]
    )
)
#==========================================================================================


def cadastrar_insumo (page: ft.Page):
     return ft.Container( 
        ft.Stack(
           controls=[
              ft.Container(
                height=640,
                width=960,
                padding=20,
                bgcolor="#FFFFFF",
                top= 20,
                left=40,
                border_radius=10,
                shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=3, color=ft.Colors.GREY,
                        offset=ft.Offset(1, 1),          
                    ),
                     content= ft.Column(
                            scroll=ft.ScrollMode.ALWAYS,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                        ft.Column(
                                            controls=[
                                                ft.Text("Cadastro de Insumo", size=28),
                                                ft.Text("Adicione um novo insumo ao seu estoque", size=13),
                                            ], spacing=0
                                        ),
                                    ], spacing = 20
                                ),
                                ft.Container(
                                    padding=20,
                                    bgcolor="#FFFFFF",
                                    border=ft.Border.all(width=1, color=ft.Colors.GREY),
                                    border_radius=8,
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                    controls=[
                                        ft.Text("Nome:",weight=ft.FontWeight.BOLD),
                                        ft.Text("Medida:",weight=ft.FontWeight.BOLD, ),
                                    ], spacing=400
                                ),
                                ft.Row(
                                    controls=[
                                        txt_nome,
                                        txt_uni_medi,
                                    ], 
                                ),
                                ft.Row(
                                    controls=[
                                        
                                        ft.Text("Custo:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("quantidade:",weight=ft.FontWeight.BOLD, ),
                                        
                                    ], spacing=400
                                ),
                                ft.Row(
                                    controls=[
                                        txt_custo,
                                        txt_qtd,
                                    ],
                                ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    padding=20,
                                    bgcolor="#FFFFFF",
                                    border=ft.Border.all(width=1, color=ft.Colors.GREY),
                                    border_radius=8,
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                    controls=[
                                        ft.Text("Fornecedor:", weight=ft.FontWeight.BOLD, ),
                                        ft.Text("Telefone:",weight=ft.FontWeight.BOLD, ),
                                        ft.Text("E-Mail:",weight=ft.FontWeight.BOLD, )
                                    ], spacing=220
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
                                ], spacing=410),
                                ft.Row(
                                    controls=[
                                        ft.Text(""),
                                        txt_comentario,           
                                 ], spacing= 100
                                ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                  content=ft.Row(
                                     controls=[
                                        lbl_status,
                                        btn_salvar
                                    ],                                     
                                      alignment=ft.CrossAxisAlignment.END
                                   ), padding=10
                                )                              
                            ], spacing=10                  
                        )                     
                    ),
                ]
            )
        )






