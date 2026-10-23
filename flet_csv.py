import random
import asyncio
import flet as ft
import csv

async def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "Medição de Temperatura e Humidade"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Widgets iniciais
    txt_title = ft.Text(value="Medição de Temperatura e Humidade", text_align="center", weight="bold")
    txt_temperature = ft.Text(value="Temperatura: --°C")
    txt_humidity = ft.Text(value="Humidade: --%")

    # Adicionando widgets à página
    page.add(txt_title, txt_temperature, txt_humidity)

    # Inicializar o arquivo CSV com cabeçalho
    csv_file_path = "flet.csv"
    fieldnames = ['Temperature', 'Humidity']

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    async def update_values():
        while True:
            # Gerar valores aleatórios
            temperature = random.randint(0, 50)
            humidity = random.randint(20, 80)

            # Atualizar widgets
            txt_temperature.value = f"Temperatura: {temperature}°C"
            txt_humidity.value = f"Humidade: {humidity}%"
            page.update()  # Atualizar página sincronamente

            # Adicionar os valores ao CSV
            with open(csv_file_path, mode='a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'Temperature': temperature, 'Humidity': humidity})

            # Manter apenas as últimas 100 linhas no arquivo CSV
            with open(csv_file_path, mode='r', newline='') as csv_file:
                rows = list(csv.DictReader(csv_file))

            if len(rows) > 100:
                rows = rows[-100:]  # Pega as últimas 100 linhas
                with open(csv_file_path, mode='w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

            # Aguardar 1 segundo
            await asyncio.sleep(1)

    # Iniciar a tarefa assíncrona
    asyncio.create_task(update_values())

# Iniciar o app
ft.run(main)
