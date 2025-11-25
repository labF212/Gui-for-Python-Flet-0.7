import random
import asyncio
import flet as ft

async def main(page: ft.Page):
    # Set page title
    page.title = "Medição de Temperatura e Humidade"
    
    # Create title text widget
    txt = ft.Text(value="Medição de Temperatura e Humidade",text_align="CENTER",weight="BOLD")
    #txt.alignment = ft.MainAxisAlignment.CENTER
    
    # Create temperature text widget
    txt_temperature = ft.Text(value="Temperatura: --°C")

    # Create humidity text widget
    txt_humidity = ft.Text(value="Humidade: --%")

    # Add widgets to page
    page.add(txt)
    page.add(txt_temperature)
    page.add(txt_humidity)

    # Update widgets with initial values
    temperature = random.randint(0, 50)
    humidity = random.randint(20, 80)
    txt_temperature.value = f"Temperatura: {temperature}°C"
    txt_humidity.value = f"Humidade: {humidity}%"

    async def update_values():
        while True:
            # Generate random temperature and humidity values
            temperature = random.randint(0, 50)
            humidity = random.randint(20, 80)

            
            # Update the text widgets
            txt_temperature.value = f"Temperatura: {temperature}°C"
            txt_humidity.value = f"Humidade: {humidity}%"

            # Update the page with the new values
            page.update()

            # Sleep for 1 second
            await asyncio.sleep(1)

    # Start updating the values
    asyncio.create_task(update_values())

ft.app(main)
