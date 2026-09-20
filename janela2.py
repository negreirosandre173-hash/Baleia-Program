import flet as ft
from janela1 import on_change_custo
from database import obter_insumos, salvar_produto

lista_referencias_insumos = []
coluna_insumos = ft.Column()
dados_banco = obter_insumos()
sugestoes = [ft.AutoCompleteSuggestion(key=item["nome"], value=item["nome"]) for item in dados_banco]




def validar_numeros(e):
    texto_limpo = "".join(c for c in e.control.value if c.isdigit())
    if e.control.value != texto_limpo:
        e.control.value = texto_limpo
        e.control.update()

nome_produto = ft.TextField(label="Nome Produto:", hint_text="Ex: Cosmopolitan", width=320)

novo_codigo = ft.TextField(label="Código Produto", hint_text="Ex: 123...", width=120, on_change=validar_numeros)


def adicionar_campo(e):
    novo_insumo = ft.AutoComplete(suggestions=sugestoes, width=200)
    nova_categoria = ft.Dropdown(
        label="categoria", 
        options=[ft.dropdown.Option("KG"), ft.dropdown.Option("UND"), ft.dropdown.Option("ML")],
        value=None
    )
    nova_qtd = ft.TextField(label="QTD", width=80, on_change=validar_numeros)
    
    nova_linha = ft.Row([novo_insumo, nova_categoria, nova_qtd])

    lista_referencias_insumos.append({
        "nome": novo_insumo,
        "categoria": nova_categoria,
        "qtd": nova_qtd
    })
    
    coluna_insumos.controls.append(nova_linha)

    if coluna_insumos.page:
        coluna_insumos.update() 


def salvar_dados(e):
    page = e.control.page

    produto_final = {
        "nome": nome_produto.value.upper(),
        "codigo": novo_codigo.value,
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
            
            produto_final["insumos"].append({
                "insumo_id": insumo_identificador,  
                "categoria": insumo["categoria"].value,
                "quantidade": qtd_limpa
            })
    
    salvar_produto(produto_final)
  
    nome_produto.value = ""
    novo_codigo.value = ""
    lista_referencias_insumos.clear()
    coluna_insumos.controls.clear()
    
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
    coluna_insumos.controls.append(ft.Row([novo_nome, nova_categoria, nova_qtd]))
    
    if page:
        page.update()



def janel2(page: ft.Page, voltar):

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
                            ft.Text("Cadastro de Produto", size=35, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=10, thickness=1, color=ft.Colors.BLUE),
                            ft.Text("Informações Básicas", weight=ft.FontWeight.BOLD),
                            ft.Row(controls=[nome_produto, novo_codigo]),
                            ft.Text("Insumos:"),
                            coluna_insumos,
                            ft.ElevatedButton("Adicionar Insumo", on_click=adicionar_campo),
                            ft.Divider(),
                            ft.Container(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton("Cancelar", on_click=voltar),
                                        ft.FilledButton("Salvar", on_click=salvar_dados) 
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
