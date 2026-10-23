import flet as ft
from flet_charts import MatplotlibChartWithToolbar
import matplotlib.pyplot as plt
import random
import asyncio
from datetime import datetime

# ---------------- CONFIGURAÇÕES ----------------
NUM_AMOSTRAS = 100
MAX_LINHAS_TABELA = 10
recolher_dados = True

tempos = list(range(NUM_AMOSTRAS))
temperaturas = [0] * NUM_AMOSTRAS
humidades = [0] * NUM_AMOSTRAS

# ---------------- GERADOR DE DADOS ----------------
def gerar_dados():
    temp = round(random.uniform(20, 40), 1)
    hum = round(random.uniform(20, 80), 1)
    return temp, hum

# ---------------- APP ----------------
def main(page: ft.Page):
    global recolher_dados

    page.title = "Dashboard Industrial"
    page.padding = 15
    page.theme_mode = ft.ThemeMode.DARK

    # ----------- CARDS -----------
    txt_temp = ft.Text("0.0 °C", size=28, weight="bold")
    txt_hum = ft.Text("0.0 %", size=28, weight="bold")
    txt_estado = ft.Text("INATIVO", size=22, weight="bold")

    card_height = 120
    card_width = 200

    # Card Temperatura
    card_temp = ft.Card(
        content=ft.Container(
        bgcolor="#1e3a5f",
        content=ft.Row(
            [
                #ft.Icon("alarm", color="red", size=10),
                ft.Column([txt_temp], alignment="center", spacing=5),
            ],
            alignment="center",
            spacing=10
        ),
        padding=15,
        width=card_width,
        height=card_height,
        border_radius=12,
    )
)

    # Card Humidade
    card_hum = ft.Card(
        content=ft.Container(
            bgcolor="#1b5e20",
            content=ft.Column([ft.Text("Humidade"), txt_hum],
                              alignment="center", spacing=5),
            padding=15,
            width=card_width,
            height=card_height,
            border_radius=12,
        )
    )

    # Card Estado
    card_estado = ft.Card(
        content=ft.Container(
            bgcolor="#263238",
            content=ft.Column([ft.Text("Estado"), txt_estado],
                              alignment="center", spacing=5),
            padding=15,
            width=card_width,
            height=card_height,
            border_radius=12,
        )
    )

    # ----------- GRÁFICO -----------
    fig, ax = plt.subplots()
    ax.set_xlim(0, NUM_AMOSTRAS - 1)
    ax.set_ylim(0, 100)
    ax.set_title("Temperatura e Humidade em Tempo Real")
    ax.set_xlabel("Tempo (amostras)")
    ax.set_ylabel("Valor")
    ax.grid(True, linestyle="--", alpha=0.5)

    linha_temp, = ax.plot(tempos, temperaturas, color="red", label="Temperatura (°C)")
    linha_hum, = ax.plot(tempos, humidades, color="blue", label="Humidade (%)")
    ax.legend(loc="upper center", ncol=2)
    fig.subplots_adjust(bottom=0.15)

    chart = MatplotlibChartWithToolbar(figure=fig, expand=True, height=350)

    # ----------- TABELA -----------
    tabela = ft.DataTable(
        border=ft.Border.all(1, "white"),
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Temp (°C)")),
            ft.DataColumn(ft.Text("Hum (%)")),
        ],
        rows=[],
    )

    def nova_linha(hora, t, h):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(hora)),
                ft.DataCell(ft.Text(f"{t:.1f}")),
                ft.DataCell(ft.Text(f"{h:.1f}")),
            ]
        )

    # ----------- ATUALIZAÇÃO -----------
    async def atualizar():
        while True:
            if recolher_dados:
                t, h = gerar_dados()

                temperaturas.pop(0)
                humidades.pop(0)
                temperaturas.append(t)
                humidades.append(h)

                # Atualiza gráfico
                linha_temp.set_ydata(temperaturas)
                linha_hum.set_ydata(humidades)
                chart.figure.canvas.draw_idle()

                # Atualiza cards
                txt_temp.value = f"{t:.1f} °C"
                txt_hum.value = f"{h:.1f} %"

                # Estado
                if t > 35 or h > 75:
                    txt_estado.value = "ALARME"
                    card_estado.content.bgcolor = "#b71c1c"
                elif t > 30 or h > 65:
                    txt_estado.value = "ATENÇÃO"
                    card_estado.content.bgcolor = "#f57c00"
                else:
                    txt_estado.value = "NORMAL"
                    card_estado.content.bgcolor = "#2e7d32"

                # Atualiza tabela
                hora = datetime.now().strftime("%H:%M:%S")
                tabela.rows = [nova_linha(hora, t, h)] + tabela.rows[:MAX_LINHAS_TABELA - 1]

                page.update()

            await asyncio.sleep(1)

    # ----------- CONTROLOS -----------
    async def sair_app(e):
        await page.window.close()

    def toggle(e):
        global recolher_dados
        recolher_dados = not recolher_dados
        btn_toggle.text = "Iniciar" if not recolher_dados else "Parar"
        page.update()

    btn_toggle = ft.Button("Parar/Continuar", on_click=toggle)
    btn_sair = ft.Button("Sair", on_click=sair_app)

    # ----------- LAYOUT PRINCIPAL -----------
    page.add(
        ft.Column(
            [
                ft.Row([card_temp, card_hum, card_estado],
                       alignment="center", spacing=20),
                ft.Row([ft.Container(chart, expand=2),
                        ft.Container(tabela, expand=1)],
                       spacing=20, expand=True),
                ft.Row([btn_toggle, btn_sair],
                       alignment="center", spacing=10)
            ],
            expand=True,
        )
    )

    asyncio.create_task(atualizar())

ft.run(main)
