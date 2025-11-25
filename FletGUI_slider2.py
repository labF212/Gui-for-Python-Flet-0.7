import flet as ft
import time

def main(page: ft.Page):
    page.title = "Manual and Automatic Slider"
    
    page.window_width = 200
    page.window_height = 200
    #page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    
    slider1_value = 0
    slider2_value = 0
    
    def slider_changed(e):
        nonlocal slider1_value, slider2_value
        if e.control == slider1:
            slider1_value = int(e.control.value)
            pwm_label2.value = f"{slider1_value} PWD"
        elif e.control == slider2:
            slider2_value = int(e.control.value)
            pwm_label4.value = f"{slider2_value} PWD"
        page.update()
    
        
    def radiogroup_changed(e):  # Receive the selected value directly
        if e.control.value == "Manual":
            slider1.visible = True
            slider2.visible = True
            #pwm_label1.visible = True
            #pwm_label2.visible = True
            #print("Manual")
        else:
            slider1.visible = False
            slider2.visible = False
            #pwm_label1.visible = True
            #pwm_label2.visible = True
            #print("Automatic")
            
            # Fading up and down...
            for i in range(255):
                if e.control.value == "Manual":
                    pwm_label2.value = "0 PWD"
                    pwm_label4.value = "0 PWD"
                    page.update()
                    break
                time.sleep(.5)
                pwm_label2.value = f"{i} PWD"
                pwm_label4.value = f"{255-i} PWD"
                page.update()
                
            for i in range(255):
                if e.control.value == "Manual":
                    pwm_label2.value = "0 PWD"
                    pwm_label4.value = "0 PWD"
                    page.update()
                    break
                time.sleep(.5)
                pwm_label2.value = f"{255-i} PWD"
                pwm_label4.value = f"{i} PWD"
                page.update()
            
    def exit_app(_):
         page.window.close()


    #Building Interface
    
    pwm_label1 = ft.Text("LED in pin 6")
    pwm_label2 = ft.Text("0 PWD", expand=True, text_align=ft.TextAlign.END)

    row1 = ft.Row([
        pwm_label1,
        pwm_label2
    ])

    pwm_label3 = ft.Text("LED in pin 5")
    pwm_label4 = ft.Text("0 PWD",expand=True, text_align=ft.TextAlign.END)

    slider1 = ft.Slider(value=0, min=0, max=254, on_change=slider_changed)

    row2 = ft.Row([
        pwm_label3,
        pwm_label4
    ])

    slider2 = ft.Slider(value=0, min=0, max=254, on_change=slider_changed)
    
    button_exit = ft.ElevatedButton("Exit", icon=ft.Icons.EXIT_TO_APP, on_click=exit_app)
    button_center = ft.Row([button_exit], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    cg = ft.RadioGroup(
        value="Manual",
        content=ft.Row([
            ft.Radio(value="Manual", label="Manual"),  
            ft.Radio(value="Automatic", label="Automatic"),
        ]),
        on_change=radiogroup_changed
    )

    row3 = ft.Row([
        ft.Text("Work mode:"),
        cg 
    ])
    
    page.add(
        row1,
        slider1,
        row2,
        slider2,
        row3,
        button_center
    )



ft.app(target=main)
