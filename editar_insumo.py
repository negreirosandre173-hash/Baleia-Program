import flet as ft
from database import obter_conexao, obter_insumos, obter_detalhes_insumos, deletar_insumo_por_nome, salvar_alteracoes_insumo 
from cadastrar_insumo import on_change_telefone, validar_numeros, on_change_custo

nome_selecionado_insumo = ""
resultado_container = ft.Column()

dados_insumos = obter_insumos()
sugestoes_autocomplete_insumos = [
    ft.AutoCompleteSuggestion(key=nome["nome"], value=nome["nome"]) 
    for nome in dados_insumos
]

btn_salvar = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=lambda e: salvar_alteracoes_insumo(
                                        e, 
                                        txt_buscar_insumo, 
                                        nome_selecionado_insumo, 
                                        lbl_status, 
                                        txt_uni_medi,
                                        txt_qtd,
                                        txt_fornecedor,
                                        txt_telefone,
                                        txt_email,
                                        txt_comentario,
                                        txt_custo
                                        ),
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.SAVE, color="white"),
            ft.Text("Salvar", color="white")
        ]
    )
)


def realizar_busca_insumo(e):
    global nome_selecionado_insumo
    page = e.page 
        
    if e.control and e.control.value:
        nome_selecionado_insumo = e.control.value
    else:
        nome_selecionado_insumo = txt_buscar_insumo.value

    nome_selecionado_insumo = str(nome_selecionado_insumo).strip()

    if not nome_selecionado_insumo:
        resultado_container.controls = [ft.Text("Selecione ou digite o nome do produto.", color="red")]
        page.update()
        return

    componentes_resultado = [
        ft.Row(
            controls=[
                ft.Container(
                    width=920,
                    height=60,
                    border_radius=10,
                    bgcolor="#1E3A8A",
                        content=ft.Column(
                            controls=[
                                ft.Container(height=10),
                                ft.Row(
                                    controls=[
                                        ft.Text(f"SELECIONADO: {nome_selecionado_insumo.upper()}", size=16, color="white",),
                                            ], alignment=ft.MainAxisAlignment.CENTER
                                        )
                                    ]
                                )
                            ),
                        ], margin=0
                    )
                ]
            
    resultado_container.controls = componentes_resultado
    page.update() 
    
txt_buscar_insumo = ft.AutoComplete(
    suggestions=sugestoes_autocomplete_insumos,
    width=620,
    on_select=realizar_busca_insumo 
)

def verificar_erros_busca(linhas, nome):
    if linhas is None:
        return ft.Text("Erro interno ao buscar no banco de dados.", color="red", weight="bold")
    if len(linhas) == 0:
        return ft.Text(f"Nome '{nome}' não localizado no catálogo.", color="orange")
    return None

def buscar_insumo():
    return ft.Container(
        ft.Stack(
            controls=[
                ft.Container(
                    padding=0,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                        ft.Column(
                                            
                                            controls=[
                                                ft.Text("Editar Insumo", size=28),
                                                ft.Text("Mantenha seu estoque sempre atualizado!", size=13),
                                            ], spacing=0, alignment=ft.MainAxisAlignment.START
                                        ),
                                    ], spacing = 20
                                ),
                            ft.Row(controls=[
                            ft.Container(
                                    width=920,
                                    height=60,
                                    border_radius=10,
                                    border=ft.Border.all(width=1, color=ft.Colors.GREY),
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE, size=25, margin=10),
                                            ft.Row(controls=[txt_buscar_insumo], alignment=ft.MainAxisAlignment.CENTER),
                                                ], spacing=80
                                            )
                                        ),
                                        ]
                                    ),
                            ft.Container(height=10),
                            ft.Row(controls=[(resultado_container)], alignment=ft.MainAxisAlignment.CENTER),
                        ],
                    ),
                )   
            ]
        )
    )

def clicar_deletar(e):
    global nome_selecionado_insumo
    page = e.page 
 
    nome_para_deletar = nome_selecionado_insumo if nome_selecionado_insumo else (txt_buscar_insumo.value.strip() if txt_buscar_insumo.value else "")

    if not nome_para_deletar:
        resultado_container.controls = [
            ft.Row(controls=[ft.Text("Busque e selecione um insumo antes de excluir!", color="orange")], alignment=ft.MainAxisAlignment.CENTER)
        ]
        page.update()
        return

    try:
        deletar_insumo_por_nome(nome_para_deletar)
        resultado_container.controls = [
            ft.Row(
                controls=[
                    ft.Text(f"Insumo'{nome_para_deletar}' deletado com sucesso!", color="green", weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER,
            )
        ]

        txt_buscar_insumo.value = ""
        nome_selecionado_insumo = ""
        
    except Exception as erro:
        resultado_container.controls = [
            ft.Row(
                controls=[ft.Text(f"Erro ao deletar: {erro}", color="red")],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    page.update()


btn_excluir = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click= clicar_deletar,
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.DELETE, color="white"),
            ft.Text("Deletar", color="white")
        ]
    )
)

# ======================================================= 

txt_uni_medi = ft.Dropdown(   
    options=[
        ft.dropdown.Option("KG"),
        ft.dropdown.Option("UNID"),
        ft.dropdown.Option("ML")
    ], width=300
)
txt_custo = ft.TextField(hint_text="Ex: 12,99", width=300, on_change=on_change_custo)
txt_qtd = ft.TextField(label="QTD", width=300, on_change=validar_numeros)



txt_fornecedor = ft.TextField(hint_text="Ex: BaleiaLtda", width=300)
txt_telefone = ft.TextField(hint_text="(61) 9 9999-9999 ", width=300, on_change=on_change_telefone)
txt_email = ft.TextField(hint_text="Ex: BaleiaPrograma173@gmail.com:", width=300)
txt_comentario = ft.TextField(hint_text="Ex: Produto comprado com desconto", width=600)

lbl_status = ft.Text(value="", color=ft.Colors.GREEN)

# ==========================================================================================

def editar_insumo(page: ft.Page):
    return ft.Container( 
        ft.Stack(
            controls=[
                ft.Container(
                    height=630,
                    width=960,
                    padding=20,
                    bgcolor="white",
                    top=20,
                    left=40,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=3, color=ft.Colors.GREY,
                        offset=ft.Offset(1, 1),          
                    ),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Row(controls=[buscar_insumo()]),
                            ft.Row(
                                controls=[
                                    ft.Text("Medida:", weight=ft.FontWeight.BOLD),
                                    ft.Text(" Custo:", weight=ft.FontWeight.BOLD),
                                    ft.Text("  Quantidade:", weight=ft.FontWeight.BOLD),
                                ], spacing=250
                            ),
                            ft.Row(
                                controls=[
                                    txt_uni_medi,
                                    txt_custo,
                                    txt_qtd,                                    
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Fornecedor:", weight=ft.FontWeight.BOLD),
                                    ft.Text("Telefone:", weight=ft.FontWeight.BOLD),
                                    ft.Text("  E-Mail:", weight=ft.FontWeight.BOLD)
                                ], spacing=230
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
                                    ft.Text("Comentário:", weight=ft.FontWeight.BOLD),
                                ], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row(
                                controls=[
                                    txt_comentario,
                                ], alignment=ft.MainAxisAlignment.CENTER
                            ),
                            lbl_status,
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        btn_excluir,
                                        btn_salvar,
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

