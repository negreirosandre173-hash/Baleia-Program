import flet as ft
from cadastrar_insumo import on_change_custo
from database import obter_insumos, salvar_produto, obter_conexao, obter_nome_produto, deletar_produto_por_nome, salvar_produto_editado
from cadastrar_produto import adicionar_campo


 
lista_referencias_insumos = [] 
coluna_insumos = ft.Column()
dados_banco = obter_insumos()
sugestoes = [ft.AutoCompleteSuggestion(key=item["nome"], value=item["nome"]) for item in dados_banco]

nome_selecionado_produto = ""
resultado_container = ft.Column()
dados_nome_produto = obter_nome_produto()

sugestoes_nome_autocomplete = [
    ft.AutoCompleteSuggestion(key=nome_produto, value=nome_produto)
    for nome_produto in dados_nome_produto
]

txt_buscar_nome_produto = ft.AutoComplete(
    suggestions=sugestoes_nome_autocomplete,width=200
)

def clicar_deletar(e):
        global nome_selecionado_produto
        global resultado_container
              
        nome_para_deletar = txt_buscar_nome_produto.value.strip() if txt_buscar_nome_produto.value else nome_selecionado_produto

        try:
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


def validar_numeros(e):
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()

nome_produto = txt_buscar_nome_produto


def cadastrar_produto_editado(page: ft.Page):

    if not coluna_insumos.controls:
        novo_nome = ft.AutoComplete(suggestions=sugestoes, width=200)
        nova_categoria = ft.Dropdown(
            label="categoria", 
            options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")]
        )
        nova_qtd = ft.TextField(label="QTD", width=80, on_change=validar_numeros)
        
        lista_referencias_insumos.append({
            "nome": novo_nome,
            "categoria": nova_categoria,
            "qtd": nova_qtd
        })
        coluna_insumos.controls = [ft.Row([novo_nome, nova_categoria, nova_qtd])]

    return ft.Container(
        ft.Stack(
            controls=[
                ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
                ft.Container(
                    width=550, height=600, bgcolor="white", padding=20, border_radius=10, top=30, left=400,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK, offset=ft.Offset(0,1)),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Text("Editar Produto", size=35, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=10, thickness=1, color=ft.Colors.BLUE),
                            ft.Text("Selecionar Produto", weight=ft.FontWeight.BOLD),
                            ft.Row(controls=[nome_produto ]),
                            ft.Text("Insumos:"),
                            coluna_insumos,
                            ft.Button("Adicionar Insumo", on_click=adicionar_campo),
                            ft.Divider(),
                            ft.Container(content=resultado_container),
                            ft.Container(
                                ft.Row(
                                    controls=[
                                        ft.Button("excluir" ,on_click=clicar_deletar),
                                        ft.Button("Cancelar"),
                                        ft.Button("Salvar", on_click=disparar_salvamento) 
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


def disparar_salvamento(e):
    page = e.control.page
    
    global nome_selecionado_produto
    nome_antigo_str = nome_selecionado_produto if nome_selecionado_produto else txt_buscar_nome_produto.value

    if not nome_antigo_str:
        print("Erro: Nenhum produto selecionado para edição.")
        return

    produto_dados = {
        "nome": txt_buscar_nome_produto.value.upper(),
        "insumos": []
    }
    
    for insumo in lista_referencias_insumos:
        nome_valor = insumo["nome"].value if insumo["nome"].value else ""
        
        if nome_valor:
            id_insumo = None
            for item in dados_banco:
                if item["nome"] == nome_valor:
                    id_insumo = item["id"]
                    break
            
            insumo_identificador = id_insumo if id_insumo is not None else nome_valor
            
            qtd_texto = insumo["qtd"].value if insumo["qtd"].value else "0"
            qtd_limpa = qtd_texto.replace(",", ".")
            
            produto_dados["insumos"].append({
                "insumo_id": insumo_identificador,  
                "categoria": insumo["categoria"].value,
                "quantidade": qtd_limpa
            })
    
    try:
        salvar_produto_editado(produto_dados, nome_antigo_str)
        resultado_container.controls = [
            ft.Row([ft.Text("Produto editado!", color="green", weight=ft.FontWeight.BOLD)], 
                   alignment=ft.MainAxisAlignment.CENTER)
        ]
        
        txt_buscar_nome_produto.value = ""
        lista_referencias_insumos.clear()
        coluna_insumos.controls.clear()
        
        novo_nome = ft.AutoComplete(suggestions=sugestoes, width=200)
        nova_categoria = ft.Dropdown(
            label="categoria", 
            options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")]
        )
        nova_qtd = ft.TextField(label="QTD", width=80, on_change=validar_numeros)
        
        lista_referencias_insumos.append({"nome": novo_nome, "categoria": nova_categoria, "qtd": nova_qtd})
        coluna_insumos.controls.append(ft.Row([novo_nome, nova_categoria, nova_qtd]))
        
        if page:
            page.update()
            
    except Exception as erro:
        resultado_container.controls = [
            ft.Row([ft.Text(f"Erro ao salvar edição: {erro}", color="red")], alignment=ft.MainAxisAlignment.CENTER)
        ]
        if page:
            page.update()


