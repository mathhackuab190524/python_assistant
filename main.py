
import flet as ft
import tkinter as tk
from Model import *
from functions import *
from audio_record import *

window_width = 400
window_height = 500

api_key = "**********OPENAI_API_KEY**********"

llm = llm

system_prompt = """You are an assistant whose task is to help the user programming in Python. You can only be asked questions 
about Python. If the user doesn't ask you anything about Python, just tell him who you are 
and ask him if he has any doubts, don't do anything alse. This applies when the user says you hello, asks who you are or simply
asks anything not realted with Python.
If the user does ask something about Python, you will act as an expert 
Python developer who is able to provide detailed solutions, advice and clear explanations of complex programming issues. 
Provide a code answering the question or solving the issue the user might have when needed.
You should respond in a concise and professional manner. The format of your answer should be directly an answer, 
it must never contain the words 'AI', 'System' or similar and never try to finish the user query if it is unfinished."""

conversation = [
    ("system", system_prompt)
]

root = tk.Tk()
screen_width = root.winfo_screenwidth()

def main(page: ft.Page):
    """
    Initializes and configures the main application page.

    This function sets up the main application window, configures its dimensions, theme, and other properties.
    It also initializes the user interface components, such as the file picker, buttons, text field, and 
    interaction row. Finally, it updates the page with the initialized components.

    Parameters:
    page (ft.Page): The main application page.
    """

    #Window settings
    page.window_width = window_width 
    page.window_height = window_height
    page.window_min_height = window_height
    page.window_min_width = window_width
    page.theme_mode = ft.ThemeMode.DARK
    page.window_always_on_top = True
    page.window_left = screen_width - page.window_width
    
    #Main window User Interface

    column = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.ALWAYS,
        auto_scroll= True,
        width = screen_width * 3 / 5
    )

    #File Selecting Management

    def pick_files_result(e: ft.FilePickerResultEvent):
        """
        Handles the result of the file picker dialog.

        This function updates the select file button text based on the selected file.
        It also enables various UI elements and updates the interaction row's opacity.

        Parameters:
        e (ft.FilePickerResultEvent): The event object containing the result of the file picker dialog.
        """
        print(select_file_button.text)
        if e.files:
            select_file_button.text = (e.files[0]).path
        else:
            select_file_button.text = "¡Cancelado!"
        print(select_file_button.text)

        select_file_button.update()

        list.content = column
        list.update()
        list.alignment = ft.alignment.top_center
        list.update()

        text_field.disabled = False
        text_field.update() 

        button1.disabled = False
        button1.update()

        button2.disabled = False
        button2.update()

        interaction_row.opacity = 1
        interaction_row.update()



    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    
    #Initial Page User Interface
    def button_clicked(e):
        """
        Handles the click event of the select file button.

        This function opens the file picker dialog to allow the user to select a file.

        Parameters:
        e: The event object.
        """
        pick_files_dialog.pick_files(allow_multiple=False)


    select_file_button_height = 30
    select_file_button_width = 137
    select_file_button = ft.ElevatedButton(
        "Select File", 
        width=select_file_button_width, 
        height=select_file_button_height, 
        on_click=button_clicked,
        color = ft.colors.WHITE,
        icon_color = ft.colors.GREEN,
        icon= ft.icons.UPLOAD_FILE
    )

    list = ft.Container(
        content = select_file_button,
        expand = True,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        border_radius=10,
    )

    def update_icon(e):
        """
        Updates the icon of button2 based on the text field's value.

        If the text field has content, the icon is set to SEND_ROUNDED. Otherwise, it is set to LIGHTBULB.

        Parameters:
        e: The event object.
        """
        if text_field.value.strip():
            button2.icon = ft.icons.SEND_ROUNDED

        else:
            button2.icon = ft.icons.LIGHTBULB
        button2.update()

    def audio(e):
        """
        Handles the click event of the audio button.

        This function adds a new audio input element to the column, processes the code,
        generates an answer, and updates the UI accordingly.

        Parameters:
        e: The event object.
        """
        new_element = audio_input()
        #Sends a message from the user
        if new_element.strip(): 
            alignment = ft.MainAxisAlignment.END
            column.controls.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(new_element),
                            bgcolor=ft.colors.GREEN,
                            border_radius=5,
                            padding=10,
                            width=window_width - 100, 
                        )
                    ],
                    alignment=alignment 
                )
            )
            column.update() 
            text_field.value = ""
            button2.icon = ft.icons.LIGHTBULB 

        code = read_file(select_file_button.text)
        answer = generate_answer(conversation, new_element, code)

        #Adds a message from the assistant
        alignment = ft.MainAxisAlignment.START
        column.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(answer),
                        bgcolor=ft.colors.GREEN,
                        border_radius=5,
                        padding=10,
                        width=window_width - 100, 
                    )
                ],
                alignment=alignment 
            )
        )
        column.update() 
        page.update()

    def add_new_element(e):
        """
        Handles the click event of the add new element button.

        This function adds a new text input element to the column, processes the code,
        generates an answer, and updates the UI accordingly.

        Parameters:
        e: The event object.
        """
        new_element = text_field.value
        text_field.value = ""
        page.update()
        #Sends a message from the user
        if new_element.strip(): 
            alignment = ft.MainAxisAlignment.END
            column.controls.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(new_element),
                            bgcolor=ft.colors.GREEN,
                            border_radius=5,
                            padding=10,
                            width=window_width - 100, 
                        )
                    ],
                    alignment=alignment 
                )
            )
            column.update() 
            button2.icon = ft.icons.LIGHTBULB 

        code = read_file(select_file_button.text)
        answer = generate_answer(conversation, new_element, code)
        
        #Sends a message from the assistant
        alignment = ft.MainAxisAlignment.START
        column.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(answer),
                        bgcolor=ft.colors.GREEN,
                        border_radius=5,
                        padding=10,
                        width=window_width - 100, 
                    )
                ],
                alignment=alignment 
            )
        )
        column.update() 
        page.update()


    #User Interface
    text_field = ft.TextField(
        hint_text="Ask me a question",  
        bgcolor=ft.colors.GREEN,        
        color=ft.colors.WHITE,    
        expand = True,
        on_change= update_icon,
        content_padding=10,
        on_submit=add_new_element,
        disabled = True 
    )

    button1 = ft.IconButton(on_click=audio,
                            icon = ft.icons.MULTITRACK_AUDIO,
                            icon_color = ft.colors.GREEN,
                            disabled=True 
                            )
    
    button2 = ft.IconButton(on_click=add_new_element,
                            icon = ft.icons.LIGHTBULB,
                            icon_color = ft.colors.GREEN,
                            disabled = True 
    )

    interaction_row = ft.Row(
        controls=[button1, text_field, button2],
        height= 33,
        expand = True,
        alignment = ft.MainAxisAlignment.CENTER,
        opacity=0.4##
    )   

    page.add(list, ft.Container(
        content = interaction_row,
        height = 40,
        alignment= ft.alignment.center,
    ))
        
    page.add(list)
    page.update()
    

ft.app(target=main)

