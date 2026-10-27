import flet as ft
import math  
from database import obter_preco_insumos, obter_conexao

lista_referencias_insumos = []
coluna_insumos = ft.Column()
dados_banco = obter_preco_insumos()
sugestoes = [ft.AutoCompleteSuggestion(key=item["nome"], value=item["nome"]) for item in dados_banco]

def validar_numeros(e):
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()

def salvar_texto_autocomplete(e):
    if hasattr(e, "selection") and e.selection:
        e.control.value = e.selection.value
    e.control.update()

def calcular_totais(e):
    try:
        numero_multiplicador = float(qtd_produto.value) if qtd_produto.value else 0.0
    except ValueError:
        numero_multiplicador = 0.0

    try:
        semanal_multiplicador = float(semanal_produto.value) if semanal_produto.value else 0.0
    except ValueError:
        semanal_multiplicador = 0.0

    precos_insumos = {}
    quantidades_banco_insumos = {}
    
    for item in dados_banco:
        nome_db = item.get("nome") or item.get("NOME") or ""
        nome_db = str(nome_db).upper().strip()
        
        preco_db = item.get("preco_unitario") or item.get("PRECO_UNITARIO") or 0.0
        precos_insumos[nome_db] = float(preco_db)
        
        qtd_db = item.get("quantidade") or item.get("QUANTIDADE") or 1.0
        quantidades_banco_insumos[nome_db] = float(qtd_db) if float(qtd_db) > 0 else 1.0

    for item in lista_referencias_insumos:
        auto_comp = item["nome"]
        
        nome_selecionado = auto_comp.value if auto_comp.value else ""
        nome_selecionado = str(nome_selecionado).upper().strip()
        
        try:
            qtd_insumo = float(item["qtd"].value) if item["qtd"].value else 0.0
        except ValueError:
            qtd_insumo = 0.0

        volume_calculado = numero_multiplicador * semanal_multiplicador * qtd_insumo
        item["volume"].value = f"{volume_calculado:.2f}"

        preco_unitario = precos_insumos.get(nome_selecionado, 0.0)
        total_calculado = volume_calculado * preco_unitario
        item["total"].value = f"R$ {total_calculado:.2f}"

        quantidade_da_tabela = quantidades_banco_insumos.get(nome_selecionado, 1.0)
        resultado_divisao = volume_calculado / quantidade_da_tabela
        
        total_item_arredondado = math.ceil(resultado_divisao)
        item["total_item"].value = f"{total_item_arredondado}"

    coluna_insumos.update()


def adicionar_campo(e):
    novo_insumo = ft.AutoComplete(
        suggestions=sugestoes, 
        width=250,
        on_select=salvar_texto_autocomplete,
        on_change=salvar_texto_autocomplete,
        data=""
    )
    nova_qtd = ft.TextField(width=112, on_change=validar_numeros)
    novo_volume = ft.TextField(width=112, read_only=True, value="0.00")
    novo_total = ft.TextField(width=112, read_only=True, value="R$ 0.00")
    novo_total_item = ft.TextField(width=112, read_only=True, value="0")
    txt_uni_medi= ft.Dropdown(   
                            options=[
                                    ft.dropdown.Option("KG"),
                                    ft.dropdown.Option("UNID"),
                                    ft.dropdown.Option("ML")
                                     ], width=112
                            )
    
    nova_linha = ft.Row([novo_insumo, nova_qtd, txt_uni_medi, novo_volume, novo_total, novo_total_item], spacing=20) 
    
    lista_referencias_insumos.append({
        "nome": novo_insumo,
        "qtd": nova_qtd,
        "volume": novo_volume,
        "total": novo_total,
        "total_item": novo_total_item
    })
    coluna_insumos.controls.append(nova_linha)
    if coluna_insumos.page:
        coluna_insumos.update()

def novo_produto_clique(e):
    nome_produto.value = ""
    qtd_produto.value = ""
    semanal_produto.value = ""
    
    lista_referencias_insumos.clear()
    coluna_insumos.controls.clear()
    
    novo_nome = ft.AutoComplete(
        suggestions=sugestoes,
        width=255,
        on_select=salvar_texto_autocomplete,
        on_change=salvar_texto_autocomplete,
        data=""
    )

    txt_uni_medi= ft.Dropdown(   
                            options=[
                                    ft.dropdown.Option("KG"),
                                    ft.dropdown.Option("UNID"),
                                    ft.dropdown.Option("ML")
                                     ], width=112
                            )
    nova_qtd = ft.TextField(width=112, on_change=validar_numeros)
    novo_volume = ft.TextField(width=112, read_only=True, value="0.00")
    novo_total = ft.TextField(width=112, read_only=True, value="R$ 0.00")
    novo_total_item = ft.TextField(width=112, read_only=True, value="0")
    
    lista_referencias_insumos.append({
        "nome": novo_nome,
        "qtd": nova_qtd,
        "volume": novo_volume,
        "total": novo_total,
        "total_item": novo_total_item
    })
    coluna_insumos.controls = [ft.Row([novo_nome, nova_qtd, txt_uni_medi, novo_volume, novo_total, novo_total_item], spacing=20)]
    
    nome_produto.update()
    qtd_produto.update()
    semanal_produto.update()
    coluna_insumos.update()

nome_produto = ft.TextField(hint_text="Ex: Cosmopolitan", width=290)
qtd_produto = ft.TextField(hint_text="Ex: 2", width=290, on_change=validar_numeros)
semanal_produto = ft.TextField(hint_text="Ex: 4", width=290, on_change=validar_numeros)

#====================================================================================================

btn_calcular = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=calcular_totais,
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.CALCULATE, color="white"),
            ft.Text("Calcular", color="white")
        ]
    )
)

btn_novo = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=novo_produto_clique,
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.AUTORENEW, color="white"),
            ft.Text("Novo Produto", color="white")
        ]
    )
)

btn_novo_insumo = ft.Container(
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
#===================================================================================================

def calcular_estoque_compra(page: ft.Page):
    if not coluna_insumos.controls:
        novo_nome = ft.AutoComplete(
            suggestions=sugestoes, 
            width=250,
            on_select=salvar_texto_autocomplete,
            on_change=salvar_texto_autocomplete,
            data=""
        )

        txt_uni_medi= ft.Dropdown(   
                            options=[
                                    ft.dropdown.Option("KG"),
                                    ft.dropdown.Option("UNID"),
                                    ft.dropdown.Option("ML")
                                     ], width=112
                            )
        nova_qtd = ft.TextField(width=112, on_change=validar_numeros)
        novo_volume = ft.TextField(width=112, read_only=True, value="0.00")
        novo_total = ft.TextField(width=112, read_only=True, value="R$ 0.00")
        novo_total_item = ft.TextField(width=112, read_only=True, value="0")
        
        lista_referencias_insumos.append({
            "nome": novo_nome,
            "qtd": nova_qtd,
            "volume": novo_volume,
            "total": novo_total,
            "total_item": novo_total_item
        })
        coluna_insumos.controls = [ft.Row(
            [novo_nome, nova_qtd,txt_uni_medi, novo_volume, novo_total, novo_total_item]
            , spacing=20)]
        
    return ft.Container(
        ft.Stack(
            controls=[
                ft.Container(
                    width=960,
                    height=640,
                    bgcolor="white",
                    padding=20,
                    border_radius=10,
                    top=20,
                    left=40,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.GREY, offset=ft.Offset(1,1)),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                    ft.Text("Simulação de Estoque", size=28),
                                ]
                            ),

                            ft.Divider(),
                            ft.Row(
                                controls=[
                                    ft.Text("Nome", weight=ft.FontWeight.BOLD, width=290),
                                    ft.Text("Venda Diária", weight=ft.FontWeight.BOLD, width=290),
                                    ft.Text("Dias de Vendas", weight=ft.FontWeight.BOLD, width=290),
                                ],alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                            ft.Row(controls=[nome_produto, qtd_produto, semanal_produto], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                            ft.Container(height=20),
                            ft.Container(
                                width=920,
                                height=50,
                                bgcolor="#1E3A8A",
                                border_radius=10,
                                content=ft.Row(
                                        controls=[
                                            ft.Text("Projeção",size=20, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER
                            ),
                                
                            ),                            
                            
                            ft.Container(width=100),
                            ft.Row(
                                controls=[
                                    ft.Text("Insumos:", weight=ft.FontWeight.BOLD,width=250),
                                    ft.Text("Quantidade", weight=ft.FontWeight.BOLD, width=112),
                                    ft.Text("Unidade", weight=ft.FontWeight.BOLD, width=112),
                                    ft.Text("Volume", weight=ft.FontWeight.BOLD, width=112),
                                    ft.Text("Custo", weight=ft.FontWeight.BOLD, width=112),
                                    ft.Text("estoque", weight=ft.FontWeight.BOLD, width=112),
                                ], alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                            coluna_insumos,
                            btn_novo_insumo,
                            ft.Divider(),
                            ft.Container(
                                ft.Row(
                                    controls=[
                                        btn_novo,
                                        btn_calcular,
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                    spacing=10
                                ),
                            )
                        ]
                    )
                ),
            ],
        )
    )
