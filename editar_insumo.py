import flet as ft
from database import obter_conexao, obter_insumos, obter_detalhes_insumos, deletar_insumo_por_nome, salvar_alteracoes_insumo 
from cadastrar_insumo import on_change_telefone, validar_numeros, on_change_data, on_change_custo

nome_selecionado_insumo = ""
resultado_container = ft.Column()

dados_insumos = obter_insumos()
sugestoes_autocomplete_insumos = [
    ft.AutoCompleteSuggestion(key=nome["nome"], value=nome["nome"]) 
    for nome in dados_insumos
]

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
                ft.Text(f"SELECIONADO: {nome_selecionado_insumo.upper()}", size=16, weight="bold", color="green"),
            ], alignment=ft.MainAxisAlignment.CENTER
        ),
    ]
            
    resultado_container.controls = componentes_resultado
    page.update() 
    
txt_buscar_insumo = ft.AutoComplete(
    suggestions=sugestoes_autocomplete_insumos,
    width=400,
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
                    content=ft.Column(
                        controls=[
                            ft.Row(controls=[ft.Container(width=60), ft.Text("Editar Insumo", size=32, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row(controls=[txt_buscar_insumo], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row(controls=[ft.Container(width=60), (resultado_container)], alignment=ft.MainAxisAlignment.CENTER),
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

# ======================================================= 

txt_uni_medi = ft.Dropdown(   
    options=[
        ft.dropdown.Option("KG"),
        ft.dropdown.Option("UNID"),
        ft.dropdown.Option("ML")
    ], width=180
)
txt_custo = ft.TextField(hint_text="Ex: 12,99", width=180, on_change=on_change_custo)
txt_qtd = ft.TextField(label="QTD", width=180, on_change=validar_numeros)

txt_data = ft.TextField(
    hint_text="DD/MM/AAAA",
    width=180,
    keyboard_type=ft.KeyboardType.NUMBER,
    on_change=on_change_data
)

txt_fornecedor = ft.TextField(hint_text="Ex: BaleiaLtda", width=180)
txt_telefone = ft.TextField(hint_text="(61) 9 9999-9999 ", width=180, on_change=on_change_telefone)
txt_email = ft.TextField(hint_text="Ex: BaleiaPrograma173@gmail.com:", width=180)
txt_comentario = ft.TextField(hint_text="Ex: Produto comprado com desconto", width=360)

lbl_status = ft.Text(value="", color=ft.Colors.GREEN)

# ==========================================================================================

def editar_insumo(page: ft.Page):
    return ft.Container( 
        ft.Stack(
            controls=[
                ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
                ft.Container(
                    height=600,
                    width=600,
                    padding=20,
                    bgcolor="white",
                    top=60,
                    left=400,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=10, color=ft.Colors.BLACK,
                        offset=ft.Offset(0, 1),
                    ),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Row(controls=[buscar_insumo()], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row(
                                controls=[
                                    ft.Text("Medida:", weight=ft.FontWeight.BOLD),
                                    ft.Text("Custo:", weight=ft.FontWeight.BOLD),
                                    ft.Text("quantidade:", weight=ft.FontWeight.BOLD),
                                ], spacing=145
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
                                    ft.Text("E-Mail:", weight=ft.FontWeight.BOLD)
                                ], spacing=120
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
                                    ft.Text("Data:", weight=ft.FontWeight.BOLD)
                                ], spacing=260),
                            ft.Row(
                                controls=[
                                    ft.Text(""),
                                    txt_comentario,
                                    txt_data           
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            lbl_status,
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Button("Excluir", on_click=clicar_deletar),
                                        ft.Button("Cancelar"),
                                        ft.Button("Salvar", on_click=lambda e: salvar_alteracoes_insumo(
                                        e, 
                                        txt_buscar_insumo, 
                                        nome_selecionado_insumo, 
                                        lbl_status, 
                                        txt_uni_medi,
                                        txt_qtd,
                                        txt_data,
                                        txt_fornecedor,
                                        txt_telefone,
                                        txt_email,
                                        txt_comentario,
                                        txt_custo

                                        ))
                                    ],                                     
                                    alignment=ft.CrossAxisAlignment.END
                                ), padding=10
                            )                              
                        ], alignment=ft.MainAxisAlignment.CENTER                
                    )                     
                ),
            ]
        )
    )

