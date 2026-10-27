import flet as ft
from cadastrar_insumo import on_change_custo
from database import obter_insumos, salvar_produto, salvar_dados


lista_referencias_insumos = []
coluna_insumos = ft.Column()
dados_banco = obter_insumos()
sugestoes = [ft.AutoCompleteSuggestion(key=item["nome"], value=item["nome"]) for item in dados_banco]


def validar_numeros(e):
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()

nome_produto = ft.TextField(hint_text="Ex: Cosmopolitan", width=920)


def adicionar_campo(e):
    novo_insumo = ft.AutoComplete(suggestions=sugestoes, width=300)
    nova_categoria = ft.Dropdown(
        width=300,
        label="categoria", 
        options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")],
        value=None
    )
    nova_qtd = ft.TextField(hint_text="Ex: 1000", width=300, on_change=validar_numeros)
    
    nova_linha = ft.Row([novo_insumo, nova_categoria, nova_qtd])

    lista_referencias_insumos.append({
        "nome": novo_insumo,
        "categoria": nova_categoria,
        "qtd": nova_qtd
    })
    
    coluna_insumos.controls.append(nova_linha)

    if coluna_insumos.page:
        coluna_insumos.update() 



btn_salvar = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=lambda e: salvar_dados(e, nome_produto,
                                        lista_referencias_insumos,
                                        coluna_insumos,
                                        sugestoes,
                                        validar_numeros,
                                        dados_banco),
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.SAVE, color="white"),
            ft.Text("Salvar", color="white")
        ]
    )
)

btn_adiconar_insumo = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=adicionar_campo,
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.ADD, color="white"),
            ft.Text("Adicionar Insumo", color="white")
        ]
    )
)

def cadastrar_produto(page: ft.Page):

    if not coluna_insumos.controls:
        novo_nome = ft.AutoComplete(suggestions=sugestoes, width=300)
        nova_categoria = ft.Dropdown(
            width=300,
            label="categoria", 
            options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")]
        )
        nova_qtd = ft.TextField(hint_text="Ex: 1000", width=300, on_change=validar_numeros)
        
        lista_referencias_insumos.append({
            "nome": novo_nome,
            "categoria": nova_categoria,
            "qtd": nova_qtd
        })
        coluna_insumos.controls = [ft.Row([novo_nome, nova_categoria, nova_qtd])]

    return ft.Container(
        ft.Stack(
            controls=[
                ft.Container(
                    height=640,
                    width=960, 
                    bgcolor="white", 
                    padding=20, 
                    border_radius=10, top=20, left=40,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.GREY, offset=ft.Offset(0,1)),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                    ft.Text("Cadastro de Produto", size=28),
                                ]
                            ),
                            ft.Divider(),
                            ft.Column(controls=[
                                ft.Text("Nome:", weight=ft.FontWeight.BOLD, ),
                                nome_produto]),
                            ft.Row(
                                controls=[
                                    ft.Text("Insumos:", weight=ft.FontWeight.BOLD, width=300),
                                    ft.Text("Unidade:", weight=ft.FontWeight.BOLD,width=300),
                                    ft.Text("Quantidade:", weight=ft.FontWeight.BOLD,width=300)
                                ]
                            ),
                            coluna_insumos,
                            btn_adiconar_insumo,
                            ft.Divider(),
                            ft.Container(
                                ft.Row(
                                        controls=[
                                        btn_salvar
                                        ],
                                    alignment=ft.MainAxisAlignment.END, 
                                ),
                            )
                        ]
                    )
                ),
            ],
        )
    )
