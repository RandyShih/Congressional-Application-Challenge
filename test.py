import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyB_5KHGQ94m6cu_L-kEWeYzsXxuPmrvqp4")
main = tk.Tk()
main.geometry('800x600')
print(dir(main))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def askchatGPT(text):
    response = model.generate_content(text)
    textx.delete('1.0', END)
    textx.insert('1.0', response.text)
    return response.text


def printe():
    print(askchatGPT(entry.get()))
    if entry.get() == 'rawr':
        mainFrame.pack_forget()
        mainNOFRAME.pack(fill='both', expand=True)


def switchy():
    mainNOFRAME.pack_forget()
    mainFrame.pack(fill='both', expand=True)

print('rawr')
test2 = ttk.Notebook(main)
test2.place(relx=0, rely=.1)
mainNOFRAME = ttk.Frame(test2)
button2 = tk.Button(master=mainNOFRAME, width=5, command=switchy)
button2.place(relx=.5, rely=.5)
mainFrame = tk.Frame(name='yes', master=main, width=1)
button = tk.Button(master=mainFrame, text='rawr', command=printe)
button.place(rely=.5, relx=.5, anchor='center')
entry = tk.Entry(master=mainFrame)
entry.place(rely=.55, relx=.5, anchor="center")
mainFrame.pack(fill='both', expand=True)
a = Scrollbar(master=main, orient='vertical')
a.pack(fill='y', side=RIGHT)
textx = Text(master=main, width=20, height=10, yscrollcommand=a.set)
textx.place(relx=.5, rely=.3, anchor='center')
n = ttk.Notebook(main)
f1 = ttk.Frame(n)  # first page, which would get widgets gridded into it
f2 = ttk.Frame(n)  # second page
n.add(f1, text='One')
n.add(f2, text='Two')
n.place(relx=.1, rely=.2)

main.resizable(height=False, width=False)
main.mainloop()
