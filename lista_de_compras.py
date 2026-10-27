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
    texto_medio = ft.Text("MÉDIA: R$ 0.00", size=12, color=ft.Colors.BLACK)
    
    novo_insumo = ft.AutoComplete(
        suggestions=sugestoes, 
        width=280,
        on_select=lambda e: tratar_selecao_insumo(e, texto_medio),
        on_change=lambda e: tratar_selecao_insumo(e, texto_medio)
    )

    txt_uni_medi= ft.TextField(hint_text="Ex: Gramas")

    nova_qtd = ft.TextField( width=280)
    
    referencias = {
        "nome": novo_insumo,
        "qtd": nova_qtd,
        "unid": txt_uni_medi,
        "custo_medio_visual": texto_medio 
    }
    
    botao_remover = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_color=ft.Colors.RED,
        tooltip="Remover Insumo",
        on_click=lambda _: deletar_linha(nova_linha, referencias)
    )
    
    bloco_insumo = ft.Column([novo_insumo, texto_medio], spacing=2)
    nova_linha = ft.Row([bloco_insumo, nova_qtd, txt_uni_medi, botao_remover], vertical_alignment=ft.CrossAxisAlignment.START)
    
    lista_referencias_insumos.append(referencias)
    coluna_insumos.controls.append(nova_linha)
    
    if coluna_insumos.page:
        coluna_insumos.update()

#=======================================================================================


btn_print = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=lambda _: gerar_pdf_lista_compras(lista_referencias_insumos),
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(icon=ft.Icons.PRINT, color="white"),
            ft.Text("Imprimir", color="white")
        ]
    )
)

btn_adicionar_insumo = ft.Container(
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
            ft.Text("Adicionar", color="white")
        ]
    )
)

#=============================================================================================


def lista_de_compras(page: ft.Page):
    if not coluna_insumos.controls:
        texto_medio_inicial = ft.Text("MÉDIA: R$ 0.00", size=12, color=ft.Colors.BLACK)
        
        novo_nome = ft.AutoComplete(
            suggestions=sugestoes, 
            width=280,
            on_select=lambda e: tratar_selecao_insumo(e, texto_medio_inicial),
            on_change=lambda e: tratar_selecao_insumo(e, texto_medio_inicial)
        )

        txt_uni_medi= ft.TextField(hint_text="Ex: Gramas")

        nova_qtd = ft.TextField( width=280)
        
        referencias_inicial = {
            "nome": novo_nome,
            "qtd": nova_qtd,
            "unid": txt_uni_medi,
            "custo_medio_visual": texto_medio_inicial
        }
        
        botao_remover_inicial = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.RED,
            tooltip="Remover Insumo",
            on_click=lambda _: deletar_linha(linha_inicial, referencias_inicial)
        )
        
        bloco_insumo_inicial = ft.Column([novo_nome, texto_medio_inicial], spacing=2)
        linha_inicial = ft.Row([bloco_insumo_inicial, nova_qtd, txt_uni_medi, botao_remover_inicial], vertical_alignment=ft.CrossAxisAlignment.START)
        
        lista_referencias_insumos.append(referencias_inicial)
        coluna_insumos.controls = [linha_inicial]

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
                                    ft.Text("Lista de Compras", size=28),
                                    
                                ]
                            ),
                            ft.Divider(height=10, thickness=1),
                            ft.Row(
                                controls=[
                                    ft.Text("Insumos:", weight=ft.FontWeight.BOLD, width=280),
                                    ft.Text("Quantidade:", weight=ft.FontWeight.BOLD, width=280),
                                    ft.Text("Unidade:", weight=ft.FontWeight.BOLD, width=280),
                                ]
                            ),
                            coluna_insumos,
                            btn_adicionar_insumo,
                            ft.Divider(),
                            ft.Row(
                                controls=[
                                    btn_print
                                ], alignment=ft.MainAxisAlignment.END
                            )
                        ]
                    )
                ),
            ],
        )
    )