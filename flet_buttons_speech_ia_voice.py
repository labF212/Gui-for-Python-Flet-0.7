import flet as ft
import subprocess

VOICE_MODEL = "voices/pt_PT-tugao-medium.onnx"

def speak(text):
    #command = f'echo "{text}" | piper --model {VOICE_MODEL} --output-raw | aplay -r 22050 -f S16_LE -t raw -'
    command = f'echo "{text}" | piper --model {VOICE_MODEL} --length-scale 1.5 --output-raw | aplay -r 22050 -f S16_LE -t raw -'
    subprocess.run(command, shell=True)

def main(page: ft.Page):
    page.title = "Leitor IA"
    page.theme_mode = ft.ThemeMode.DARK

    def save_clicked(e):
        t.value = i.value
        page.update()

    def clear_clicked(e):
        i.value = ""
        t.value = ""
        page.update()

    def read_text(e):
        if t.value != "":
            speak(t.value)

    title_page = ft.Text("Leitor com IA (Português PT)")

    i = ft.TextField(label="Introduza o texto")

    save_button = ft.Button(
        "Guardar",
        on_click=save_clicked,
        icon=ft.Icons.SAVE,
        tooltip="Guarda o que está na caixa de texto",
        icon_color="green600"
    )

    read_button = ft.Button(
        "Ler",
        on_click=read_text,
        icon=ft.Icons.RECORD_VOICE_OVER,
        tooltip="Ler o texto em voz alta",
        icon_color="blue600"
    )

    clear_button = ft.Button(
        "Apagar",
        on_click=clear_clicked,
        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
        tooltip="Apaga conteúdo da caixa de texto",
        icon_color="pink600"
    )

    t = ft.Text()

    page.add(
        title_page,
        i,
        ft.Row([save_button, read_button, clear_button]),
        t
    )

ft.run(main)