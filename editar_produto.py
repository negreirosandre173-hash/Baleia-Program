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
    suggestions=sugestoes_nome_autocomplete,width=720
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

def adicionar_campo(e):
    novo_insumo = ft.AutoComplete(suggestions=sugestoes, width=300)
    nova_categoria = ft.Dropdown(
        width=280,
        label="categoria", 
        options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")],
        value=None
    )
    nova_qtd = ft.TextField(label="QTD", width=280, on_change=validar_numeros)
    
    nova_linha = ft.Row([novo_insumo, nova_categoria, nova_qtd])

    lista_referencias_insumos.append({
        "nome": novo_insumo,
        "categoria": nova_categoria,
        "qtd": nova_qtd,
        

    })
    
    coluna_insumos.controls.append(nova_linha)

    if coluna_insumos.page:
        coluna_insumos.update() 



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


btn_salvar = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=disparar_salvamento,
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.SAVE, color="white"),
            ft.Text("Salvar", color="white")
        ]
    )
)

btn_excluir_dados = ft.Container(
    bgcolor="#1E3A8A",
    width=180,
    height=40,
    border_radius=10,
    on_click=clicar_deletar,
    ink=True,
    content=ft.Row(
        controls=[
            ft.Text(""),
            ft.Icon(ft.Icons.DELETE_FOREVER, color="white"),
            ft.Text("Excluir", color="white")
        ]
    )
)

btn_adicionar = ft.Container(
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
            ft.Text("Adicionar Insumos", color="white")
        ]
    )
)



def cadastrar_produto_editado(page: ft.Page):

    if not coluna_insumos.controls:
        novo_nome = ft.AutoComplete(suggestions=sugestoes, width=300)
        nova_categoria = ft.Dropdown(
            width=280,
            label="categoria", 
            options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")]
        )
        nova_qtd = ft.TextField(label="QTD", width=280, on_change=validar_numeros)
        
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
                    width=920, height=640, bgcolor="white", padding=20, border_radius=10, top=20, left=40,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.GREY, offset=ft.Offset(1,1)),
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                    ft.Text("Editar Produto", size=28),
                                ]
                            ),
                            ft.Row(controls=[
                                ft.Container(
                                             content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE, size=25, margin=20),
                                                    nome_produto
                                                ],spacing=30
                                             ),
                                             width=880,
                                             height=60,
                                             border_radius=10,
                                             border=ft.Border.all(width=1, color=ft.Colors.GREY),),
                                             ]),
                            ft.Text("Insumos:"),
                            coluna_insumos,
                            btn_adicionar,
                            ft.Container(content=resultado_container),
                            ft.Container(
                                ft.Row(
                                    controls=[
                                        btn_excluir_dados,
                                        btn_salvar,
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





