import flet as ft

def main(page: ft.Page):
    page.title = "Controlo de Relé"
    page.theme_mode = ft.ThemeMode.DARK

    # Funções
    def ligar_rele(e):
        led_icon.color = "green"
        page.update()

    def desligar_rele(e):
        led_icon.color = "red"
        page.update()

    # Título
    title = ft.Text("Controlo de Relé", size=24, weight=ft.FontWeight.BOLD)

    # Labels
    entradas_label = ft.Text("Entradas", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    saidas_label = ft.Text("Saídas", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # LED
    led_icon = ft.Icon(ft.Icons.CIRCLE, color="red", size=60)
    led_label = ft.Text("Relé 1", size=14, color="black")

    led_container = ft.Container(
        content=ft.Column(
            [led_icon, led_label],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=10,
        bgcolor="yellow",
        border_radius=8,
        width=120,
        height=100,
        alignment=ft.alignment.Alignment(0, 0)  # centraliza horizontal e vertical
    )

    # Botões
    ligar_button = ft.Button(
        "Ligar Relé",
        on_click=ligar_rele,
        icon=ft.Icons.POWER,
        icon_color="green600",
        tooltip="Liga o relé"
    )

    desligar_button = ft.Button(
        "Desligar Relé",
        on_click=desligar_rele,
        icon=ft.Icons.POWER_OFF,
        icon_color="red600",
        tooltip="Desliga o relé"
    )

    buttons_container = ft.Container(
        content=ft.Row(
            [ligar_button, desligar_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        padding=10,
        bgcolor="yellow",
        border_radius=8,
        width=350,
        height=100,
        alignment=ft.alignment.Alignment(0, 0)  # centraliza horizontal e vertical
    )

    entradas_column = ft.Column(
        [entradas_label, buttons_container],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    saidas_column = ft.Column(
        [saidas_label, led_container],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    control_row = ft.Row(
        [entradas_column, saidas_column],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(title, control_row)

ft.run(main)
