import flet as ft

def main(page: ft.Page):
    page.title = "Controlo de Relés"
    page.theme_mode = ft.ThemeMode.DARK

    def ligar_rele(led_icon):
        led_icon.color = "green"
        page.update()

    def desligar_rele(led_icon):
        led_icon.color = "red"
        page.update()

    title = ft.Text("Controlo de Relés", size=24, weight=ft.FontWeight.BOLD)

    def create_rele_controls(rele_number):
        # LED
        led_icon = ft.Icon(ft.Icons.CIRCLE, color="red", size=60)
        led_label = ft.Text(f"Relé {rele_number}", size=14, color="black")

        led_container = ft.Container(
            content=ft.Column(
                [led_icon, led_label],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            bgcolor="yellow",
            border_radius=8,
            width=120,
            height=100,
            alignment=ft.Alignment.CENTER,
        )

        # Botões (SEM ElevatedButton)
        ligar_button = ft.Button(
            f"Ligar Relé {rele_number}",
            icon=ft.Icons.POWER,
            on_click=lambda e: ligar_rele(led_icon),
        )

        desligar_button = ft.Button(
            f"Desligar Relé {rele_number}",
            icon=ft.Icons.POWER_OFF,
            on_click=lambda e: desligar_rele(led_icon),
        )

        buttons_container = ft.Container(
            content=ft.Row(
                [ligar_button, desligar_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=10,
            bgcolor="yellow",
            border_radius=8,
            width=350,
            height=100,
            alignment=ft.Alignment.CENTER,
        )

        return ft.Row(
            [buttons_container, led_container],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

    page.add(
        title,
        ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                        "Entradas",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.Alignment.CENTER,
                    width=350,
                ),
                ft.Container(
                    content=ft.Text(
                        "Saídas",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.Alignment.CENTER,
                    width=120,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        create_rele_controls(1),
        create_rele_controls(2),
        create_rele_controls(3),
        create_rele_controls(4),
    )

ft.run(main)
