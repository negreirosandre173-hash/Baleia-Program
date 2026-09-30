import flet as ft
from database import obter_conexao, obter_nome_produto, deletar_produto_por_nome

# 1. Escopo Global Inicial
nome_selecionado_produto = ""
resultado_container = ft.Column()

dados_nome_produto = obter_nome_produto()

sugestoes_nome_autocomplete = [
    ft.AutoCompleteSuggestion(key=nome_produto, value=nome_produto)
    for nome_produto in dados_nome_produto
]

# 2. Instancia o componente antes de ser lido pela função (Evita NameError)
txt_buscar_nome_produto = ft.AutoComplete(
    suggestions=sugestoes_nome_autocomplete,
)

# 3. Funções de Manipulação da Interface
def realizar_busca_nome_produto(e, page: ft.Page = None):
    global nome_selecionado_produto

    if not page and hasattr(e, "page"):
        page = e.page

    if hasattr(e, "selection") and e.selection:
        nome_selecionado_produto = (
            e.selection.value if hasattr(e.selection, "value") else str(e.selection)
        )
    else:
        nome_selecionado_produto = txt_buscar_nome_produto.value

    nome_selecionado_produto = str(nome_selecionado_produto).strip()

    if not nome_selecionado_produto:
        resultado_container.controls = [
            ft.Text(" Selecione ou digite o nome do produto.", color="red")
        ]
        if page:
            page.update()
        return

    resultado_container.controls = [
        ft.Row(
            controls=[
                ft.Text(
                    f"Produto selecionado: {nome_selecionado_produto}", color="green"
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]
    if page:
        page.update()

# Vincula o evento após a criação da função
txt_buscar_nome_produto.on_select = lambda e: realizar_busca_nome_produto(e, e.page)

# 4. Componente Visual da Janela de Edição
def editar_produto(page: ft.Page, voltar):
    
    # Evento de clique que chama a exclusão do banco e atualiza os elementos visuais
    def clicar_deletar(e):
        global nome_selecionado_produto
        
        # Puxa o valor do campo atualizado
        nome_para_deletar = txt_buscar_nome_produto.value.strip() if txt_buscar_nome_produto.value else nome_selecionado_produto

        if not nome_para_deletar:
            resultado_container.controls = [
                ft.Row(
                    controls=[ft.Text("Nenhum produto selecionado.", color="red")],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
            page.update()
            return

        try:
            # Envia a string pura para o arquivo database.py
            deletar_produto_por_nome(nome_para_deletar)

            resultado_container.controls = [
                ft.Row(
                    controls=[
                        ft.Text(
                            f"Produto '{nome_para_deletar}' deletado com sucesso!", 
                            color="green", 
                            weight=ft.FontWeight.BOLD
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
            txt_buscar_nome_produto.value = ""
            nome_selecionado_produto = ""
            
        except Exception as erro:
            resultado_container.controls = [
                ft.Row(
                    controls=[ft.Text(f"Erro ao deletar: {erro}", color="red")],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        
        page.update()

    return ft.Container(
        content=ft.Stack(
            controls=[
                ft.Image(
                    src="desfoque.png",
                    expand=True,
                    filter_quality=ft.FilterQuality.LOW,
                ),
                ft.Container(
                    padding=20, width=600, height=600, bgcolor="white", top=50, left=455, border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK, offset=ft.Offset(0, 1)),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[ft.Text("Editar Produto", size=35, weight=ft.FontWeight.BOLD)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Divider(height=10, thickness=1, color=ft.Colors.BLUE),
                            ft.Text("Nome do Produto", size=20, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Container(content=txt_buscar_nome_produto, width=300),
                                    ft.ElevatedButton("Buscar", on_click=lambda e: realizar_busca_nome_produto(e, page)),
                                ]
                            ),
                            ft.Container(content=resultado_container, expand=True),
                            ft.Divider(color=ft.Colors.WHITE, height=5),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("excluir", on_click=clicar_deletar), # Corrigido para chamar o fluxo de interface
                                    ft.ElevatedButton("Cancelar", on_click=voltar),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                ),
            ]
        )
    )
