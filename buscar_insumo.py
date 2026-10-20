import flet as ft
from database import obter_insumos
from database import obter_conexao, obter_detalhes_insumos


resultado_container = ft.Column()

    
def realizar_busca_insumo(e):
        
    if hasattr(e, "selection") and e.selection:
        nome_selecionado_insumo = e.selection.value
    else:
        nome_selecionado_insumo = txt_buscar_insumo.value

    nome_selecionado_insumo = str(nome_selecionado_insumo).strip()
        
    if not nome_selecionado_insumo:
        resultado_container.controls = [ft.Text("Selecione ou digite o nome do produto.", color="red")]
        page.update()
        return

    linhas_receita = obter_detalhes_insumos(nome_selecionado_insumo)
        
    if status_erro := verificar_erros_busca(linhas_receita, nome_selecionado_insumo):
        resultado_container.controls = [status_erro]
        page.update()
        return

    componentes_resultado = []
        
    for uni_medi, quantidade, custo, fornecedor, telefone, email, comentario, data_cadastro in linhas_receita:

        data_formatada = data_cadastro.strftime("%d/%m/%Y") if hasattr(data_cadastro, "strftime") else str(data_cadastro)
            
        componentes_resultado.extend([
            ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_300),
                
            ft.Row(
                controls=[ft.Text(f"{nome_selecionado_insumo.upper()}", size=20, weight="bold", color="green")],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                
            ft.Container(
                width=300,
                height=400,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Quantidade/Volume:", weight=ft.FontWeight.BOLD),
                                ft.Text("Custo:", weight=ft.FontWeight.BOLD),
                                ft.Text("Fornecedor:", weight=ft.FontWeight.BOLD),
                                ft.Text("Telefone:", weight=ft.FontWeight.BOLD),
                                ft.Text("E-mail:", weight=ft.FontWeight.BOLD),
                                ft.Text("Data de Cadastro:", weight=ft.FontWeight.BOLD),
                                ft.Text("Comentário:", weight=ft.FontWeight.BOLD),
                                         ]
                                    ),

                        ft.Column(
                            controls=[
                                ft.Text(f"{quantidade} {uni_medi}"),
                                ft.Text( f"R$ {custo:.2f}"),
                                ft.Text(f"{fornecedor}"),
                                ft.Text(f"{telefone}"),
                                ft.Text(f"{email}"),
                                ft.Text(f"{data_formatada}"),
                                ft.Text(f"{comentario}"),
                                         ]
                                    ),
                            
                                
                            ], spacing=70
                        )
                    )
                ])
            
    resultado_container.controls = componentes_resultado
    


    
def verificar_erros_busca(linhas, nome):
    if linhas is None:
        return ft.Text("Erro interno ao buscar no banco de dados.", color="red", weight="bold")
    if len(linhas) == 0:
        return ft.Text(f"Nome '{nome}' não localizado no catálogo.", color="orange")
    return None

dados_insumos = obter_insumos()
sugestoes_autocomplete_insumos = [
    ft.AutoCompleteSuggestion(key=nome["nome"], value=nome["nome"]) 
    for nome in dados_insumos
    ]

txt_buscar_insumo = ft.AutoComplete(
    suggestions=sugestoes_autocomplete_insumos,
    width=400,
    on_select=realizar_busca_insumo 
    )

def buscar_insumo(page: ft.Page):
    return ft.Container(
        ft.Stack(
            controls=[
                ft.Image(src="desfoque.png", filter_quality=ft.FilterQuality.LOW),
                ft.Container(
                        padding=20,
                        width=600,
                        height=600, 
                        top=50,
                        left=455, 
                        bgcolor="white",
                        border_radius=10,
                        shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=10, color=ft.Colors.BLACK,
                        offset=ft.Offset(0, 1),          
                    ), 
                    content=ft.Column(
                        controls=[
                            ft.Text("Buscar Insumo", size=32, weight=ft.FontWeight.BOLD),
                            ft.Row(controls=[txt_buscar_insumo], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Container(content=resultado_container, width=600, height=400, padding=0),
                            ft.Button("Cancelar")
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    )   
                ]
            )
        )




