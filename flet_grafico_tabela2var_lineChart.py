import flet as ft
import flet_charts as fch
import random
import asyncio
from datetime import datetime

MAX_POINTS = 20
max_valores_tabela = 10
recolher_dados = True

def gerar_dados():
    temperatura =  int(random.uniform(20, 25))
    humidade    =  int(random.uniform(20, 80))
    return temperatura, humidade

def main(page: ft.Page):
    global recolher_dados

    page.title = "Gráfico e Tabela de Dados"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- Indicador de status ---
    status_text = ft.Text("🟢 Em execução", size=16, weight="bold")

    # --- LineChart ---
    temp_series = fch.LineChartData(color=ft.Colors.RED, stroke_width=2, points=[])
    hum_series = fch.LineChartData(color=ft.Colors.BLUE, stroke_width=2, points=[])

    line_chart = fch.LineChart(
        data_series=[temp_series, hum_series],
        min_y=0,
        max_y=110,
        min_x=0,
        max_x=MAX_POINTS - 1,
        expand=True,
        left_axis=fch.ChartAxis(
            title=ft.Text("Valor"),
            label_size=10,
            show_labels=True,
        ),
        bottom_axis=fch.ChartAxis(
            title=ft.Text("Tempo (s)"),
            label_size=10,
            show_labels=True,
            #label_interval=5,
        ),
    )

    grafico_com_espaco = ft.Container(
        content=line_chart,
        padding=ft.padding.only(left=20),
    )

    # --- Tabela ---
    tabela_estilizada = ft.DataTable(
        bgcolor="yellow",
        border=ft.border.all(2, "red"),
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
                ft.DataCell(ft.Text(f"{temperatura}°C")),
                ft.DataCell(ft.Text(f"{humidade}%")),
            ],
            color=cor_linha,
        )

    # --- Função assíncrona para atualizar dados ---
    async def atualizar_dados():
        t = 0
        while True:
            if recolher_dados:
                temp, hum = gerar_dados()

                # Adiciona pontos no gráfico
                temp_series.points.append(fch.LineChartDataPoint(t, temp))
                hum_series.points.append(fch.LineChartDataPoint(t, hum))

                # Mantém apenas últimos MAX_POINTS
                if len(temp_series.points) > MAX_POINTS:
                    temp_series.points.pop(0)
                    hum_series.points.pop(0)

                # Atualiza limites do eixo X
                line_chart.min_x = max(0, t - MAX_POINTS + 1)
                line_chart.max_x = t
                #line_chart.bottom_axis.labels = [f"{p.x}s" for p in temp_series.points]

                # Labels no eixo X a cada 5 segundos
                line_chart.bottom_axis.labels = [
                    fch.ChartAxisLabel(
                        value=p.x,
                        label=ft.Text(f"{int(p.x)}")
                    )
                    for p in temp_series.points
                    if p.x % 5 == 0
                ]


                line_chart.update()

                # Atualiza tabela
                hora_atual = datetime.now().strftime("%H:%M:%S")
                tabela_estilizada.rows.insert(
                    0,
                    adicionar_linha(hora_atual, temp, hum, len(tabela_estilizada.rows)),
                )
                if len(tabela_estilizada.rows) > max_valores_tabela:
                    tabela_estilizada.rows.pop()

                page.update()
                t += 1

            await asyncio.sleep(1)  # Atualiza a cada 1s

    # --- Botões ---
    def alternar_recolha(e):
        global recolher_dados
        recolher_dados = not recolher_dados

        # Atualiza botão e indicador
        botao_parar.text = "Continuar" if not recolher_dados else "Parar"
        status_text.value = "🟢 Em execução" if recolher_dados else "⏸ Parado"
        page.update()

    async def sair_app(e):
        await page.window.close()

    # Criando os botões
    botao_parar = ft.Button("Parar/Continuar", on_click=alternar_recolha, tooltip="Parar/Continuar")
    botao_sair = ft.Button("Sair", on_click=sair_app, tooltip="Sair do Programa")

    # --- Layout ---
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Medição de Temperatura e Humidade", size=20, weight="bold"),
                                status_text,            # Indicador de status
                                grafico_com_espaco,
                            ],
                            expand=1,
                        ),
                        ft.Column(
                            [
                                ft.Text("Tabela de Dados", size=18, weight="bold"),
                                tabela_estilizada,
                            ],
                        ),
                    ],
                    expand=True,
                    spacing=20,
                ),
                ft.Row([botao_parar, botao_sair], alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=True,
        )
    )

    # --- Inicia atualização assíncrona ---
    asyncio.create_task(atualizar_dados())

# Executa o app
ft.run(main)
