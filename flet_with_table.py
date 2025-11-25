import random
import asyncio
import flet as ft

async def main(page: ft.Page):
    # Set page title
    page.title = "Medição de Temperatura e Humidade"

    # Create title text widget
    txt = ft.Text(value="Medição de Temperatura e Humidade", text_align="CENTER", weight="BOLD")

    # Create DataTable widget with temperature and humidity columns
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Temperatura")),
            ft.DataColumn(ft.Text("Humidade")),
        ],
        rows=[],
    )

    # Add widgets to page
    page.add(txt)
    page.add(table)

    # List to store last 10 temperature and humidity values
    values = []

    async def update_values():
        nonlocal values

        while True:
            # Generate random temperature and humidity values
            temperature = random.randint(0, 50)
            humidity = random.randint(20, 80)

            # Add new value to the list
            values.append((temperature, humidity))

            # Keep only the last 10 values
            values = values[-10:]

            # Update the table with the last 10 values
            rows = []
            for temp, hum in values:
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{temp}°C")),
                        ft.DataCell(ft.Text(f"{hum}%")),
                    ],
                )
                rows.append(row)
            table.rows = rows

            # Update the page with the new values
            page.update()

            # Sleep for 1 second
            await asyncio.sleep(1)

    # Start updating the values
    asyncio.create_task(update_values())

ft.app(main)