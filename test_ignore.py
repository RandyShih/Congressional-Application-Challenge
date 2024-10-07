import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import json as json
from tkinter import messagebox

increase_value = 0

try:
    import google.generativeai as genai
    import os
except:
    print("google.generativeai import failed!")

# Google API Configuration
try:
    genai.configure(api_key="AIzaSyB_5KHGQ94m6cu_L-kEWeYzsXxuPmrvqp4")
    Model = genai.GenerativeModel(model_name="gemini-1.5-flash")
except:
    print("google.generativeai configuration failed!")
main = tk.Tk()
main.geometry('1200x800')
main.title('Organize Now!')
style = ttk.Style()
# Main Style Configuration
main.tk.call('source', 'theme/azure.tcl')
style.theme_use('azure-dark')
print(style.theme_names())
font_test = font.Font(family='Georgia')
user = None
style.configure("Custom.TButton")
style.element_create("custom", 'from', 'default')
style.layout("Custom.TButton", [('custom.button', {'children': [('customButton.button',
                               {'sticky': 'nswe',
                                'children':
                                    [('customButton.padding',
                                      {'sticky': 'nswe',
                                       'children':
                                           [('customButton.label',
                                             {'expand': '1', 'sticky': 'nswe'}
                                             )
                                            ]
                                       }
                                      )
                                     ]
                                }
                               )
                              ]})]

)
style.configure('Custom.TButton', background='#292828', borderwidth=2, relief='SUNKEN')
style.map('Custom.TButton', background=[('active', '#595858')])
print(font)

class createclass:
        def __init__(self, width, height, column, row):
            self.width = width
            self.height = height
            self.column = column
            self.row = row
            self.label = ttk.Label(master=classScreen, width=self.width, style='Card.TFrame')
            self.label.grid(column=self.column, row=self.row, sticky='ew', columnspan=1, pady=10)

def recallclasses():
    with open('user_data.json') as sp:
        userdata = json.load(sp)
        print(user)
        print(userdata)
        print(userdata[user]['Class'])
        return userdata[user]['Class']
def index(username):
    usernamefound = False
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        for i in userdata:
            if username == i['Username']:
                usernameindex = userdata.index(i)
                usernamefound = True
    if usernamefound == True:
        return usernameindex
    else:
        return "Invalid Username, data not found."
def hideallscreensexcept():
    mainscreen_homescreen.grid_forget()
def changeclassesscreen():
    classScreen.grid(row=0, column=2, sticky='nsew', columnspan=8, rowspan=10)
    recallclasses()
    classNUM = 0
    for i in recallclasses():
        classNUM += 1
        createclass(column=3, row=classNUM, width=10, height=10)
    hideallscreensexcept()

def askchatGPT(text, textbox):
    response = Model.generate_content(text)
    textbox.configure(state='normal')
    textbox.delete('1.0', END)
    textbox.insert('1.0', response.text)
    textbox.configure(state='disabled')


def changeloginscreentext(message):
    errorlogin_loginmenu["text"] = message


def login():
    username = usernameentry_loginmenu.get()
    password = passwordentry_loginmenu.get()
    with open("user_data.json", 'r') as sp:
        userdata = json.load(sp)
        try:
            userpassword = userdata[index(username)]['Password']
            if userpassword == password:
                changeloginscreentext("Successfully logged in!")
                login_menu.grid_forget()
                global user
                user = index(username)
            else:
                changeloginscreentext("Wrong password!")
        except:
            changeloginscreentext("Invalid username!")


def getChatGPTInput(text, textbox):
    try:
        print(askchatGPT(text, textbox))
    except:
        print('Function getChatGPTInput error!')


def changescreen_signupscreen():
    signupscreen.grid(column=0, row=0, sticky='NSEW', columnspan=50, rowspan=50)

# Test Code, Delete Later
#
weight_factor = 1
# Home Screen
homescreen_menu = ttk.Frame(main, padding=20, style='Card.TFrame', borderwidth=20, height=2222)
homebutton_homescreen = ttk.Button(homescreen_menu, text='Home', style='Accent.TButton', width=20)
assignmentsbutton_homescreen = ttk.Button(homescreen_menu, text='Assignments', style='Custom.TButton', width=20, command=changeclassesscreen)
classesbutton_homescreen = ttk.Button(homescreen_menu, text='Classes', style='Accent.TButton', width=20)
calanderbutton_homescreen = ttk.Button(homescreen_menu, text='Calendar', style='Accent.TButton', width=20)
profilebutton_homescreen = ttk.Button(homescreen_menu, text='Profile', style='Accent.TButton', width=20)
settingsbutton_homescreen = ttk.Button(homescreen_menu, text='Settings', style='Accent.TButton', width=20)
mainscreen_homescreen = ttk.Frame(main, style='Card.TFrame', borderwidth=10, height=100)
mainscreen_homescreen.grid(row=0, column=2, sticky='nsew', columnspan=8, rowspan=10)
ignore_text = Text(master=mainscreen_homescreen, width=50, height=20, borderwidth=20, background='gray',
                   font=font_test, state='disabled')
textinput_homescreen = ttk.Entry(master=mainscreen_homescreen, width=30)
askaibutton_homescreen = ttk.Button(master=mainscreen_homescreen, style='Accent.TButton', text='Ask AI!',
                                    command=lambda: getChatGPTInput(textinput_homescreen.get(), ignore_text))
settingsbutton_homescreen.grid(column=0, row=6, pady=20)
homebutton_homescreen.grid(column=0, row=1, pady=20)
profilebutton_homescreen.grid(column=0, row=5, pady=20)
calanderbutton_homescreen.grid(column=0, row=4, pady=20)
classesbutton_homescreen.grid(column=0, row=3, pady=20)
assignmentsbutton_homescreen.grid(column=0, row=2, pady=20)
homescreen_menu.grid(column=0, row=0, sticky='nsew', columnspan=2, rowspan=10)
homescreen_menu.grid_propagate(0)

# Main Screen Grid configuration
mainscreen_homescreen.grid_propagate(0)
for i in range(0, 6):
    mainscreen_homescreen.grid_columnconfigure(i, weight=weight_factor)
    mainscreen_homescreen.grid_rowconfigure(i, weight=weight_factor)
scrollbar = ttk.Scrollbar(master=mainscreen_homescreen, orient="vertical")

# Main Grid Configuration
for i in range(0, 10):
    main.grid_rowconfigure(i, weight=weight_factor)
    main.grid_columnconfigure(i, weight=weight_factor)
main.resizable(height=True, width=True)

# Login Menu Configuration
login_menu = ttk.Frame(main, style='Card.TFrame')
login_menu.grid(column=0, row=0, sticky='NSEW', columnspan=10, rowspan=10)
for i in range(0, 50):
    login_menu.columnconfigure(i, weight=weight_factor)
    login_menu.rowconfigure(i, weight=weight_factor)
login_menu.columnconfigure(25, weight=1)

# Sign Up Screen Configuration
signupscreen = ttk.Frame(master=main, style="Card.TFrame")
for i in range(0, 50):
    signupscreen.rowconfigure(i, weight=weight_factor)
    signupscreen.columnconfigure(i, weight=weight_factor)
signupscreen.columnconfigure(25, weight=5)
image = tk.PhotoImage(file="R.png", master=login_menu)

# Login Screen Widgets
passwordentry_loginmenu = ttk.Entry(login_menu, width=25, foreground='white', font=('Georgia', 8))
print(passwordentry_loginmenu.winfo_class())
usernameentry_loginmenu = ttk.Entry(login_menu, width=25, foreground='white', font=('Georgia', 8))
loginbutton_loginmenu = ttk.Button(login_menu, text='Login', command=login, style='Accent.TButton', width=40)
errorlogin_loginmenu = Label(login_menu, width=40, text='Please enter your username and password', bg='#333333',
                             fg='red', font=("Georgia", 8))
signupbutton_loginmenu = ttk.Button(login_menu, text='Sign up', style='Accent.TButton', width=40,
                                    command=changescreen_signupscreen)
passwordlabel_loginmenu = ttk.Label(master=login_menu, text='Password: ', font=('Georgia', 10), background='#333333', foreground='white')
usernamelabel_loginmenu = ttk.Label(master=login_menu, text='Username: ', font=('Georgia', 10), background='#333333', foreground='white')
label_login = ttk.Label(master=login_menu, image=image, background='#333333')
passwordentry_loginmenu.grid(column=25, row=20, sticky='e')
usernameentry_loginmenu.grid(column=25, row=19, sticky='e')
usernamelabel_loginmenu.grid(column=25, row=19, sticky='w')
passwordlabel_loginmenu.grid(column=25, row=20, sticky='w')
loginbutton_loginmenu.grid(column=25, row=22)
errorlogin_loginmenu.grid(column=25, row=21)
signupbutton_loginmenu.grid(column=25, row=23)
label_login.grid(column=25, row=18)

# Sign Up Screen Widgets
passwordentry_signupscreen = ttk.Entry(master=signupscreen, foreground='white', width=30)
passwordentry_signupscreen.grid(column=25, row=20, sticky='e')
usernameentry_signupscreen = ttk.Entry(master=signupscreen, foreground='white', width=30)
usernameentry_signupscreen.grid(column=25, row=19, pady=5, sticky='e')
signupbutton_signupscreen = ttk.Button(master=signupscreen, style='Accent.TButton', text='Sign up')
signupbutton_signupscreen.grid(column=25, row=21, sticky='ew', pady=5)
label = ttk.Label(master=signupscreen, image=image, width=12, background='#333333')
label.grid(column=25, row=18)
passwordlabel_signupscreen = ttk.Label(master=signupscreen, text='Password:', font=font_test, background='#333333',
                                       foreground='white', width=8)
passwordlabel_signupscreen.grid(column=25, row=20, sticky='w', padx=5)
usernamelabel_signupscreen = ttk.Label(master=signupscreen, text='Username: ', font=font_test, background='#333333',
                                       foreground='white', width=8)
usernamelabel_signupscreen.grid(column=25, row=19, sticky='w', padx=5)

# Classes Screen
classScreen = ttk.Frame(master=main, style='Card.TFrame')
AddClassEntry_Classes = ttk.Entry(master=classScreen, width=5)
AddClassEntry_Classes.grid(row=0, column=0)
# Classes Screen Configuration
for i in range(0, 6):
    classScreen.columnconfigure(i, weight=weight_factor)
    classScreen.rowconfigure(i, weight=weight_factor)
classScreen.grid_propagate(0)
main.mainloop()
