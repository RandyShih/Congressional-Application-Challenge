import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import json as json
import time as time
from tkinter import messagebox

increase_value = 0
classesScreenValue = 1
classFrameNum = 0
weight_factor = 1

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
classesScreenDict = {}
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
        def __init__(self, width, height, column, row, master, text):
            self.width = width
            self.height = height
            self.column = column
            self.row = row
            self.frame = ttk.Frame(master=master, width=self.width, style='Card.TFrame', height=self.height)
            self.frame.grid(column=self.column, row=self.row, pady=40, sticky='nsew', columnspan=3)
            self.label = ttk.Label(master=self.frame, text=text, background='#333333', foreground='white', font=("Georgia", 12))
            self.label.grid(column=0, row=0, padx=5, pady=5)
            print(recallassignmentdetails('Math', timedue=True))
            print(f'Created the class {text}!')

class createclassScreen:
    def __init__(self, master):
        global classFrameNum
        self.master = master
        self.frame = ttk.Frame(master=master, style="Card.TFrame")
        self.frame.grid(column=0, row=0, sticky="NSEW", columnspan=6, rowspan=6)
        self.leftbutton = ttk.Button(master=self.frame, width=10, command=testcmd, text='Left')
        self.rightbutton = ttk.Button(master=self.frame, width=10, command=testcmd, text='Right')
        for i in range(0,6):
            self.frame.rowconfigure(i, weight=weight_factor)
            self.frame.columnconfigure(i, weight=weight_factor)
        self.leftbutton.grid(column=2, row=5, sticky='s', pady=20)
        self.rightbutton.grid(column=3, row=5, sticky='s', pady=20)
        classFrameNum += 1
        if classFrameNum != 1:
            self.frame.grid_forget()
        classesScreenDict.update({classFrameNum: self.frame})
def loading():
    progressionBar.step(0)
    loadingscreen.grid(column=0, row=0, columnspan=10, rowspan=10, sticky='nsew')
    progressionBar.place(rely=.5, relx=.5, anchor=CENTER)

def loadingcomplete():
    loadingscreen.grid_forget()
    progressionBar.step(0)

def recallassignmentdetails(classes, timedue=False, datedue=False, shortdescription=False, notes=False, period=False):
    with open("user_data.json", 'r')  as sp:
        userdata = json.load(sp)
        counter = 0
        for classesIndex in userdata[user]['Classes']:
            assignmentInformationDict = {

            }
            if classes == classesIndex:
                assignmentInformationDict.pop("Assignment Index", counter)
                if timedue:
                    assignmentInformationDict.pop("Time Due", userdata[user]['TimeDue'])
                if datedue:
                    assignmentInformationDict.pop("Time Due", userdata[user]['TimeDue'])
                if shortdescription:
                    assignmentInformationDict.pop("Time Due", userdata[user]['TimeDue'])
                if notes:
                    assignmentInformationDict.pop("Time Due", userdata[user]['TimeDue'])
                if period:
                    assignmentInformationDict.pop("Time Due", userdata[user]['TimeDue'])
                counter += 1
                return assignmentInformationDict

def recallclasses():
    with open('user_data.json') as sp:
        userdata = json.load(sp)
        return userdata[user]['Classes']
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
def testcmd():
    global classesScreenValue
    global classesScreenDict
    for i, v in classesScreenDict:
        print('e')

def signup():
    username = usernameentry_signupscreen.get()
    password = passwordentry_signupscreen.get()
    print(username)
    with (open('user_data.json', 'r+') as sp):
        userdata = json.load(sp)
        print(userdata)
        for accounts in userdata:
            if username == accounts['Username']:
                errormessage_signupscreen['text'] = f'The username {username} already exists!'
                return
        for i in username:
            if i.isspace():
                errormessage_signupscreen['text'] = 'Username cannot contain spaces!'
                return
        for i in password:
            if i.isspace():
                errormessage_signupscreen['text'] = "Password cannot contain spaces!"
                return
        if len(username) < 4:
            errormessage_signupscreen['text'] = 'Username must be more than 4 characters!'
        elif len(password) < 4:
            errormessage_signupscreen['text'] = 'Password must be more than 4 characters!'
        else:
                print(type(userdata))
                userdata.append({"Username": username,
                "Password": password,
                "Assignments": [],
                "Period": [],
                "Classes": [],
                "DueDate": [],
                "TimeDue": []})
                sp.seek(0)
                sp.truncate()
                json.dump(userdata, sp, indent=4)
                errormessage_signupscreen['text'] = 'Account successfully created!'
def changeclassesScreen():
    createclassScreen(main)
def updateClasses():
    global classFrameNum
    classScreen.grid(column=2, row=0, columnspan=8, rowspan=10, sticky='nsew')
    classeserrormessage = ttk.Label(master=classScreen, text='Classes not found!', background='#333333',foreground='red', font=('Georgia', 20))
    print(recallclasses())
    if recallclasses() == []:
        print("Classes not found!")
        classeserrormessage.grid(column=3, row=2, sticky='nsew')
        return
    else:
        try:
            classeserrormessage.grid_forget()
        except:
            print('Classes error message not found!')
    firsttime = True
    global classesScreenDict
    classesScreenDict = {}
    classFrameNum = 0
    recallclasses()
    for destroyclasses in classScreen.winfo_children():
        destroyclasses.destroy()
    classNUM = 0
    for classes in recallclasses():
        if classNUM % 3 == 0 or firsttime:
            createclassScreen(master=classScreen)
            if not firsttime:
                classNUM = 0
            print("Created a class screen!")
            firsttime = False
        classNUM += 1
        createclass(row=classNUM, column=1, width=60, height=10, master=classesScreenDict[classFrameNum], text=classes)


def askchatGPT(text, textbox):
    response = Model.generate_content(text)
    textbox.configure(state='normal')
    textbox.delete('1.0', END)
    textbox.insert('1.0', response.text)
    textbox.configure(state='disabled')


def changeloginscreentext(message):
    errormessage_loginmenu["text"] = message


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

def returnloginscreen():
    loading()
    progressionBar.step(50)
    main.update_idletasks()
    login_menu.grid(column=0, row=0, sticky='NSEW', columnspan=10, rowspan=10)
    signupscreen.grid_forget()
    progressionBar.step(100)
    loadingcomplete()

def changescreen_signupscreen():
    loading()
    progressionBar.step(50)
    main.update_idletasks()
    signupscreengrid()
    progressionBar.step(100)
    loadingcomplete()


def signupscreengrid():
    signupscreen.grid(column=0, row=0, sticky='NSEW', columnspan=50, rowspan=50)
# Test Code, Delete Later

#
# Home Screen
homescreen_menu = ttk.Frame(main, padding=20, style='Card.TFrame', borderwidth=20, height=2222)
homebutton_homescreen = ttk.Button(homescreen_menu, text='Home', style='Accent.TButton', width=20)
assignmentsbutton_homescreen = ttk.Button(homescreen_menu, text='Assignments', style='Accent.TButton', width=20, command=updateClasses)
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

# Loading Screen
loadingscreen = ttk.Frame(master=main, style='Card.TFrame')
progressionBar = ttk.Progressbar(master=loadingscreen, orient="horizontal", length=600)
loadingscreen.lift()

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
errormessage_loginmenu = Label(login_menu, width=40, text='Please enter your username and password', bg='#333333',
                               fg='red', font=("Georgia", 8))
signupbutton_loginmenu = ttk.Button(login_menu, text='Sign up', style='Accent.TButton', width=40,
                                    command=changescreen_signupscreen)
passwordlabel_loginmenu = ttk.Label(master=login_menu, text='Password: ', font=('Georgia', 10), background='#333333', foreground='white')
usernamelabel_loginmenu = ttk.Label(master=login_menu, text='Username: ', font=('Georgia', 10), background='#333333', foreground='white')
label_login = ttk.Label(master=login_menu, image=image, background='#333333')
passwordentry_loginmenu.grid(column=25, row=20, sticky='e')
usernameentry_loginmenu.grid(column=25, row=19, sticky='e')
usernamelabel_loginmenu.grid(column=25, row=19, sticky='w', pady=5)
passwordlabel_loginmenu.grid(column=25, row=20, sticky='w', pady=5)
loginbutton_loginmenu.grid(column=25, row=22, pady=5)
errormessage_loginmenu.grid(column=25, row=21, pady=5)
signupbutton_loginmenu.grid(column=25, row=23, pady=5)
label_login.grid(column=25, row=18)

# Sign Up Screen Widgets
passwordentry_signupscreen = ttk.Entry(master=signupscreen, foreground='white', width=30)
passwordentry_signupscreen.grid(column=25, row=20, sticky='e')
usernameentry_signupscreen = ttk.Entry(master=signupscreen, foreground='white', width=30)
usernameentry_signupscreen.grid(column=25, row=19, pady=5, sticky='e')
signupbutton_signupscreen = ttk.Button(master=signupscreen, style='Accent.TButton', text='Sign up', command=signup)
signupbutton_signupscreen.grid(column=25, row=22, sticky='ew', pady=5)
appLogo = ttk.Label(master=signupscreen, image=image, width=12, background='#333333')
appLogo.grid(column=25, row=18)
passwordlabel_signupscreen = ttk.Label(master=signupscreen, text='Password:', font=font_test, background='#333333',
                                       foreground='white', width=8)
passwordlabel_signupscreen.grid(column=25, row=20, sticky='w', padx=5)
usernamelabel_signupscreen = ttk.Label(master=signupscreen, text='Username: ', font=font_test, background='#333333',
                                       foreground='white', width=8)
usernamelabel_signupscreen.grid(column=25, row=19, sticky='w', padx=5)
returnlogin_signupscreen = ttk.Button(master=signupscreen, style='Accent.TButton', text='Return to login', command=returnloginscreen)
returnlogin_signupscreen.grid(column=25, row=23, sticky='ew', pady=5)
errormessage_signupscreen = ttk.Label(master=signupscreen, width=20, anchor="center", background="#333333", foreground='red', text='Insert a username and password!')
errormessage_signupscreen.grid(column=25, row=21, sticky='ew', pady=5)
# Classes Screen
classScreen = ttk.Frame(master=main, style='Card.TFrame')
# Classes Screen Configuration
for i in range(0, 6):
    classScreen.columnconfigure(i, weight=weight_factor)
    classScreen.rowconfigure(i, weight=weight_factor)
classScreen.grid_propagate(0)
main.mainloop()
