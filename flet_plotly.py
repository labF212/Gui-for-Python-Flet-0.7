import flet as ft
import flet_charts as fch
import plotly.graph_objects as go
import random
from datetime import datetime
import asyncio

def main(page: ft.Page):
    page.title = "Temperatura e Humidade em Tempo Real"
    
    # Cria a figura Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", name="Temperatura (°C)"))
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", name="Humidade (%)"))  # Aqui mudamos para H maiúsculo
    fig.update_layout(
        title="Temperatura e Humidade em Tempo Real",
        xaxis_title="Hora",
        yaxis=dict(title="Temperatura / Humidade", range=[0, 100])
    )
    
    chart = fch.PlotlyChart(figure=fig, expand=True)
    page.add(chart)

    async def update_chart():
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            temp = random.uniform(0, 40)
            humidity = random.uniform(20, 80)
            
            # Adiciona novos dados
            fig.data[0].x += (now,)
            fig.data[0].y += (temp,)
            fig.data[1].x += (now,)
            fig.data[1].y += (humidity,)
            
            # Mantém apenas os últimos 20 pontos
            for trace in fig.data:
                trace.x = trace.x[-20:]
                trace.y = trace.y[-20:]
            
            chart.update()  # Atualiza só o gráfico
            await asyncio.sleep(2)

    asyncio.get_event_loop().create_task(update_chart())

if __name__ == "__main__":
    ft.run(main)
