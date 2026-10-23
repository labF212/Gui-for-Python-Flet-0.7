import flet as ft

def main(page: ft.Page):
    page.title = "Como utilizar botões"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # -------- ELEMENTOS VISUAIS --------
    title_page = ft.Text(
        "Botões e Input Box",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    input_text = ft.TextField(
        width=300,
        label="Introduza texto"
    )

    output_text = ft.Text()

    # -------- DIÁLOGOS --------
    def close_alert(e):
        alert_dialog.open = False
        page.update()

    def close_help(e):
        help_dialog.open = False
        page.update()

    alert_dialog = ft.AlertDialog(
        title=ft.Text("Caixa de texto vazia"),
        content=ft.Text("Introduza dados na caixa primeiro."),
        actions=[
            ft.Button("OK", on_click=close_alert)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    help_dialog = ft.AlertDialog(
        title=ft.Text("Como usar", weight=ft.FontWeight.BOLD),
        content=ft.Row(
            [
                ft.Icon(
                    ft.Icons.QUESTION_MARK_OUTLINED,
                    size=60,
                    color=ft.Colors.PINK
                ),
                ft.Column(
                    [
                        ft.Text("• Escreva algo na caixa de texto."),
                        ft.Text("• Clique em Guardar para mostrar."),
                        ft.Text("• Clique em Apagar para limpar."),
                    ],
                    tight=True
                ),
            ],
            spacing=20
        ),
        actions=[
            ft.Button("OK", on_click=close_help)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # depois de criar alert_dialog e help_dialog
    page.overlay.extend([alert_dialog, help_dialog])


    # -------- FUNÇÕES --------
    def save_clicked(e):
        if not input_text.value.strip():
            alert_dialog.open = True
            page.update()
            return

        output_text.value = input_text.value
        page.update()

    def clear_clicked(e):
        input_text.value = ""
        output_text.value = ""
        page.update()

    def help_clicked(e):
        help_dialog.open = True
        page.update()

    # -------- BOTÕES (API MODERNA) --------
    save_button = ft.Button(
        "Guardar",
        icon=ft.Icons.SAVE,
        tooltip="Guarda o texto",
        on_click=save_clicked
    )

    clear_button = ft.Button(
        "Apagar",
        icon=ft.Icons.DELETE_FOREVER,
        tooltip="Apaga o texto",
        on_click=clear_clicked
    )

    help_button = ft.Button(
        "Ajuda",
        icon=ft.Icons.HELP_OUTLINE,
        tooltip="Mostra ajuda",
        on_click=help_clicked
    )

    # -------- LAYOUT --------
    page.add(
        title_page,
        input_text,
        ft.Row(
            [save_button, clear_button, help_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12
        ),
        output_text
    )

ft.run(main)
