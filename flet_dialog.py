import flet as ft
import asyncio

def criar_dialog(page):
    """Cria o diálogo apenas uma vez e retorna ele."""
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

    link_buttons = ft.Row(
        controls=[
            ft.TextButton(
    "Documentação do Flet",
    tooltip="Abrir documentação oficial",
    style=ft.ButtonStyle(
        text_style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    ),
    on_click=lambda e: asyncio.create_task(abrir_url("https://flet.dev/docs/")),
)

        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Informações"),
        content=ft.Column([markdown_content, link_buttons], tight=True),
        actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(page, dialog))],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return dialog

def abrir_dialog(page, dialog):
    if dialog not in page.overlay:
        page.overlay.append(dialog)
    dialog.open = True
    page.update()

def fechar_dialog(page, dialog):
    dialog.open = False
    page.update()


def main(page: ft.Page):
    page.title = "Exemplo simples"
    page.theme_mode = ft.ThemeMode.DARK

    dialog_info = criar_dialog(page)

    # Botões
    sobre_btn = ft.TextButton("Sobre", on_click=lambda e: abrir_dialog(page, dialog_info))
    ajuda_btn = ft.TextButton("Ajuda", on_click=lambda e: abrir_dialog(page, dialog_info))
    sair_btn = ft.Button("Sair", on_click=lambda e: asyncio.create_task(fechar_app(page)))

    page.add(
        ft.Row([sobre_btn, ajuda_btn, sair_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    )

async def fechar_app(page):
    await page.window.destroy()

# Função async para abrir URL
async def abrir_url(url):
    launcher = ft.UrlLauncher()
    await launcher.launch_url(url)

if __name__ == "__main__":
    ft.run(main)
