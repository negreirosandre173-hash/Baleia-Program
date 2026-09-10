import flet as ft
from janela3 import janel3


def main(page: ft.Page):
    page.window_full_screen = True
    page.padding = 0
    
    

    
    page.add(janel3())
ft.app(target=main)
