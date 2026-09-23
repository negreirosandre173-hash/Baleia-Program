import flet as ft

def main(page: ft.Page):
    page.title = "Exemplo de GridView"
    page.theme_mode = ft.ThemeMode.DARK
    
    grid = ft.GridView(
        expand=True,
        runs_count=4,
        spacing=10,
        run_spacing=10,
        controls=[
            ft.Container(
                content=ft.Text(f"Item {i}", color=ft.Colors.WHITE),
                
                bgcolor=ft.Colors.BLUE_700,
                border_radius=5,
            )
            for i in range(20)
        ],
    )
    
    page.add(grid)

ft.app(target=main)
