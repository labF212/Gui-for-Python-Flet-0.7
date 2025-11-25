import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import random
import asyncio
from datetime import datetime

num_amostras = 100
max_valores_tabela = 10
recolher_dados = True
num_amostra = 0

def gerar_dados():
    temperatura = random.uniform(20, 25)
    humidade = random.uniform(20, 80)
    return temperatura, humidade

tempos = list(range(num_amostras))
temperaturas = [0] * num_amostras
humidades = [0] * num_amostras


async def main(page: ft.Page):
    global recolher_dados, num_amostra, temperaturas, humidades

    page.title = "Gráfico e Tabela de Dados"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    fig, ax = plt.subplots()
    ax.set_xlim(0, num_amostras - 1)
    ax.set_ylim(0, 110)
    ax.set_title("Temperatura e Humidade em Tempo Real\n")
    ax.set_xlabel("Tempo (amostras)")
    ax.set_ylabel("Valor")

    linha_temperatura, = ax.plot(tempos, temperaturas, label="Temperatura (°C)", color='red')
    linha_humidade, = ax.plot(tempos, humidades, label="Humidade (%)", color='blue')
    ax.grid(axis='y', color='lightgrey', linestyle='--', linewidth=0.7)
    ax.set_yticks(range(0, 101, 10))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=2)

    chart = MatplotlibChart(fig, expand=True)

    tabela_estilizada = ft.DataTable(
        bgcolor="yellow",
        border=ft.border.all(2, "red"),
        vertical_lines=ft.border.BorderSide(3, "blue"),
        horizontal_lines=ft.border.BorderSide(1, "green"),
        border_radius=10,
        heading_row_color="#d95f0e",
        heading_text_style=ft.TextStyle(color="white", weight="bold"),
        columns=[
            ft.DataColumn(ft.Text("Hora", color="black")),
            ft.DataColumn(ft.Text("Temperatura (°C)", color="black")),
            ft.DataColumn(ft.Text("Humidade (%)", color="black")),
        ],
        rows=[],
    )

    def adicionar_linha(hora, temperatura, humidade, indice):
        cor_linha = "#fec44f" if indice % 2 == 0 else "#fff7bc"
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(hora)),
                ft.DataCell(ft.Text(f"{temperatura:.2f}°C")),
                ft.DataCell(ft.Text(f"{humidade:.2f}%")),
            ],
            color=cor_linha,
        )

    async def atualizar_dados():
        global temperaturas, humidades, recolher_dados, num_amostra

        while True:
            if recolher_dados:
                num_amostra += 1
                nova_temp, nova_hum = gerar_dados()

                temperaturas.pop(0)
                humidades.pop(0)
                temperaturas.append(nova_temp)
                humidades.append(nova_hum)

                # atualizar gráfico
                linha_temperatura.set_ydata(temperaturas)
                linha_humidade.set_ydata(humidades)
                chart.figure.canvas.draw()

                agora = datetime.now()
                hora_atual = agora.strftime("%H:%M:%S")

                tabela_estilizada.rows.insert(
                    0,
                    adicionar_linha(hora_atual, nova_temp, nova_hum, len(tabela_estilizada.rows)),
                )

                if len(tabela_estilizada.rows) > max_valores_tabela:
                    tabela_estilizada.rows.pop()

                # corrigir cores
                for i, row in enumerate(tabela_estilizada.rows):
                    row.color = "#fec44f" if i % 2 == 0 else "#fff7bc"

                page.update()

            await asyncio.sleep(1)

    def alternar_recolha(e):
        global recolher_dados
        recolher_dados = not recolher_dados
        botao_parar_iniciar.text = "Iniciar" if not recolher_dados else "Parar"
        botao_parar_iniciar.update()

    def sair_app(e):
        page.window.close()

    botao_parar_iniciar = ft.ElevatedButton(
        text="Parar",
        on_click=alternar_recolha,
    )
    botao_sair = ft.ElevatedButton(
        text="Sair",
        on_click=sair_app,
    )

    conteudo_principal = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Medição de Temperatura e Humidade", weight="BOLD", size=20),
                    ft.Container(chart, expand=True, height=400),
                ],
                expand=1,
            ),
            ft.Column(
                [
                    ft.Text("Tabela de Dados", weight="BOLD", size=18),
                    tabela_estilizada,
                ],
            ),
        ],
        expand=True,
    )

    page.add(
        ft.Column(
            [conteudo_principal, ft.Row([botao_parar_iniciar, botao_sair], alignment="center")],
            expand=True,
        )
    )

    asyncio.create_task(atualizar_dados())


ft.app(main)
