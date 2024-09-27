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
font_test = font.Font(family='Arial', size=8, weight="bold")
style.configure('Accent.TButton', font=font_test, borderwidth=100)
style.configure('NewStyle.TButton', font=font_test, borderwidth=100)
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
# Test Code, Delete Later

#
weight_factor=1

homescreen_menu = ttk.Frame(main, padding=20, style='Card.TFrame', borderwidth=20)
homescreen_menu.grid(column=0, row=0, sticky='nsw', columnspan=6, rowspan=6)
homebutton_homescreen = ttk.Button(homescreen_menu, text='Home', style='Accent.TButton', width=20)
homebutton_homescreen.grid(column=0, row=1, pady=20)
assignmentsbutton_homescreen = ttk.Button(homescreen_menu, text='Assignments', style='Accent.TButton', width=20)
assignmentsbutton_homescreen.grid(column=0, row=2, pady=20)
classesbutton_homescreen = ttk.Button(homescreen_menu, text='Classes', style='Accent.TButton', width=20)
classesbutton_homescreen.grid(column=0, row=3, pady=20)
calanderbutton_homescreen = ttk.Button(homescreen_menu, text='Calendar', style='Accent.TButton', width=20)
calanderbutton_homescreen.grid(column=0, row=4, pady=20)
profilebutton_homescreen = ttk.Button(homescreen_menu, text='Profile', style='Accent.TButton', width=20)
profilebutton_homescreen.grid(column=0, row=5, pady=20)
settingsbutton_homescreen = ttk.Button(homescreen_menu, text='Settings', style='Accent.TButton', width=20)
settingsbutton_homescreen.grid(column=0, row=6, pady=20)
mainscreen_homescreen = ttk.Frame(main, style='Card.TFrame', borderwidth=10)
mainscreen_homescreen.grid(row=0, column=2, sticky='nsew', columnspan=6, rowspan=6)
main.resizable(height=False, width=False)
main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(2, weight=1)
mainscreen_homescreen.propagate(False)
ignore_text = Text(master=mainscreen_homescreen, width=100, height=20, borderwidth=20, background='gray',
                   font=font_test, state='disabled')
ignore_text.grid(row=0, column=5, sticky='n', pady=20, columnspan=1, rowspan=1)
textinput_homescreen = ttk.Entry(master=mainscreen_homescreen, width=30)
askaibutton_homescreen = ttk.Button(mainscreen_homescreen, style='Accent.TButton', text='Ask AI!',
                                    command=lambda: getChatGPTInput(textinput_homescreen.get(), ignore_text))
textinput_homescreen.grid(column=5, row=1, pady=10, sticky='nsew', rowspan=1, columnspan=1)
askaibutton_homescreen.grid(column=5, row=2, pady=10, sticky='nsew', columnspan=1, rowspan=1)
# Grid configuration
mainscreen_homescreen.grid_rowconfigure(0, weight=1)
mainscreen_homescreen.grid_rowconfigure(1, weight=1)
mainscreen_homescreen.grid_rowconfigure(2, weight=1)
mainscreen_homescreen.grid_rowconfigure(3, weight=1)
mainscreen_homescreen.grid_rowconfigure(4, weight=1)
mainscreen_homescreen.grid_rowconfigure(5, weight=5)
mainscreen_homescreen.grid_rowconfigure(6, weight=1)
mainscreen_homescreen.grid_rowconfigure(7, weight=1)
mainscreen_homescreen.grid_rowconfigure(8, weight=1)
mainscreen_homescreen.grid_rowconfigure(9, weight=1)
mainscreen_homescreen.grid_columnconfigure(0, weight=1)
mainscreen_homescreen.grid_columnconfigure(1, weight=1)
mainscreen_homescreen.grid_columnconfigure(2, weight=1)
mainscreen_homescreen.grid_columnconfigure(3, weight=1)
mainscreen_homescreen.grid_columnconfigure(4, weight=1)
mainscreen_homescreen.grid_columnconfigure(5, weight=5)
mainscreen_homescreen.grid_columnconfigure(6, weight=1)
mainscreen_homescreen.grid_columnconfigure(7, weight=1)
mainscreen_homescreen.grid_columnconfigure(8, weight=1)
mainscreen_homescreen.grid_columnconfigure(9, weight=1)

main.grid_rowconfigure(0, weight=weight_factor)
main.grid_rowconfigure(1, weight=weight_factor)
main.grid_rowconfigure(2, weight=weight_factor)
main.grid_rowconfigure(3, weight=weight_factor)
main.grid_rowconfigure(4, weight=weight_factor)
main.grid_columnconfigure(0, weight=weight_factor)
main.grid_columnconfigure(1, weight=weight_factor)
main.grid_columnconfigure(2, weight=weight_factor)
main.grid_columnconfigure(3, weight=weight_factor)
main.grid_columnconfigure(4, weight=weight_factor)

main.mainloop()
