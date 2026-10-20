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
        width=200,
        on_select=salvar_texto_autocomplete,
        on_change=salvar_texto_autocomplete,
        data=""
    )
    nova_qtd = ft.TextField(width=90, on_change=validar_numeros)
    novo_volume = ft.TextField(width=120, read_only=True, value="0.00")
    novo_total = ft.TextField(width=120, read_only=True, value="R$ 0.00")
    novo_total_item = ft.TextField(width=100, read_only=True, value="0")
    
    nova_linha = ft.Row([novo_insumo, nova_qtd, novo_volume, novo_total, novo_total_item], spacing=25) 
    
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
        width=200,
        on_select=salvar_texto_autocomplete,
        on_change=salvar_texto_autocomplete,
        data=""
    )
    nova_qtd = ft.TextField(width=90, on_change=validar_numeros)
    novo_volume = ft.TextField(width=120, read_only=True, value="0.00")
    novo_total = ft.TextField(width=120, read_only=True, value="R$ 0.00")
    novo_total_item = ft.TextField(width=100, read_only=True, value="0")
    
    lista_referencias_insumos.append({
        "nome": novo_nome,
        "qtd": nova_qtd,
        "volume": novo_volume,
        "total": novo_total,
        "total_item": novo_total_item
    })
    coluna_insumos.controls = [ft.Row([novo_nome, nova_qtd, novo_volume, novo_total, novo_total_item], spacing=25)]
    
    nome_produto.update()
    qtd_produto.update()
    semanal_produto.update()
    coluna_insumos.update()

nome_produto = ft.TextField(hint_text="Ex: Cosmopolitan", width=250)
qtd_produto = ft.TextField(hint_text="Ex: 2", width=90, on_change=validar_numeros)
semanal_produto = ft.TextField(hint_text="Ex: 4", width=90, on_change=validar_numeros)

def calcular_estoque_compra(page: ft.Page):
    if not coluna_insumos.controls:
        novo_nome = ft.AutoComplete(
            suggestions=sugestoes, 
            width=200,
            on_select=salvar_texto_autocomplete,
            on_change=salvar_texto_autocomplete,
            data=""
        )
        nova_qtd = ft.TextField(width=90, on_change=validar_numeros)
        novo_volume = ft.TextField(width=120, read_only=True, value="0.00")
        novo_total = ft.TextField(width=120, read_only=True, value="R$ 0.00")
        novo_total_item = ft.TextField(width=100, read_only=True, value="0")
        
        lista_referencias_insumos.append({
            "nome": novo_nome,
            "qtd": nova_qtd,
            "volume": novo_volume,
            "total": novo_total,
            "total_item": novo_total_item
        })
        coluna_insumos.controls = [ft.Row([novo_nome, nova_qtd, novo_volume, novo_total, novo_total_item], spacing=25)]
        
    return ft.Container(
        ft.Stack(
            controls=[
                ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
                ft.Container(
                    width=780,
                    height=600,
                    bgcolor="white",
                    padding=20,
                    border_radius=10,
                    top=30,
                    left=350,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK, offset=ft.Offset(0,1)),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Text("Simulação de Estoque", size=35, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=10, thickness=1, color=ft.Colors.BLUE),
                            ft.Row(
                                controls=[
                                    ft.Text("Nome", weight=ft.FontWeight.BOLD, width=250),
                                    ft.Text("Consumo Diário", weight=ft.FontWeight.BOLD, width=200),
                                    ft.Text("Venda Semanal", weight=ft.FontWeight.BOLD, width=200),
                                ],
                                spacing=20
                            ),
                            ft.Row(controls=[nome_produto, qtd_produto, semanal_produto], spacing=20),
                            ft.Container(width=100),
                            ft.Row(
                                controls=[
                                    ft.Text("Projeção", weight=ft.FontWeight.BOLD, size=20),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Container(width=100),
                            ft.Row(
                                controls=[
                                    ft.Text("Insumos:", weight=ft.FontWeight.BOLD,),
                                    ft.Text("und/g/ml", weight=ft.FontWeight.BOLD),
                                    ft.Text("Volume", weight=ft.FontWeight.BOLD),
                                    ft.Text("Custo", weight=ft.FontWeight.BOLD),
                                    ft.Text("estoque", weight=ft.FontWeight.BOLD),
                                ],
                                spacing=90
                            ),
                            coluna_insumos,
                            ft.Button("Adicionar Insumo", on_click=adicionar_campo),
                            ft.Divider(),
                            ft.Container(
                                ft.Row(
                                    controls=[
                                        ft.Button("Novo Produto", on_click=novo_produto_clique),
                                        ft.Button("Cancelar",),
                                        ft.Button("Calcular", on_click=calcular_totais)
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
