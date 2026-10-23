import flet as ft
import flet_charts as fch
import random
from datetime import datetime
import asyncio

MAX_POINTS = 20  # mostrar até 20 pontos no gráfico

def main(page: ft.Page):
    page.title = "Temperatura e Humidade com LineChart"

    # duas séries de dados:
    temp_series = fch.LineChartData(
        color=ft.Colors.RED,
        stroke_width=2,
        points=[],
    )
    hum_series = fch.LineChartData(
        color=ft.Colors.BLUE,
        stroke_width=2,
        points=[],
    )

    line_chart = fch.LineChart(
        data_series=[temp_series, hum_series],
        min_y=0,
        max_y=100,
        expand=True,
        left_axis=fch.ChartAxis(title=ft.Text("Valor")),
        bottom_axis=fch.ChartAxis(title=ft.Text("Tempo (s)")),
    )

    page.add(line_chart)

    async def update_chart():
        t = 0
        while True:
            now = datetime.now().strftime("%H:%M:%S")

            # cria um ponto (x=t, y=valor)
            temp = random.uniform(0, 40)
            hum = random.uniform(20, 80)

            temp_series.points.append(fch.LineChartDataPoint(t, temp))
            hum_series.points.append(fch.LineChartDataPoint(t, hum))

            # manter apenas últimos MAX_POINTS
            if len(temp_series.points) > MAX_POINTS:
                temp_series.points.pop(0)
                hum_series.points.pop(0)

            # atualiza a escala do eixo X
            line_chart.min_x = t - MAX_POINTS + 1
            line_chart.max_x = t

            line_chart.update()
            t += 1
            await asyncio.sleep(0.5)

    asyncio.get_event_loop().create_task(update_chart())

if __name__ == "__main__":
    ft.run(main)
