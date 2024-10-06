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
print(font)
image2 = tk.PhotoImage(file='dog.png')
style.configure('Test1.TButton', font=('Georgia', 10), width=20, borderwidth=5, border='white', background='blue')
style.element_create('Custom', 'from', 'default')
style.layout('Test1.TButton', [('CustomButton.button', {'sticky': 'nswe', 'children': [('CustomButton.padding', {'sticky': 'nswe', 'children': [('CustomButton.label', {'expand': '1', 'sticky': 'nswe'})]})]})]
)
style.map('Test1.TButton', image=[('active', image2)])
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
    login_menu.grid_forget()
    signupscreen.grid(column=0, row=0, sticky='NSEW', columnspan=50, rowspan=50)


# Test Code, Delete Later

#
weight_factor = 1

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
ignore_text = Text(master=mainscreen_homescreen, width=100, height=20, borderwidth=20, background='gray',
                   font=font_test, state='disabled')
ignore_text.grid(row=0, column=5, sticky='n', pady=20, columnspan=1, rowspan=1)
textinput_homescreen = ttk.Entry(master=mainscreen_homescreen, width=30)
askaibutton_homescreen = ttk.Button(mainscreen_homescreen, style='Accent.TButton', text='Ask AI!',
                                    command=lambda: getChatGPTInput(textinput_homescreen.get(), ignore_text))
textinput_homescreen.grid(column=5, row=1, pady=10, sticky='nsew', rowspan=1, columnspan=1)
askaibutton_homescreen.grid(column=5, row=2, pady=10, sticky='nsew', columnspan=1, rowspan=1)
# Main Screen Grid configuration
for i in range(0, 10):
    mainscreen_homescreen.grid_columnconfigure(i, weight=weight_factor)
    mainscreen_homescreen.grid_rowconfigure(i, weight=weight_factor)
mainscreen_homescreen.propagate(False)

# Main Grid Configuration
for i in range(0, 5):
    main.grid_rowconfigure(i, weight=weight_factor)
    main.grid_columnconfigure(i, weight=weight_factor)
main.resizable(height=False, width=False)

# Login Menu Configuration
login_menu = ttk.Frame(main, style='Card.TFrame')
login_menu.grid(column=0, row=0, sticky='NSEW', columnspan=5, rowspan=5)
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
loginbutton_loginmenu = ttk.Button(login_menu, text='Login', command=login, style='Test1.TButton')
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
main.mainloop()
