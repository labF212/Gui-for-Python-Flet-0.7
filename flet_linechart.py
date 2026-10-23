import flet as ft
import flet_charts as fch
import random

def main(page: ft.Page):
    page.title = "Gráfico Temperatura e Humidade"
    page.padding = 20
    page.bgcolor = "#E0E0E0"  # fundo da página

    # Dados iniciais
    horas = list(range(24))
    temperatura = [random.uniform(5, 40) for _ in horas]   # 5ºC a 40ºC
    humidade = [random.uniform(20, 80) for _ in horas]     # 20% a 80%

    # Legenda manual
    legenda = ft.Row([
        ft.Container(ft.Text("Temperatura (°C)", color="red"), padding=5),
        ft.Container(ft.Text("Humidade (%)", color="blue"), padding=5)
    ], spacing=20)

    # Cria séries de dados (sem 'name')
    series = [
        fch.LineChartData(
            color="red",
            points=[fch.LineChartDataPoint(x=h, y=t) for h, t in zip(horas, temperatura)],
        ),
        fch.LineChartData(
            color="blue",
            points=[fch.LineChartDataPoint(x=h, y=u) for h, u in zip(horas, humidade)],
        )
    ]

    chart = fch.LineChart(
        data_series=series,
        bgcolor="#FFFFFF",  # fundo do gráfico
        expand=True,
        min_x=0,
        max_x=23,
        min_y=0,
        max_y=100  # eixo Y cobrindo os valores possíveis
    )

    # Função para atualizar dados aleatórios
    def atualizar_dados(e):
        nonlocal horas, temperatura, humidade
        novas_horas = horas[-1] + 1
        horas.append(novas_horas)
        temperatura.append(random.uniform(5, 40))
        humidade.append(random.uniform(20, 80))

        # Mantém apenas os últimos 24 pontos
        horas = horas[-24:]
        temperatura = temperatura[-24:]
        humidade = humidade[-24:]

        chart.data_series = [
            fch.LineChartData(
                color="red",
                points=[fch.LineChartDataPoint(x=h, y=t) for h, t in zip(horas, temperatura)],
            ),
            fch.LineChartData(
                color="blue",
                points=[fch.LineChartDataPoint(x=h, y=u) for h, u in zip(horas, humidade)],
            )
        ]
        chart.update()

    # Botão para atualizar dados
    btn = ft.Button("Atualizar dados aleatórios", on_click=atualizar_dados)

    # Layout
    page.add(
        legenda,  # legenda manual
        chart,
        ft.Row([btn], alignment="center", height=50)
    )

ft.app(target=main)
