import tkinter as tk
from tkinter import ttk
from tkinter import *
main = tk.Tk()
main.geometry('800x600')
print(dir(main))


def printe():
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
n = ttk.Notebook(main)
f1 = ttk.Frame(n)   # first page, which would get widgets gridded into it
f2 = ttk.Frame(n)   # second page
n.add(f1, text='One')
n.add(f2, text='Two')
n.place(relx=.1,rely=.2)

main.resizable(height=False, width=False)
main.mainloop()
