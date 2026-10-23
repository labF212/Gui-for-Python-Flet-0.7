import flet as ft

def main(page: ft.Page):
    page.title = "Manual Slider"

    slider1_value = 0
    slider2_value = 0

    def slider_changed(e):
        nonlocal slider1_value, slider2_value
        if e.control == slider1:
            slider1_value = int(e.control.value)
            pwm_label2.value = f"{slider1_value} PWM"
        elif e.control == slider2:
            slider2_value = int(e.control.value)
            pwm_label4.value = f"{slider2_value} PWM"
        page.update()
        
    # ----------------------------
    # Botão sair
    # ----------------------------
    async def on_exit(e):
        #board.shutdown()
        await page.window.destroy()

    pwm_label1 = ft.Text("LED in pin 6")
    pwm_label2 = ft.Text(expand=True,text_align=ft.TextAlign.END)

    row1 = ft.Row([
        pwm_label1,
        pwm_label2
    ])

    pwm_label3 = ft.Text("LED in pin 5")
    pwm_label4 = ft.Text(expand=True,text_align=ft.TextAlign.END)

    slider1 = ft.Slider(value=0, min=0, max=254, on_change=slider_changed)

    row2 = ft.Row([
        pwm_label3,
        pwm_label4
    ])

    slider2 = ft.Slider(value=0, min=0, max=254, on_change=slider_changed)
    
    button_exit= ft.Button("Exit", icon=ft.Icons.EXIT_TO_APP, on_click=on_exit)
    button_center = ft.Row([button_exit], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    page.add(
        row1,
        slider1,
        row2,
        slider2,
        button_center
    )

# Cleanup ao fechar a janela
    def on_window_close(e):
        board.shutdown()
    page.on_window_close = on_window_close

# ----------------------------
# EXECUÇÃO
# ----------------------------
if __name__ == "__main__":
    ft.run(main)
