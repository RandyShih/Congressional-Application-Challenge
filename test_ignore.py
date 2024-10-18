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
AIConfigure = True

try:
    import google.generativeai as genai
    import os
except:
    print("google.generativeai import failed!")
    AIConfigure = False

# Google API Configuration
try:
    genai.configure(api_key="AIzaSyB_5KHGQ94m6cu_L-kEWeYzsXxuPmrvqp4")
    Model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    AIConfigure = True
except:
    print("google.generativeai configuration failed!")
    AIConfigure = False

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
title_font = font.Font(family='Georgia', size=9, weight='bold')
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
                                                                ]})])
style.configure('CustomF.TFrame')
style.element_create('CustomF', 'from', 'clam')
style.layout("CustomF.TFrame", [("CustomFFrame.TFrame", {'children': [('CustomFFrame.border', {'sticky': 'nswe'})]})]
             )
style.configure('CustomF.TFrame', background='#2B2B2B')
print(style.layout('Custom.TFrame'))
style.configure('Custom.TButton', background='#292828', borderwidth=2, relief='SUNKEN')
style.map('Custom.TButton', background=[('active', '#595858')])
print(font)
addClassWidgets = [

]
comboBoxData = None
assignmentList = [

]
assignmentScreenList =[

]
yearFrameNum = 0


class createclass:
    def __init__(self, width, height, column, row, master, className):
        if className != 'Insert Class':
            self.textdata = ""
            self.width = width
            self.height = height
            self.column = column
            self.row = row
            self.className = className + ", Period: " + str(getClassData(className)[0])
            self.frame = LabelFrame(master=master, width=self.width, background='#2B2B2B', bd=5,
                                    highlightbackground='#2B2B2B', foreground='white', relief='sunken',
                                    height=self.height, text=self.className, font=font_test)
            self.frame.grid(column=self.column, row=self.row, pady=15, sticky='nsew', columnspan=3)
            self.frame.propagate(0)
            self.label = ttk.Label(master=self.frame, text=className, background='#2B2B2B', foreground='white',
                                   font=title_font)
            self.classbutton = ttk.Button(master=self.frame, command=testcmd, text='Enter', width=10,
                                          style='Accent.TButton')
            self.classbutton.place(relx=.98, rely=.90, anchor='se')
            self.text = Text(master=self.frame, width=60, height=4, background="#2B2B2B", foreground="white",
                             relief="flat", font=title_font)
            self.text.place(relx=.45, rely=.9, anchor='s')
            self.text.propagate(0)
            self.scrollbar = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
            self.text['yscrollcommand'] = self.scrollbar.set
            self.scrollbar.pack(fill='y', side='right', expand=True, anchor='e')
            self.text.configure(state='normal')
            self.text.delete(1.0, END)
            print(recallassignmentdetails(className))
            try:
                for assignment, detail in recallassignmentdetails(className).items():
                    self.textdata = "Assigment: " + assignment + "\n" + "       Date Due: " + detail[
                        "DateDue"] + "\n" + "       Time Due: " + detail["TimeDue"] + "\n" + "       Description: " + \
                                    detail['Description'] + '\n\n'
                    self.text.insert(1.0, self.textdata)
                    print(str(assignment) + str(detail) + " were added!")
                self.text.configure(state='disabled')
            except:
                pass
            print(f'Created the class {className}!')
        else:
            global comboBoxData
            global addClassWidgets
            self.row = row
            self.master = master
            self.column = column
            self.className = className
            self.addClass = LabelFrame(master=self.master, width=40, height=4, background='#2B2B2B', relief='sunken')
            self.addClass.grid(row=0, column=self.column, pady=20, sticky='nsew', columnspan=3, rowspan=1)
            for i in range(0, 10):
                self.addClass.columnconfigure(i, weight=weight_factor)
                self.addClass.rowconfigure(i, weight=weight_factor)
            self.addClassLabelFrame = LabelFrame(master=self.addClass, text='Add a class!',
                                                 font=('Georgia', 15, 'bold'), foreground='white', background='#333333')
            self.addClassLabelFrame.grid(column=2, row=4, columnspan=1, sticky='nsew', padx=20, rowspan=1)
            self.addClassNameLabel = ttk.Label(master=self.addClassLabelFrame, width=10, font=title_font,
                                               foreground='white',
                                               background='#333333', text='Class Name: ')
            self.addClassPeriodLabel = ttk.Label(master=self.addClassLabelFrame, width=10, font=title_font,
                                                 foreground='white', background='#333333', text='Class Period: ')
            self.addClassErrorLabel = ttk.Label(master=self.addClassLabelFrame, background='#333333', foreground='red',
                                                text='Add a class!')
            self.addClassErrorLabel.grid(column=2, row=5, padx=20)
            self.addClassNameLabel.grid(column=0, row=3, sticky='w', padx=10, pady=15)
            self.addClassPeriodLabel.grid(column=0, row=5, sticky='w', padx=10, pady=15)
            self.addClassNameEntry = ttk.Entry(master=self.addClassLabelFrame, width=15, foreground='white')
            self.addClassPeriodEntry = ttk.Entry(master=self.addClassLabelFrame, width=15, foreground='white')
            self.addClassNameEntry.grid(column=1, row=3, sticky='e')
            self.addClassPeriodEntry.grid(column=1, row=5, sticky='e')
            self.addClassButton = ttk.Button(master=self.addClassLabelFrame, width=10, text='Add class',
                                             command=addClass)
            self.addClassButton.grid(column=2, row=3, padx=20, rowspan=1)
            self.removeClassLabelFrame = LabelFrame(master=self.addClass, text='Remove a class!',
                                                    font=('Georgia', 15, 'bold'), width=50, height=50,
                                                    background="#333333", foreground='white')
            self.removeClassLabelFrame.grid(column=4, row=4, rowspan=1, columnspan=3, sticky='nsew')
            self.removeClassButton = ttk.Button(master=self.removeClassLabelFrame, text='Remove Class',
                                                command=removeClass)
            self.removeClassComboBox = ttk.Combobox(master=self.removeClassLabelFrame, foreground='white')
            self.comboBoxData = []
            for classes in recallclasses():
                if classes != 'Insert Class':
                    self.comboBoxData.append(classes)
            self.removeClassComboBox['value'] = self.comboBoxData
            self.removeClassComboBox.grid(column=1, row=2, sticky='sn', pady=10, padx=30)
            self.removeClassButton.grid(column=2, row=2, sticky='sn', pady=10, padx=20)
            self.removeClassButtonLabel = Label(master=self.removeClassLabelFrame, width=20,
                                                text='              Remove a class!', font=('Georgia', 8),
                                                foreground='red', background='#333333', justify='center')
            self.removeClassButtonLabel.grid(column=1, row=3, pady=10, padx=20, sticky='ew', columnspan=5)
            self.addClass.propagate(0)
            self.removeClassComboBox.current(0)
            comboBoxData = self.comboBoxData
            addClassWidgets.append(self.addClassNameEntry)
            addClassWidgets.append(self.addClassPeriodEntry)
            addClassWidgets.append(self.addClassErrorLabel)
            addClassWidgets.append(self.removeClassComboBox)
            addClassWidgets.append(self.removeClassButtonLabel)
            print(addClassWidgets)


image2 = tk.PhotoImage(file='arrow.png')


class createclassScreen:
    def __init__(self, master):
        global classFrameNum
        self.master = master
        self.frame = ttk.Frame(master=master, style="Card.TFrame")
        self.frame.grid(column=0, row=0, sticky="NSEW", columnspan=6, rowspan=6)
        self.leftbutton = ttk.Button(master=self.frame, width=50, command=classesleftchange, text='Left',
                                     style='Accent.TButton')
        self.rightbutton = ttk.Button(master=self.frame, width=50, command=classesrightchange, text='Right',
                                      style='Accent.TButton')
        self.frame.grid_propagate(False)
        for i in range(0, 5):
            self.frame.rowconfigure(i, weight=weight_factor)
            self.frame.columnconfigure(i, weight=weight_factor)
            self.leftbutton.grid(column=2, row=5, sticky='s', pady=20)
        self.rightbutton.grid(column=3, row=5, sticky='s', pady=20)
        classFrameNum += 1
        print(classFrameNum)
        if classFrameNum != 1:
            self.frame.grid_forget()
        classesScreenDict.update({classFrameNum: self.frame})


class createAssignmentScreen:
    global assignmentList
    global yearFrameNum
    def __init__(self, master, text):
        self.master = master
        self.text = text
        self.frame = ttk.Frame(master=self.master, style="Card.TFrame")
        self.frame.grid(column=0, row=0, sticky="nsew", columnspan=11, rowspan=11)
        self.frame.grid_propagate(False)
        for i in range(0, 11):
            self.frame.rowconfigure(i, weight=weight_factor)
            self.frame.columnconfigure(i, weight=weight_factor)
        self.yearLabelFrame = LabelFrame(master=self.frame, text=self.text, background='#2B2B2B', foreground='white',
                                         font=('Georgia', 20, 'bold'), height=1, width=1, relief='sunken', borderwidth=4)
        self.yearLabelFrame.propagate(0)
        self.leftbutton = ttk.Button(master=self.frame, text='Left', width=20, command=leftAssignments)
        self.rightbutton = ttk.Button(master=self.frame, text='Right', width=20, command=rightAssignments)
        self.leftbutton.grid(column=4, row=10, rowspan=1, pady=10, padx=10)
        self.rightbutton.grid(column=7, row=10, rowspan=1, pady=10, padx=10)
        assignmentList.append(self.yearLabelFrame)
        assignmentScreenList.append(self.frame)
        for i in range(0, 4):
            self.yearLabelFrame.rowconfigure(i, weight=weight_factor)
            self.yearLabelFrame.columnconfigure(i, weight=weight_factor)
        self.yearLabelFrame.grid(row=1, column=1, columnspan=4, rowspan=8, pady=10, sticky='nsew', padx=10)
        self.addClassFrame = LabelFrame(master=self.frame, text='Add a Class!', background='#2B2B2B', foreground='white',
                                         font=('Georgia', 20, 'bold'), height=1, width=1, relief='sunken', borderwidth=4)
        self.addClassFrame.grid(column=5, row=1, sticky='nsew', columnspan=5, rowspan=8, pady=10, padx=10)
        if yearFrameNum != 1:
            self.frame.grid_forget()


class createAssignments:
    def __init__(self, row, master, month):
        self.row = row
        self.master = master
        self.month = "Month: " + monthFinder(month)
        self.frameAssignment = LabelFrame(master=self.master, text=self.month, font=('Georgia', 12, 'bold'), height=100, background='#333333', foreground='white')
        self.frameAssignment.grid(column=0, row=self.row, columnspan=4, rowspan=1, sticky='nsew', padx=15, pady=20)

def rightAssignments():
    global assignmentScreenList
    global yearFrameNum
    childrenCounter = 0
    for children in assignmentScreenList:
        childrenCounter += 1
    print(str(childrenCounter) + str(yearFrameNum))
    if yearFrameNum <= childrenCounter and yearFrameNum != 0:
        print(str(assignmentScreenList[::-1]))
        assignmentScreenList[::-1][yearFrameNum - 1].grid_forget()
        yearFrameNum -= 1
        assignmentScreenList[::-1][yearFrameNum - 1].grid(column=0, row=0, sticky="nsew", columnspan=11, rowspan=11)


def leftAssignments():
    global assignmentScreenList
    global yearFrameNum
    childrenCounter = 0
    for children in assignmentScreenList:
        childrenCounter += 1
    print(str(childrenCounter) + str(yearFrameNum))
    if yearFrameNum < childrenCounter:
        assignmentScreenList[::-1][yearFrameNum - 1].grid_forget()
        yearFrameNum += 1
        assignmentScreenList[::-1][yearFrameNum - 1].grid(column=0, row=0, sticky="nsew", columnspan=11, rowspan=11)

def createAssignment():
    global assignmentList
    global yearFrameNum
    yearFrameNum = 0
    monthFrameNum = 0
    dayFrameNum = 0
    monthindex = 0
    stringResponse = ""
    initialize = True
    yearMonthList = [

    ]
    assignmentList = [

    ]
    assignmentDateIndex = {

    }
    yearDate = [

    ]
    classesYear = {

    }
    monthDict = {

    }
    dayList = [

    ]
    sortedDayList = [

    ]
    monthList = [

    ]
    monthYearDict = {

    }
    for i in assignmentScreen.winfo_children():
        i.destroy()
    counter = 0
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        assignments = userdata[user]['Assignments']
    for assignment, data in assignments.items():
        counter += 1
        yearDate.append(int(data['DateDue'][-4:]))
        monthDict.update({assignment: {monthIndexer(data['DateDue']): yearFinder(assignment)}})
        dayList.append(int(dayFinder(assignment)))
    for day in sorted(dayList):
        sortedDayList.append(day)
    for assignment, key in assignments.items():
        monthList.append(monthIndexer(key['DateDue']))
    for assignment, key in assignments.items():
        monthYearDict.update({monthIndexer(key['DateDue']): yearFinder(assignment)})
    for year in sorted(yearDate):
        yearMonthList = [

        ]
        for assignment, date in monthDict.items():
            for month, yearM in date.items():
                if int(year) == int(yearM):
                    yearMonthList.append(month)
        assignmentDateIndex.update({year: sorted(set(yearMonthList))})

    assignmentScreen.grid(row=0, column=2, columnspan=8, rowspan=10, sticky='nsew')
    assignmentScreen.lift()
    for year, months in assignmentDateIndex.items():
        monthIndex = 0
        monthFrameNum = 0
        if initialize == True:
            createAssignmentScreen(master=assignmentScreen, text=year)
            yearFrameNum += 1
            initialize = False
        print("New Year: " + '\n' + "    Year Frame NUM: " + str(yearFrameNum) + '\n' + "    monthList: " + str(monthList) + '\n' + "    yearDate: " + str(sorted(yearDate)))
        for monthN in monthList:
            monthIndex += 1
            # print(str(months) + " " + str(monthN) + " " + str(sorted(yearDate)[monthIndex-1]) + " " + str(year))
            if sorted(yearDate)[monthIndex-1] == year:
                if monthFrameNum % 2 == 0:
                    print(stringResponse)
                    stringResponse = ""
                    monthFrameNum = 0
                    print("Assignment screen created for: " + "Year: " + str(year) + ", Month: " + str(monthN))
                    createAssignmentScreen(master=assignmentScreen, text=year)
                    # print("Assignment Screen List: " + str(assignmentScreenList))
                    yearFrameNum += 1
                stringResponse += "    Assignment for month, year created: " + str(monthN) + ", " + str(year) + '\n'
                #stringResponse += "    Month Frame: " + str(monthFrameNum) + ", Year Frame Num: " + str(yearFrameNum) + '\n'
                #stringResponse += "    Assignment Screen List Index: " + str(assignmentScreenList[monthFrameNum-1]) + '\n'
                #stringResponse += "    Assignment Screen List: " + str(assignmentScreenList) + '\n'
                print(assignmentList[yearFrameNum - 1])
                createAssignments(row=monthFrameNum, master=assignmentList[yearFrameNum - 1], month=monthN)
                monthFrameNum += 1



# Assignment Screen Configuration
assignmentScreen = ttk.Frame(master=main, style='Card.TFrame')
for i in range(0, 11):
    assignmentScreen.rowconfigure(i, weight=weight_factor)
    assignmentScreen.columnconfigure(i, weight=weight_factor)
assignmentScreen.propagate(0)

def getTime(assignment):
    with open('user_data.json', 'r') as sp:
        timeM = 0
        userdata = json.load(sp)
        print(userdata[user]['Assignments'][assignment]['TimeDue'][:2])
        timeM = int(userdata[user]['Assignments'][assignment]['TimeDue'][:2]) * 60 + int(
            userdata[user]['Assignments'][assignment]['TimeDue'][3:5])
        if userdata[user]['Assignments'][assignment]['TimeDue'][-2:] == 'PM':
            timeM = timeM + 720
        print("Minutes: " + str(timeM))
        return timeM


def assignmentDateChecker():
    print('Hey')


def yearFinder(assignment):
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        year = userdata[user]['Assignments'][assignment]['DateDue'][-4:]
        return year


def dayFinder(assignment):
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        day = userdata[user]['Assignments'][assignment]['DateDue'][-7:-5]
        return day


def monthIndexer(Date):
    if 'January' == str(Date[0:7]):
        return 1
    elif 'February' == Date[0:8]:
        return 2
    elif 'March' == Date[0:5]:
        return 3
    elif 'April' in Date[0:5]:
        return 4
    elif 'May' in Date[0:3]:
        return 5
    elif 'June' in Date[0:4]:
        return 6
    elif 'July' in Date[0:4]:
        return 7
    elif 'August' in Date[0:6]:
        return 8
    elif 'September' in Date[0:9]:
        return 9
    elif 'October' in Date[0:7]:
        return 10
    elif 'November' in Date[0:8]:
        return 11
    elif 'December' in Date[0:8]:
        return 12
    else:
        return 14

def monthFinder(Date):
    if Date == 1:
        return 'January'
    elif Date == 2:
        return 'February'
    elif Date == 3:
        return 'March'
    elif Date == 4:
        return 'April'
    elif Date == 5:
        return 'May'
    elif Date == 6:
        return 'June'
    elif Date == 7:
        return 'July'
    elif Date == 8:
        return 'August'
    elif Date == 9:
        return 'September'
    elif Date == 10:
        return 'October'
    elif Date == 11:
        return 'November'
    elif Date == 12:
        return 'December'
    else:
        return "No month found..."
def addClass():
    global addClassWidgets
    print(addClassWidgets)
    className = addClassWidgets[0].get()
    classPeriod = addClassWidgets[1].get()
    errorLabel = addClassWidgets[2]
    intNum = False
    with open('user_data.json', 'r+') as sp:
        userdata = json.load(sp)
        if className in userdata[user]['Classes']:
            errorLabel['text'] = 'Class already exists!'
            return
        if int(classPeriod) in userdata[user]['Period']:
            errorLabel['text'] = 'Period already exists!'
            return
        if len(className) < 15 and len(className) > 2:
            userdata[user]['Classes'].append(className)
        else:
            errorLabel['text'] = 'Invalid class name!'
            return
        try:
            int(classPeriod)
            intNum = True
        except:
            intNum = False
        if len(classPeriod) < 3 and intNum:
            userdata[user]['Period'].append(int(classPeriod))
        else:
            errorLabel['text'] = 'Invalid period!'
            return
        sp.seek(0)
        sp.truncate()
        json.dump(userdata, sp, indent=4)
        errorLabel['text'] = 'Class added!'
        sp.close()
    updateClasses()


def removeClass():
    global addClassWidgets
    global comboBoxData
    classes = addClassWidgets[3]
    errorLabel = addClassWidgets[4]
    with open('user_data.json', 'r+') as sp:
        userdata = json.load(sp)
        comboBoxData = classes.get()
        print(comboBoxData)
        index = userdata[user]['Classes'].index(comboBoxData)
        del userdata[user]['Classes'][index]
        del userdata[user]['Period'][index - 1]
        try:
            classesDict = recallassignmentdetails(classes.get())
            for asssignments, data in classesDict.items():
                del userdata[user]['Assignments'][asssignments]
        except:
            print("No assignments found!")
        sp.seek(0)
        sp.truncate()
        json.dump(userdata, sp, indent=4)
    updateClasses()


def classesrightchange():
    print(classesScreenDict)
    global classFrameNum
    classNumUpdate = 0
    valueList = []
    for classes in classesScreenDict:
        classNumUpdate += 1
        valueList.append(classNumUpdate)
    valueList = valueList[::-1]
    print("Value of classFrameNum: " + str(classFrameNum))
    if classFrameNum <= classNumUpdate and classFrameNum != 1:
        indexValue = valueList.index(classFrameNum) + 1
        print("Value of the key: " + str(indexValue))
        classesScreenDict[indexValue].grid_forget()
        classFrameNum = classFrameNum - 1
        indexValue = valueList.index(classFrameNum) + 1
        print("Value of the key: " + str(indexValue))
        classesScreenDict[indexValue].grid(column=0, row=0, sticky="NSEW", columnspan=6, rowspan=6)


def loading():
    progressionBar.step(0)
    loadingscreen.grid(column=0, row=0, columnspan=10, rowspan=10, sticky='nsew')
    progressionBar.place(rely=.5, relx=.5, anchor=CENTER)


def loadingcomplete():
    loadingscreen.grid_forget()
    progressionBar.step(0)


def getClassData(classes):
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        period = 0
        className = None
        if classes in userdata[user]['Classes']:
            index = userdata[user]['Classes'].index(classes)
            print("Index: " + str(index))
            period = userdata[user]['Period'][index - 1]
            return [period, classes]
        else:
            return "Class not found!"


def recallassignmentdetails(classes):
    with open("user_data.json", 'r') as sp:
        userdata = json.load(sp)
        userassignmentsSPECS = {

        }
        assignmentsDict = userdata[user]['Assignments']
        try:
            for assignment, data in assignmentsDict.items():
                if classes == data['Class']:
                    userassignmentsSPECS.update({assignment: data})
            return userassignmentsSPECS
        except:
            return "Classes not found!"


def classesleftchange():
    global classFrameNum
    global classesScreenDict
    classAMT = 0
    newClassesList = [

    ]
    try:
        for classes in classesScreenDict:
            classAMT += 1
            newClassesList.append(classesScreenDict[classAMT])
    except:
        print("Classes left change error!")
    newClassesList = newClassesList[::-1]
    print("New Classes List: " + str(newClassesList))
    if classFrameNum != 0 and classFrameNum < classAMT:
        print("Class Frame Num: " + str(classFrameNum))
        newClassesList[classFrameNum - 1].grid_forget()
        classFrameNum = classFrameNum + 1
        print(classFrameNum)
        newClassesList[classFrameNum - 1].grid(column=0, row=0, sticky="NSEW", columnspan=6, rowspan=6)


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
    mainScreen_homeScreen.grid_forget()


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
                             "Assignments": {},
                             "Period": [],
                             "Classes": ['Insert Class'],
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
    global addClassWidgets
    classScreen.lift()
    classScreen.grid(column=2, row=0, columnspan=8, rowspan=10, sticky='nsew')
    classeserrormessage = ttk.Label(master=classScreen, text='Classes not found!', background='#333333',
                                    foreground='red', font=('Georgia', 20))
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
    addClassWidgets = [

    ]
    for destroyclasses in classScreen.winfo_children():
        destroyclasses.destroy()
    classNUM = 0
    for classes in recallclasses():
        if classNUM % 4 == 0 or firsttime:
            createclassScreen(master=classScreen)
            if not firsttime:
                classNUM = 0
            print("Created a class screen!")
            firsttime = False
        classNUM += 1
        createclass(row=classNUM - 1, column=1, width=1, height=20, master=classesScreenDict[classFrameNum],
                    className=classes)


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


def findclassperiod(classtype):
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        counter = 0
        for classes in userdata[user]['Classes']:
            if classtype == classes:
                return userdata[user]['Period'][counter]
            counter += 1


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
homeButton_homeScreen = ttk.Button(homescreen_menu, text='Home', style='Accent.TButton', width=40)
assignmentsButton_homeScreen = ttk.Button(homescreen_menu, text='Assignments', style='Accent.TButton', width=40,
                                          command=createAssignment)
classesButton_homeScreen = ttk.Button(homescreen_menu, text='Classes', style='Accent.TButton', width=40,
                                      command=updateClasses)
calanderButton_homeScreen = ttk.Button(homescreen_menu, text='Calendar', style='Accent.TButton', width=40)
profileButton_homeScreen = ttk.Button(homescreen_menu, text='Profile', style='Accent.TButton', width=40)
settingsButton_homeScreen = ttk.Button(homescreen_menu, text='Settings', style='Accent.TButton', width=40)
mainScreen_homeScreen = ttk.Frame(main, style='Card.TFrame', borderwidth=10, height=100)
mainScreen_homeScreen.grid(row=0, column=2, sticky='nsew', columnspan=8, rowspan=10)
ignore_text = Text(master=mainScreen_homeScreen, width=50, height=20, borderwidth=20, background='gray',
                   font=font_test, state='disabled')
textInput_homeScreen = ttk.Entry(master=mainScreen_homeScreen, width=30)

HomeScreenIcon = tk.PhotoImage(file="R_optimized (1).png")
appIcon_homescreen = ttk.Label(master=homescreen_menu, image=HomeScreenIcon, background='#333333')
askAI_homescreen = ttk.Frame(master=main, height=100, width=10, style='Card.TFrame')
askAI_homescreen.grid(row=3, column=0, sticky='NSEW', columnspan=2, rowspan=4, pady=2)
askAIText_homeScreen = Text(master=askAI_homescreen, width=15, height=10, background="#2B2B2B", foreground='white')
askAI_homescreen.propagate(False)
for i in range(0, 3):
    print(i)
    askAI_homescreen.rowconfigure(i, weight=weight_factor)
    askAI_homescreen.columnconfigure(i, weight=weight_factor)
askAIText_homeScreen.grid(row=0, column=1, sticky='nsew', pady=10)
askAIEntry = ttk.Entry(master=askAI_homescreen, width=20, foreground='white')
askAIEntry.grid(row=1, column=1)
askAIText_homeScreen.configure(state='disabled')
askAIButton = ttk.Button(master=askAI_homescreen, width=5, text='Ask AI!',
                         command=lambda: askchatGPT(askAIEntry.get(), askAIText_homeScreen))
askAIButton.grid(row=2, column=1, stick='ew')
appIcon_homescreen.grid(row=0, column=0)
settingsButton_homeScreen.grid(column=0, row=4, pady=20)
homeButton_homeScreen.grid(column=0, row=1, pady=20)
# profileButton_homeScreen.grid(column=0, row=5, pady=20)
# calanderButton_homeScreen.grid(column=0, row=4, pady=20)
classesButton_homeScreen.grid(column=0, row=3, pady=20)
assignmentsButton_homeScreen.grid(column=0, row=2, pady=20)
homescreen_menu.grid(column=0, row=0, sticky='nsew', columnspan=2, rowspan=5)
homescreen_menu.grid_propagate(0)


def disableAICall():
    askAIText_homeScreen['foreground'] = 'red'
    askAIText_homeScreen['state'] = 'normal'
    askAIText_homeScreen.insert(1.0, "AI CONFIGURATION FAILED!")
    askAIText_homeScreen['state'] = 'disabled'
    askAIEntry.configure(state='disabled')


if not AIConfigure:
    disableAICall()

# Loading Screen
loadingscreen = ttk.Frame(master=main, style='Card.TFrame')
progressionBar = ttk.Progressbar(master=loadingscreen, orient="horizontal", length=600)
loadingscreen.lift()

# Main Screen Grid configuration
mainScreen_homeScreen.grid_propagate(0)
for i in range(0, 6):
    mainScreen_homeScreen.grid_columnconfigure(i, weight=weight_factor)
    mainScreen_homeScreen.grid_rowconfigure(i, weight=weight_factor)
scrollbar = ttk.Scrollbar(master=mainScreen_homeScreen, orient="vertical")

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
passwordlabel_loginmenu = ttk.Label(master=login_menu, text='Password: ', font=('Georgia', 10), background='#333333',
                                    foreground='white')
usernamelabel_loginmenu = ttk.Label(master=login_menu, text='Username: ', font=('Georgia', 10), background='#333333',
                                    foreground='white')
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
returnlogin_signupscreen = ttk.Button(master=signupscreen, style='Accent.TButton', text='Return to login',
                                      command=returnloginscreen)
returnlogin_signupscreen.grid(column=25, row=23, sticky='ew', pady=5)
errormessage_signupscreen = ttk.Label(master=signupscreen, width=20, anchor="center", background="#333333",
                                      foreground='red', text='Insert a username and password!')
errormessage_signupscreen.grid(column=25, row=21, sticky='ew', pady=5)
# Classes Screen
classScreen = ttk.Frame(master=main, style='Card.TFrame')
# Classes Screen Configuration
for i in range(0, 6):
    classScreen.columnconfigure(i, weight=weight_factor)
    classScreen.rowconfigure(i, weight=weight_factor)
classScreen.grid_propagate(0)
main.mainloop()
