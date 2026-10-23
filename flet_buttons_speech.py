import flet as ft
import pyttsx3

def main(page: ft.Page):
    page.title = "Como usar botões"
    page.theme_mode = ft.ThemeMode.DARK

    engine = pyttsx3.init()

    # procurar voz portuguesa
    voices = engine.getProperty('voices')
    for voice in voices:
        if "portuguese" in voice.name.lower() or "pt" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 150)  # velocidade da fala

    def save_clicked(e):
        t.value = i.value
        page.update()

    def clear_clicked(e):
        i.value = ""
        t.value = ""
        page.update()

    def read_text(e):
        if t.value != "":
            engine.say(t.value)
            engine.runAndWait()

    # elementos da página
    title_page = ft.Text("Botões e Input Box")

    i = ft.TextField(tooltip="Introduza o texto aqui")

    save_button = ft.Button(
        "Guardar",
        on_click=save_clicked,
        tooltip="Guarda o que está na caixa de texto",
        icon=ft.Icons.SAVE,
        icon_color="green600"
    )

    read_button = ft.Button(
        "Ler",
        on_click=read_text,
        tooltip="Ler o texto em voz alta",
        icon=ft.Icons.RECORD_VOICE_OVER,  # ícone mais adequado
        icon_color="blue600"
    )

    clear_button = ft.Button(
        "Apagar",
        on_click=clear_clicked,
        tooltip="Apaga conteúdo da caixa de texto",
        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
        icon_color="pink600"
    )

    t = ft.Text()

    button_row = ft.Row(
        [save_button, read_button, clear_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    page.add(title_page, i, button_row, t)

ft.app(target=main)