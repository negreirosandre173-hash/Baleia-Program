import flet as ft

def janel4(page: ft.Page, voltar):
    return ft.Container(
        ft.Stack(
            controls=[
                ft.Image(src="desfoque.png", expand=True, filter_quality=ft.FilterQuality.LOW),
                ft.Container(
                    padding=20,
                    width=500,
                    height=300,
                    bgcolor="white",
                    top= 200,
                    left=455,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                          spread_radius=1,blur_radius=10,color=ft.Colors.BLACK,
                          offset=ft.Offset(0,1),          
                     ), 
                    content=ft.Column(
                        controls=[
                            ft.Text("Buscar Insumo", size=35, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=10, thickness=1,color=ft.Colors.BLUE,),
                            ft.Text("Nome do Produto", size=20, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                            ft.TextField(hint_text="EX: Açúcar"),
                            ft.ElevatedButton("Buscar")
                                ]
                             ),
                             ft.Divider(color=ft.Colors.WHITE),
                             ft.Row(
                                controls=[
                                    ft.ElevatedButton("Cancelar", on_click=voltar)
                                ], 
                                alignment=ft.MainAxisAlignment.END,
                             )
                            
                            
                                 ]

                        )         
                ),
            
            ]
        )
    )


    


