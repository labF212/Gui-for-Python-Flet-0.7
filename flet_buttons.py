import flet as ft

def main(page: ft.Page):
    page.title = "Como usar botões"
    page.theme_mode = ft.ThemeMode.DARK

    def save_clicked(e):
        t.value = i.value
        page.update()

    def clear_clicked(e):
        i.value = ""
        t.value = ""
        page.update()

    #put elements on the page
    title_page = ft.Text("Botões e Input Box")
    i = ft.TextField(tooltip="Introduza o texto aqui")
    save_button = ft.Button("Guardar", on_click=save_clicked,tooltip="Guarda o que está na caixa de texto",icon=ft.Icons.SAVE,icon_color="green600")
    clear_button = ft.Button("Apagar", on_click=clear_clicked,tooltip="Apaga conteúdo das caixas de texto",icon=ft.Icons.DELETE_FOREVER_ROUNDED,icon_color="pink600")
    t = ft.Text()

    button_row = ft.Row([save_button, clear_button], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    page.add(title_page, i, button_row, t)

ft.app(target=main)