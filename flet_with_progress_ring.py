import random
import asyncio
import flet as ft

async def main(page: ft.Page):
    page.title = "Medição de Temperatura e Humidade"

    # Title
    txt = ft.Text("Medição de Temperatura e Humidade", text_align="CENTER", weight="BOLD")

    # Progress Ring – Temperatura
    txt_temp = ft.Text("Temperatura")

    pr_temp_value = ft.Text("0°C", size=20)

    pr_temp_container = ft.Container(
        content=pr_temp_value,
        width=50,
        height=50,
        alignment=ft.alignment.center,
        bgcolor="white",
        border_radius=50,
    )

    pr_temp = ft.ProgressRing(
        width=70,
        height=70,
        stroke_width=10,
        color="red",
        value=0.0,
    )

    # Progress Ring – Humidade
    txt_hum = ft.Text("Humidade")

    pr_hum_value = ft.Text("0%", size=20)

    pr_hum_container = ft.Container(
        content=pr_hum_value,
        width=50,
        height=50,
        alignment=ft.alignment.center,
        bgcolor="white",
        border_radius=50,
    )

    pr_hum = ft.ProgressRing(
        width=70,
        height=70,
        stroke_width=10,
        color="blue",
        value=0.0,
    )

    # Tables
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Temperatura")),
            ft.DataColumn(ft.Text("Humidade")),
        ],
        rows=[],
    )

    # --- LAYOUT ORGANIZADO ---

    # Linha com os dois progress rings
    rings_row = ft.Row(
        [
            ft.Column([txt_temp, pr_temp, pr_temp_container], alignment="center"),
            ft.Column([txt_hum, pr_hum, pr_hum_container], alignment="center"),
        ],
        alignment="center",
    )

    # Adicionar tudo à página
    page.add(
        ft.Row([txt], alignment="center"),
        rings_row,
        ft.Row([table], alignment="center")
    )

    # ----------------------------------------

    values = []

    async def update_values():
        nonlocal values

        while True:
            temperature = random.randint(0, 50)
            humidity = random.randint(20, 80)

            values.append((temperature, humidity))
            values = values[-5:]

            # update table
            table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{t}°C")),
                        ft.DataCell(ft.Text(f"{h}%")),
                    ]
                )
                for t, h in values
            ]

            # update progress rings
            pr_temp_value.value = f"{temperature}°C"
            pr_hum_value.value = f"{humidity}%"

            pr_temp.value = temperature / 100
            pr_hum.value = humidity / 100

            page.update()
            await asyncio.sleep(1)

    asyncio.create_task(update_values())

ft.app(target=main)
