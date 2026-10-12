import flet as ft
from cadastrar_insumo import on_change_custo
from database import obter_insumos, salvar_produto, salvar_dados, obter_custo_medio_insumo  
from lista_em_pdf import gerar_pdf_lista_compras

lista_referencias_insumos = []
coluna_insumos = ft.Column()

dados_banco = obter_insumos()
sugestoes = [ft.AutoCompleteSuggestion(key=item["nome"], value=item["nome"]) for item in dados_banco]

def validar_numeros(e):
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()

def deletar_linha(linha_controle, referencias):
    coluna_insumos.controls.remove(linha_controle)
    lista_referencias_insumos.remove(referencias)
    coluna_insumos.update()


def tratar_selecao_insumo(e, texto_custo_medio):
    nome_selecionado = e.control.value
    custo_medio = obter_custo_medio_insumo(nome_selecionado)
    
    texto_custo_medio.value = f"CUSTO MÉDIO: R$ {custo_medio:.2f}"
    texto_custo_medio.update()

def adicionar_campo(e):
    texto_medio = ft.Text("Média: R$ 0.00", size=12, color=ft.Colors.GREY_600)
    
    novo_insumo = ft.AutoComplete(
        suggestions=sugestoes, 
        width=280,
        on_select=lambda e: tratar_selecao_insumo(e, texto_medio),
        on_change=lambda e: tratar_selecao_insumo(e, texto_medio)
    )
    nova_qtd = ft.TextField( width=100)
    
    referencias = {
        "nome": novo_insumo,
        "qtd": nova_qtd,
        "custo_medio_visual": texto_medio 
    }
    
    botao_remover = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_color=ft.Colors.BLUE,
        tooltip="Remover Insumo",
        on_click=lambda _: deletar_linha(nova_linha, referencias)
    )
    
    bloco_insumo = ft.Column([novo_insumo, texto_medio], spacing=2)
    nova_linha = ft.Row([bloco_insumo, nova_qtd, botao_remover], vertical_alignment=ft.CrossAxisAlignment.START)
    
    lista_referencias_insumos.append(referencias)
    coluna_insumos.controls.append(nova_linha)
    
    if coluna_insumos.page:
        coluna_insumos.update()

def lista_de_compras(page: ft.Page, voltar):
    if not coluna_insumos.controls:
        texto_medio_inicial = ft.Text("Média: R$ 0.00", size=12, color=ft.Colors.GREY_600)
        
        novo_nome = ft.AutoComplete(
            suggestions=sugestoes, 
            width=280,
            on_select=lambda e: tratar_selecao_insumo(e, texto_medio_inicial),
            on_change=lambda e: tratar_selecao_insumo(e, texto_medio_inicial)
        )
        nova_qtd = ft.TextField( width=100)
        
        referencias_inicial = {
            "nome": novo_nome,
            "qtd": nova_qtd,
            "custo_medio_visual": texto_medio_inicial
        }
        
        botao_remover_inicial = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.BLUE,
            tooltip="Remover Insumo",
            on_click=lambda _: deletar_linha(linha_inicial, referencias_inicial)
        )
        
        bloco_insumo_inicial = ft.Column([novo_nome, texto_medio_inicial], spacing=2)
        linha_inicial = ft.Row([bloco_insumo_inicial, nova_qtd, botao_remover_inicial], vertical_alignment=ft.CrossAxisAlignment.START)
        
        lista_referencias_insumos.append(referencias_inicial)
        coluna_insumos.controls = [linha_inicial]

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
                    top=30,
                    left=400,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK, offset=ft.Offset(0,1)),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Text("Lista de Compras", size=35, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=10, thickness=1, color=ft.Colors.BLUE),
                            ft.Row(
                                controls=[
                                    ft.Text("Insumos:", weight=ft.FontWeight.BOLD),
                                    ft.Text("Quantidade:", weight=ft.FontWeight.BOLD),

                                ], spacing=230
                            ),
                            coluna_insumos,
                            ft.Button("Adicionar Insumo", on_click=adicionar_campo),
                            ft.Divider(),
                            ft.Container(
                                ft.Row(
                                    controls=[
                                        ft.Button("Cancelar", on_click=voltar),
                                        ft.IconButton(
                                            icon=ft.Icons.PRINT,
                                            icon_color=ft.Colors.BLUE,
                                            tooltip="Imprimir Lista em PDF",
                                            on_click=lambda _: gerar_pdf_lista_compras(lista_referencias_insumos)
                                        ),
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