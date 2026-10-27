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
                
            ft.Row(
                margin=0,
                controls=[
                    ft.Container(width=20),
                    ft.Container(
                        width=750,
                        bgcolor="#1E3A8A",
                        height=70,
                        padding=20,
                        border_radius=10,
                        border=ft.Border.all(width=1, color=ft.Colors.GREY),
                        content=ft.Row(
                            controls=[
                                ft.Text(f"{nome_selecionado_insumo.upper()}", size=16, weight="bold", color="white"),
                            ], alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        )
                    ),
                    ft.Container(width=20),
                ],spacing=60,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(width=20),
                        ft.Container(
                            width=750,
                            height=350,
                            border_radius=10,
                            border=ft.Border.all(width=1, color=ft.Colors.GREY),
                            content=ft.Row(
                                controls=[
                                    ft.Container(width=30),
                                    ft.Column(
                                        controls=[
                                            ft.Container(height=5),
                                            ft.Text("QUANTIDADE:", weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text("CUSTO:", weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text("FORNECEDOR:", weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text("TELEFONE:", weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text("E-MAIL:", weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text("DATA DE CADASTRO:", weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text("COMENTÁRIO:", weight=ft.FontWeight.BOLD, size=16),
                                                ], spacing=15
                                            ),
                                    ft.Column(
                                        controls=[
                                            ft.Container(height=10),
                                            ft.Text(f"{quantidade} {uni_medi}", size=14),
                                            ft.Text( f"R$ {custo:.2f}", color="green", size=14),
                                            ft.Text(f"{fornecedor}", size=14),
                                            ft.Text(f"{telefone}", size=14),
                                            ft.Text(f"{email}", size=14),
                                            ft.Text(f"{data_formatada}", size=16),
                                            ft.Text(f"{comentario}", size=14),
                                            ], spacing=15
                                    
                                        ),
                                    ft.Container(width=30),
                                    
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                            
                     ], spacing=60
                  )
                )
            ]
        )
            
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
    width=760, 
    on_select=realizar_busca_insumo,
) 


def buscar_insumo(page: ft.Page):
    return ft.Container(
        ft.Stack(
            controls=[
                ft.Container(
                        padding=20,
                        height=640,
                        width=960,
                        top= 20,
                        left=40, 
                        bgcolor="white",
                        border_radius=10,
                        shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=3, color=ft.Colors.GREY,
                        offset=ft.Offset(1, 1),          
                            ),
                        content=ft.Column(
                            controls=[
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.ASSIGNMENT_SHARP, color="#1E3A8A", size=50),
                                    ft.Text("Buscar Insumo", size=28),
                                ]),
                                ft.Divider(),
                                ft.Container(
                                    width=930,
                                    height=60,
                                    border_radius=10,
                                    border=ft.Border.all(width=1, color=ft.Colors.GREY),
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE, size=25, margin=10),
                                            ft.Row(controls=[txt_buscar_insumo], alignment=ft.MainAxisAlignment.CENTER),
                                                ], spacing=80
                                            )
                                        ),
                                ft.Container(height=20),
                                ft.Container(content=resultado_container, 
                                    width=600, 
                                    height=400, 
                                    padding=0,
                            
                                    ),
                                ],
                            ),
                        )   
                    ]
                )
            )




