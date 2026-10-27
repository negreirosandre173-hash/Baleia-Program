import flet as ft

def main(page: ft.Page):
    # Registrando a fonte
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"
    }

    # Aplicando a fonte globalmente em todo o app (opcional)
    page.theme = ft.Theme(font_family="Kanit")

    # Aplicando a fonte em um texto específico
    texto_personalizado = ft.Text(
        value="Olá, Flet!",
        font_family="Kanit",
        size=30
    )

    page.add(texto_personalizado)

ft.run(main)
