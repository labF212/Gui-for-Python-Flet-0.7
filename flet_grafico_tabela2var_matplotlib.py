import flet as ft
from flet_charts import MatplotlibChartWithToolbar
import matplotlib.pyplot as plt
import random
import asyncio
from datetime import datetime

num_amostras = 100
max_valores_tabela = 10
recolher_dados = True

tempos = list(range(num_amostras))
temperaturas = [0] * num_amostras
humidades = [0] * num_amostras


def gerar_dados():
    temperatura = random.uniform(20, 25)
    humidade = random.uniform(20, 80)
    return temperatura, humidade


def main(page: ft.Page):
    global recolher_dados

    page.title = "Gráfico e Tabela de Dados"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- Configurar gráfico ---
    fig, ax = plt.subplots()
    ax.set_xlim(0, num_amostras - 1)
    ax.set_ylim(0, 110)
    ax.set_title("Temperatura e Humidade em Tempo Real")
    ax.set_xlabel("Tempo (amostras)")
    ax.set_ylabel("Valor")
    ax.grid(axis="y", color="lightgrey", linestyle="--", linewidth=0.7)

    linha_temperatura, = ax.plot(tempos, temperaturas, label="Temperatura (°C)", color="red")
    linha_humidade, = ax.plot(tempos, humidades, label="Humidade (%)", color="blue")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=2)

    chart = MatplotlibChartWithToolbar(figure=fig, expand=True, height=400)


    # --- Configurar tabela ---
    tabela_estilizada = ft.DataTable(
        bgcolor="yellow",
        border=ft.Border.all(2, "red"),
        vertical_lines=ft.border.BorderSide(3, "blue"),
        horizontal_lines=ft.border.BorderSide(1, "green"),
        border_radius=10,
        heading_row_color="#d95f0e",
        heading_text_style=ft.TextStyle(color="white", weight="bold"),
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Temperatura (°C)")),
            ft.DataColumn(ft.Text("Humidade (%)")),
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

    # --- Função async para atualizar dados ---
    async def atualizar_dados():
        while True:
            if recolher_dados:
                nova_temp, nova_hum = gerar_dados()

                temperaturas.pop(0)
                humidades.pop(0)
                temperaturas.append(nova_temp)
                humidades.append(nova_hum)

                # 🔹 ATUALIZA APENAS OS DADOS DAS LINHAS
                linha_temperatura.set_ydata(temperaturas)
                linha_humidade.set_ydata(humidades)

                # Redesenho eficiente
                chart.figure.canvas.draw_idle()

                # Atualiza tabela
                agora = datetime.now()
                hora_atual = agora.strftime("%H:%M:%S")
                tabela_estilizada.rows.insert(
                    0,
                    adicionar_linha(
                        hora_atual,
                        nova_temp,
                        nova_hum,
                        len(tabela_estilizada.rows),
                    ),
                )
                if len(tabela_estilizada.rows) > max_valores_tabela:
                    tabela_estilizada.rows.pop()

                page.update()

            await asyncio.sleep(1,0)


    # --- Funções dos botões ---
    def alternar_recolha(e):
        global recolher_dados
        recolher_dados = not recolher_dados
        botao_parar_iniciar.text = "Iniciar" if not recolher_dados else "Parar"
        botao_parar_iniciar.update()

    async def sair_app(e):
        await page.window.close()

    # --- Botões ---
    botao_parar_iniciar = ft.Button("Parar/Continuar", on_click=alternar_recolha)
    botao_sair = ft.Button("Sair", on_click=sair_app)

    # --- Layout principal ---
    conteudo_principal = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Medição de Temperatura e Humidade", weight="bold", size=20),
                    chart,
                ],
                expand=1,
            ),
            ft.Column(
                [
                    ft.Text("Tabela de Dados", weight="bold", size=18),
                    tabela_estilizada,
                ]
            ),
        ],
        expand=True,
        spacing=20,
    )

    page.add(
        ft.Column(
            [
                conteudo_principal,
                ft.Row([botao_parar_iniciar, botao_sair], alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=True,
        )
    )

    asyncio.create_task(atualizar_dados())


ft.run(main)
