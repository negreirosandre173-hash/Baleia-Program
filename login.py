
import flet as ft

def main(page: ft.Page):
    # Configurações da janela
    page.title = "Tela de Login"
    page.bgcolor = "#1E3A8A"  # Define a cor de fundo solicitada
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Função que será chamada ao clicar no botão confirmar
    def confirmar_click(e):
        if not txt_nome.value or not txt_senha.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos!"))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Bem-vindo, {txt_nome.value}!"))
            page.snack_bar.open = True
        page.update()

    # Componentes da interface (estilizados em branco)
    lbl_titulo = ft.Column(
        controls=[
            ft.Image(src="loogo.png", width=150, height=150, color="#1E3A8A", margin=0),
            
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER
    )

    txt_nome = ft.TextField(
        hint_text="Usuário",
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        width=300
    )

    txt_senha = ft.TextField(
        hint_text="Senha",
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        password=True,
        can_reveal_password=True,
        width=300
    )

    btn_confirmar = ft.Button(
        "Confirmar",
        color="#1E3A8A",          # Cor do texto do botão (igual ao fundo para contraste)
        bgcolor=ft.Colors.WHITE,  # Cor de fundo do botão branca
        width=300,
        on_click=confirmar_click
    )

    # Container centralizado para organizar os elementos
    login_card = ft.Container(
        width=400,
        height=400,
        bgcolor="white",
        border_radius=15,
        shadow=ft.BoxShadow(
                        spread_radius=1, blur_radius=10, color=ft.Colors.BLACK,
                        offset=ft.Offset(0, 1),          
                    ),
        content=ft.Column(
        controls=[
            lbl_titulo,
            txt_nome,
            txt_senha,
            btn_confirmar
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    )

    # Adiciona o card de login à página
    page.add(login_card)

# Executa o aplicativo
ft.run(main)
