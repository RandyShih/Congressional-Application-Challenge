import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import google.generativeai as genai
import os

# Google API Configuration
genai.configure(api_key="AIzaSyB_5KHGQ94m6cu_L-kEWeYzsXxuPmrvqp4")
Model = genai.GenerativeModel(model_name="gemini-1.5-flash")

main = tk.Tk()
main.geometry('1200x800')
main.title('Organize Now!')
style = ttk.Style()
main.tk.call('source', 'theme/azure.tcl')
print(style.theme_names())
style.theme_use('azure-dark')
print(list(font.families()))
font_test = font.Font(family='Courier', size=8, weight="bold")
style.configure('TButton', font=font_test)
style.configure('Card.TFrame', background='blue')


def askchatGPT(text, textbox):
    response = Model.generate_content(text)
    textbox.configure(state='normal')
    textbox.delete('1.0', END)
    textbox.insert('1.0', response.text)
    textbox.configure(state='disabled')


def getChatGPTInput(text, textbox):
    try:
        print(askchatGPT(text, textbox))
    except:
        print('Function getChatGPTInput error!')


homescreen_menu = ttk.Frame(main, padding=20, style='Card.TFrame')
homescreen_menu.grid(column=0, row=0, sticky='nsw')
homebutton_homescreen = ttk.Button(homescreen_menu, text='Home', style='Accent.TButton', width=10)
homebutton_homescreen.grid(column=0, row=1, pady=20)
assignmentsbutton_homescreen = ttk.Button(homescreen_menu, text='Assignents', style='Accent.TButton', width=10)
assignmentsbutton_homescreen.grid(column=0, row=2, pady=20)
classesbutton_homescreen = ttk.Button(homescreen_menu, text='Classes', style='Accent.TButton', width=10)
classesbutton_homescreen.grid(column=0, row=3, pady=20)
calanderbutton_homescreen = ttk.Button(homescreen_menu, text='Calander', style='Accent.TButton', width=10)
calanderbutton_homescreen.grid(column=0, row=4, pady=20)
profilebutton_homescreen = ttk.Button(homescreen_menu, text='Profile', style='Accent.TButton', width=10)
profilebutton_homescreen.grid(column=0, row=5, pady=20)
settingsbutton_homescreen = ttk.Button(homescreen_menu, text='Settings', style='Accent.TButton', width=10)
settingsbutton_homescreen.grid(column=0, row=6, pady=20)
mainscreen_homescreen = ttk.Frame(main, style='Card.TFrame')
mainscreen_homescreen.grid(row=0, column=2, sticky='nsew')
main.resizable(height=False, width=False)
main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(2, weight=1)
mainscreen_homescreen.propagate(False)
ignore_text = Text(master=mainscreen_homescreen, width=100, height=20, borderwidth=20, background='gray',
                   font=font_test, state='disabled')
ignore_text.grid(row=1, column=0, sticky='n', pady=20)
textinput_homescreen = ttk.Entry(master=mainscreen_homescreen, width=30)
mainscreen_homescreen.grid_rowconfigure(0, weight=1)
mainscreen_homescreen.grid_columnconfigure(0, weight=1)
askaibutton_homescreen = ttk.Button(mainscreen_homescreen, style='Accent.TButton', text='Ask AI!',
                                    command=lambda: getChatGPTInput(textinput_homescreen.get(), ignore_text))
mainscreen_homescreen.grid_rowconfigure(3, weight=1)
mainscreen_homescreen.grid_rowconfigure(4, weight=1)
mainscreen_homescreen.grid_rowconfigure(5, weight=1)
mainscreen_homescreen.grid_rowconfigure(6, weight=1)
mainscreen_homescreen.grid_rowconfigure(7, weight=1)
mainscreen_homescreen.grid_rowconfigure(8, weight=1)
mainscreen_homescreen.grid_rowconfigure(9, weight=1)
mainscreen_homescreen.grid_rowconfigure(10, weight=15)
textinput_homescreen.grid(column=0, row=2, pady=5, sticky='n')
askaibutton_homescreen.grid(column=0, row=3, pady=10, sticky='n')

main.mainloop()
