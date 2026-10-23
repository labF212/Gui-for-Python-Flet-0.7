import random
import asyncio
import flet as ft
import csv


async def main(page: ft.Page):
    page.title = "Gravação de dados para ficheiro"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------------- UI ELEMENTS ----------------
    title = ft.Text("Medição de Temperatura e Humidade", weight="bold")

    txt_temperature = ft.Text("Temperatura: --°C")
    txt_humidity = ft.Text("Humidade: --%")

    # PROGRESS BAR (0 → 100)
    progress = ft.ProgressBar(width=300, value=0)

    start_button = ft.Button(
        "Save",
        icon=ft.Icons.SAVE,
        icon_color="green600"
    )

    stop_button = ft.Button(
        "Stop",
        disabled=True,
        icon=ft.Icons.STOP,
        icon_color="pink600"
    )

    buttons = ft.Row([start_button, stop_button], alignment="center")

    page.add(
        title,
        txt_temperature,
        txt_humidity,
        ft.Text("Progresso da gravação:"),
        progress,
        buttons
    )

    # ---------------- STATE ----------------
    running = False

    # ---------------- LOOP ASSÍNCRONO ----------------
    async def record_loop():
        nonlocal running

        # Reset progress bar
        progress.value = 0
        page.update()

        # cria CSV e escreve header
        with open("flet.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Temperature", "Humidity"])
            writer.writeheader()

        count = 0

        while running:
            temp = random.randint(0, 50)
            hum = random.randint(20, 80)

            # UI update
            txt_temperature.value = f"Temperatura: {temp}°C"
            txt_humidity.value = f"Humidade: {hum}%"

            # update progress bar
            progress.value = count / 100
            page.update()

            # write csv
            with open("flet.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["Temperature", "Humidity"])
                writer.writerow({"Temperature": temp, "Humidity": hum})

            count += 1
            if count >= 100:
                running = False

            await asyncio.sleep(1)

        # cleanup: limit to 100 rows
        with open("flet.csv", "r") as f:
            rows = list(csv.DictReader(f))

        rows = rows[-100:]

        with open("flet.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Temperature", "Humidity"])
            writer.writeheader()
            writer.writerows(rows)

        # FINALIZAÇÃO
        progress.value = 1
        stop_button.disabled = True
        start_button.disabled = False
        page.update()

    # ---------------- EVENT HANDLERS ----------------

    def start_clicked(e):
        nonlocal running
        running = True
        start_button.disabled = True
        stop_button.disabled = False
        page.update()

        page.run_task(record_loop)

    def stop_clicked(e):
        nonlocal running
        running = False

    start_button.on_click = start_clicked
    stop_button.on_click = stop_clicked


ft.run(main)
