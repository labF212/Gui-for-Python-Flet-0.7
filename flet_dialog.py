import flet as ft

def sobre_e_ajuda(page):
    # Conteúdo em Markdown
    markdown_content = ft.Markdown(
        """
# Sobre e Ajuda

Este programa é um exemplo simples com Flet.

### Autor
- **Nome:** Paulo Galvão  
- **Versão:** 1.0  

### Como utilizar
- Clique em **Sobre** ou **Ajuda** para ver este texto.
        """,
        extension_set="gitHub",
        selectable=True,
    )

    # Botões de links
    link_buttons = ft.Row(
        controls=[
            ft.TextButton(
                text="Documentação do Flet",
                tooltip="Abrir documentação oficial",
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                ),
                on_click=lambda e: page.launch_url("https://flet.dev/docs/"),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Criar dialog
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Informações"),
        content=ft.Column([markdown_content, link_buttons], tight=True),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    if dialog not in page.overlay:
        page.overlay.append(dialog)
    dialog.open = True
    page.update()


def close_dialog(page, dialog):
    dialog.open = False
    page.update()


def main(page: ft.Page):
    page.title = "Exemplo simples"
    page.theme_mode = ft.ThemeMode.DARK

    # Botões
    sobre_btn = ft.ElevatedButton("Sobre", on_click=lambda e: sobre_e_ajuda(page))
    ajuda_btn = ft.ElevatedButton("Ajuda", on_click=lambda e: sobre_e_ajuda(page))
    sair_btn = ft.ElevatedButton(
        "Sair",
        on_click=lambda e: page.window.close(),  # FECHA a janela corretamente
    )

    # Adiciona os botões à página
    page.add(ft.Row([sobre_btn, ajuda_btn, sair_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20))


if __name__ == "__main__":
    ft.app(target=main)
