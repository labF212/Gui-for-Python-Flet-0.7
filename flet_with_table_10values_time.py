import random
import asyncio
import datetime
import flet as ft


async def main(page: ft.Page):

    page.title = "Medição de Temperatura e Humidade"

    txt = ft.Text(
        value="Medição de Temperatura e Humidade",
        text_align="CENTER",
        weight="BOLD"
    )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Temperatura")),
            ft.DataColumn(ft.Text("Humidade")),
        ],
        rows=[],
    )

    page.add(txt)
    page.add(table)

    values = []

    async def update_values():
        nonlocal values

        while True:

            now = datetime.datetime.now()

            data_atual = now.strftime("%d/%m/%Y")
            hora_atual = now.strftime("%H:%M:%S")

            temperature = random.randint(0, 50)
            humidity = random.randint(20, 80)

            values.append(
                (
                    data_atual,
                    hora_atual,
                    temperature,
                    humidity
                )
            )

            # manter apenas os últimos 10 registos
            values = values[-10:]

            rows = []

            for data, hora, temp, hum in values:

                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(data)),
                            ft.DataCell(ft.Text(hora)),
                            ft.DataCell(ft.Text(f"{temp}°C")),
                            ft.DataCell(ft.Text(f"{hum}%")),
                        ]
                    )
                )

            table.rows = rows

            page.update()

            await asyncio.sleep(1)

    asyncio.create_task(update_values())


ft.app(main)