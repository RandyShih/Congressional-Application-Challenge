import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import json as json
import time as time
import re as re
from re import split
from tkinter import messagebox

increase_value = 0
classesScreenValue = 1
classFrameNum = 0
weight_factor = 1
assignmentCounter = 0
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
main_font = font.Font(family='Georgia')
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
assignmentScreenList = [

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
                                    height=self.height, text=self.className, font=main_font)
            self.frame.grid(column=self.column, row=self.row, pady=15, sticky='nsew', columnspan=3)
            self.frame.propagate(0)
            self.label = ttk.Label(master=self.frame, text=className, background='#2B2B2B', foreground='white',
                                   font=title_font)
            self.classbutton = ttk.Button(master=self.frame, command=testcmd, text='Enter', width=10,
                                          style='Accent.TButton')
            #self.classbutton.place(relx=.98, rely=.90, anchor='se'), self.text['width'] = 60
            self.text = Text(master=self.frame, width=70, height=4, background="#2B2B2B", foreground="white",
                             relief="flat", font=title_font, wrap=WORD)
            self.text.place(relx=.5, rely=.9, anchor='s')
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
            try:
                self.removeClassComboBox.current(0)
            except:
                print("Error_Ignore!")
            comboBoxData = self.comboBoxData
            addClassWidgets.append(self.addClassNameEntry)
            addClassWidgets.append(self.addClassPeriodEntry)
            addClassWidgets.append(self.addClassErrorLabel)
            addClassWidgets.append(self.removeClassComboBox)
            addClassWidgets.append(self.removeClassButtonLabel)
            print(addClassWidgets)

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
        self.leftbutton.grid(column=2, row=4)
        self.rightbutton.grid(column=3, row=4)
        classFrameNum += 1
        print(classFrameNum)
        if classFrameNum != 1:
            self.frame.grid_forget()
        classesScreenDict.update({classFrameNum: self.frame})


class createAssignmentScreen:
    global assignmentList
    global yearFrameNum

    def __init__(self, master, text):
        self.comboBoxDataAssignments = [

        ]
        self.comboBoxDataClasses = [

        ]
        self.master = master
        self.text = text
        self.frame = ttk.Frame(master=self.master, style="Card.TFrame")
        self.frame.grid(column=0, row=0, sticky="nsew", columnspan=11, rowspan=11)
        self.frame.grid_propagate(False)
        print('\n' + "Assignment Screen Created for: " + str(text) + '\n' + "     Frame: " + str(
            self.frame) + '\n' + "     Year Frame Num: " + str(yearFrameNum))
        for i in range(0, 10):
            self.frame.rowconfigure(i, weight=weight_factor)
            self.frame.columnconfigure(i, weight=weight_factor)
        if self.text != None:
            self.yearLabelFrame = LabelFrame(master=self.frame, text=self.text, background='#2B2B2B', foreground='white',
                                             font=('Georgia', 20, 'bold'), height=1, width=1, relief='sunken',
                                             borderwidth=4)
            self.yearLabelFrame.grid_propagate(False)
            for i in range(0, 8):
                self.yearLabelFrame.rowconfigure(i, weight=weight_factor)
                self.yearLabelFrame.columnconfigure(i, weight=weight_factor)
            self.yearLabelFrame.grid(row=2, column=1, columnspan=4, rowspan=8, pady=10, sticky='nsew', padx=10)
            assignmentList.append(self.yearLabelFrame)

        self.leftbutton = ttk.Button(master=self.frame, text='Left', width=40, command=leftAssignments,
                                     style='Accent.TButton')
        self.rightbutton = ttk.Button(master=self.frame, text='Right', width=40, command=rightAssignments,
                                      style='Accent.TButton')
        self.leftbutton.grid(column=3, row=10, rowspan=1, pady=20, padx=10)
        self.rightbutton.grid(column=6, row=10, rowspan=1, pady=20, padx=10)
        assignmentScreenList.append(self.frame)
        self.pertinentAssignmentLabelFrame = LabelFrame(master=self.frame, background='#2B2B2B', width=1,
                                                        relief='sunken', borderwidth=4)
        self.pertinentAssignmentLabelFrame.grid(column=5, row=2, sticky='nsew', columnspan=4, rowspan=8, pady=10,
                                                padx=10)
        self.addAssignmentLabelFrame = LabelFrame(master=self.frame, background='#2B2B2B', width=1, relief='sunken',
                                                  borderwidth=4)
        self.addAssignmentLabelFrame.grid(column=1, row=0, sticky='nsew', rowspan=2, columnspan=8, padx=10, pady=20)
        self.pertinentAssignmentSecondLabelFrame = LabelFrame(master=self.pertinentAssignmentLabelFrame,
                                                              text="Due now!", font=title_font, background='#333333',
                                                              foreground='white')
        self.removeAssignmentLabelFrame = LabelFrame(master=self.pertinentAssignmentLabelFrame,
                                                     text="Remove an Assignment", font=title_font, background='#333333',
                                                     foreground='white')
        self.removeAssignmentComboBox = ttk.Combobox(master=self.removeAssignmentLabelFrame, width=40,
                                                     foreground='white')
        with open('user_data.json', 'r') as sp:
            user_data = json.load(sp)
            for assignment, value in user_data[user]['Assignments'].items():
                if user_data[user]['Assignments'][assignment]['Complete'] == 'True':
                    self.comboBoxDataAssignments.append(assignment + " " + '✅')
                else:
                    self.comboBoxDataAssignments.append(assignment + " " + '❌')
        self.removeAssignmentComboBox['value'] = self.comboBoxDataAssignments
        self.removeAssignmentComboBox.grid(column=0, row=0, sticky='nsew', padx=25, pady=10)
        self.removeAssignmentButton = ttk.Button(master=self.removeAssignmentLabelFrame, text='Remove', width=20,
                                                 style='Accent.TButton',
                                                 command=lambda: deleteAssignment(self.removeAssignmentComboBox.get()))
        self.removeAssignmentButton.grid(column=0, row=1, sticky='nsew', padx=25, pady=10)
        self.removeAssignmentMarkAsCompleted = ttk.Button(master=self.removeAssignmentLabelFrame,
                                                          text='Mark as complete', width=20, style='Accent.TButton',
                                                          command=lambda: self.updateRemoveComboBox(True))
        self.removeAssignmentMarkAsCompleted.grid(column=0, row=2, sticky='nsew', padx=25, pady=10)
        self.removeAssignmentMarkAsInComplete = ttk.Button(master=self.removeAssignmentLabelFrame,
                                                           text='Mark as incomplete', width=20, style='Accent.TButton',
                                                           command=lambda: self.updateRemoveComboBox(False))
        self.removeAssignmentMarkAsInComplete.grid(column=0, row=3, sticky='nsew', padx=25, pady=10)
        try:
            self.removeAssignmentComboBox.current(0)
        except:
            print("Error_Ignore!")
        self.pertinentAssignmentLabelFrame.grid_propagate(False)
        self.pertinentAssignmentSecondLabelFrame.grid_propagate(False)
        self.removeAssignmentLabelFrame.grid_propagate(False)
        for val in range(0, 6):
            self.pertinentAssignmentLabelFrame.rowconfigure(val, weight=weight_factor)
            self.pertinentAssignmentLabelFrame.columnconfigure(val, weight=weight_factor)
        self.pertinentAssignmentSecondLabelFrame.grid(row=0, column=0, sticky='nsew', pady=10, rowspan=3, columnspan=6,
                                                      padx=30)
        self.pertinentAssignmentTextData = ''
        self.pertinentAssignmentText = Text(master=self.pertinentAssignmentSecondLabelFrame, height=11, width=28, font=main_font, foreground='white', background='#2B2B2B', wrap=WORD)
        self.pertinentAssignmentText.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)
        with open('user_data.json', 'r') as sp:
            user_data = json.load(sp)
            if 1 == 1:
                for assignment, detail in user_data[user]['Assignments'].items():
                    if assignment in dueNow():
                        if detail['Complete'] == 'True':
                            self.pertinentAssignmentTextData += "Assigment ✅: " + assignment + "\n" + "       Date Due: " + detail[
                                "DateDue"] + "\n" + "       Time Due: " + detail["TimeDue"] + "\n" + "       Description: " + \
                                            detail['Description'] + '\n\n'
                        else:
                            self.pertinentAssignmentTextData += "Assigment ❌: " + assignment + "\n" + "       Date Due: " + detail[
                                "DateDue"] + "\n" + "       Time Due: " + detail[
                                                       "TimeDue"] + "\n" + "       Description: " + \
                                                   detail['Description'] + '\n\n'
            self.pertinentAssignmentText.insert(1.0, self.pertinentAssignmentTextData)
            self.pertinentAssignmentText['state'] = 'disabled'
        self.removeAssignmentLabelFrame.grid(row=3, column=0, sticky='nsew', pady=10, rowspan=3, padx=30, columnspan=6)
        self.addAssignmentSecondLabelFrame = LabelFrame(master=self.addAssignmentLabelFrame, text='Add an Assignment!',
                                                        font=title_font, height=100, width=725, foreground='white',
                                                        background='#333333')
        self.addAssignmentSecondLabelFrame.grid(row=0, column=0, sticky='nsew', rowspan=3, columnspan=3, pady=12,
                                                padx=18)
        self.addAssignmentLabelFrame.grid_propagate(False)
        for val in range(0, 100):
            self.addAssignmentSecondLabelFrame.rowconfigure(val, weight=weight_factor)
            self.addAssignmentSecondLabelFrame.columnconfigure(val, weight=weight_factor)
        self.addAssignmentNameEntry = ttk.Entry(master=self.addAssignmentSecondLabelFrame, width=15, foreground='white')
        self.addAssignmentTimeEntry = ttk.Entry(master=self.addAssignmentSecondLabelFrame, width=15, foreground='white')
        self.addAssignmentDateDueEntry = ttk.Entry(master=self.addAssignmentSecondLabelFrame, width=15,
                                                   foreground='white')
        self.addAssignmentDescriptionEntry = ttk.Entry(master=self.addAssignmentSecondLabelFrame, width=15,
                                                       foreground='white')
        self.addAssignmentClassComboBox = ttk.Combobox(master=self.addAssignmentSecondLabelFrame, foreground='white',
                                                       width=15)
        self.addAssignmentButton = ttk.Button(master=self.addAssignmentSecondLabelFrame, style='Accent.TButton',
                                              text='Add Assignment', command=self.createAssignment)

        self.addAssignmentNameLabel = ttk.Label(master=self.addAssignmentSecondLabelFrame, width=15,
                                                text=' Assignment Name:', background='#333333', foreground='white',
                                                font=title_font)
        self.addAssignmentTimeLabel = ttk.Label(master=self.addAssignmentSecondLabelFrame, width=10,
                                                text=' Set a Time:', background='#333333', foreground='white',
                                                font=title_font)
        self.addAssignmentDateDueLabel = ttk.Label(master=self.addAssignmentSecondLabelFrame, width=10,
                                                   background='#333333', foreground='white', text='Date Due:',
                                                   font=title_font)
        self.addAssignmentDescriptionLabel = ttk.Label(master=self.addAssignmentSecondLabelFrame, width=10,
                                                       background='#333333', foreground='white', text='Description:',
                                                       font=title_font)
        self.addAssignmentClassLabel = ttk.Label(master=self.addAssignmentSecondLabelFrame, width=10,
                                                 text='Select a Class:', background='#333333', foreground='white',
                                                 font=title_font)

        self.addAssignmentSecondLabelFrame.grid_propagate(False)
        self.addAssignmentTimeEntry.grid(row=1, column=4, pady=5, sticky='w', padx=5)
        self.addAssignmentTimeLabel.grid(row=1, column=3, pady=5, sticky='e', padx=5)
        self.addAssignmentNameLabel.grid(row=0, column=3, sticky='e', pady=5, padx=5)
        self.addAssignmentNameEntry.grid(row=0, column=4, sticky='w', pady=5, padx=5)
        self.addAssignmentDateDueLabel.grid(row=0, column=10, pady=5, sticky='e', padx=10)
        self.addAssignmentDateDueEntry.grid(row=0, column=11, pady=5, sticky='w', padx=5)
        self.addAssignmentDescriptionLabel.grid(row=1, column=10, sticky='e', pady=5, padx=10)
        self.addAssignmentDescriptionEntry.grid(row=1, column=11, sticky='w', pady=5, padx=5)
        self.addAssignmentClassLabel.grid(row=0, column=24, sticky='w', pady=5, padx=5)
        for classes in recallclasses():
            if classes != 'Insert Class':
                self.comboBoxDataClasses.append(classes)
        self.addAssignmentClassComboBox['value'] = self.comboBoxDataClasses
        try:
            self.addAssignmentClassComboBox.current(0)
        except:
            print('Error_ignore!')
        self.addAssignmentClassComboBox.grid(row=0, column=25, sticky='e', pady=5, columnspan=2)
        self.addAssignmentButton.grid(row=1, column=24, stick='ew', columnspan=20, padx=20, pady=5)

        self.assignmentName = self.addAssignmentNameEntry.get()
        self.timeDue = self.addAssignmentTimeEntry.get()
        self.dateDue = self.addAssignmentDateDueEntry.get()
        self.description = self.addAssignmentDescriptionEntry.get()
        self.className = self.addAssignmentClassComboBox.get()
        if yearFrameNum != 1:
            self.frame.grid_forget()

    def updateRemoveComboBox(self, bool):
        markAssignment(self.removeAssignmentComboBox.get()[:-2], bool)
        index = self.comboBoxDataAssignments.index(self.removeAssignmentComboBox.get())
        self.comboBoxDataAssignments = [

        ]
        with open('user_data.json', 'r') as sp:
            user_data = json.load(sp)
            for assignment, value in user_data[user]['Assignments'].items():
                if user_data[user]['Assignments'][assignment]['Complete'] == 'True':
                    self.comboBoxDataAssignments.append(assignment + " " + '✅')
                else:
                    self.comboBoxDataAssignments.append(assignment + " " + '❌')
        self.removeAssignmentComboBox['value'] = self.comboBoxDataAssignments
        self.removeAssignmentComboBox.current(index)

    def createAssignment(self):
        self.dateDueListCounter = 0
        self.timeDueCounter = 0
        self.dateDueINTTrue = True
        self.timeDueINTTrue = True
        self.assignmentNameCheck = True
        self.dueDateChecked = False
        self.timeDueChecked = False
        self.assignmentName = self.addAssignmentNameEntry.get()
        self.timeDue = self.addAssignmentTimeEntry.get()
        self.dateDue = self.addAssignmentDateDueEntry.get()
        self.description = self.addAssignmentDescriptionEntry.get()
        self.className = self.addAssignmentClassComboBox.get()
        self.dateDueListSplit = split('/', self.dateDue)
        self.timeDueListSplit = split(':', self.timeDue)
        for val in self.dateDueListSplit:
            self.dateDueListCounter += 1
            try:
                int(val)
            except:
                self.dateDueINTTrue = False

        for val in self.timeDueListSplit:
            self.timeDueCounter += 1
            try:
                int(val)
            except:
                self.timeDueINTTrue = False
        if self.assignmentName in recallassignmentdetails(self.className):
            self.assignmentNameCheck = False
            self.addAssignmentNameEntry.delete(0, END)
            self.addAssignmentNameEntry['foreground'] = 'red'
            self.addAssignmentNameEntry.insert(0, 'Name exists!')
        if self.dateDueListCounter == 3 and self.dateDueINTTrue:
            if int(self.dateDueListSplit[0]) > 31 or int(self.dateDueListSplit[0]) == 0:
                self.addAssignmentDateDueEntry.delete(0, END)
                self.addAssignmentDateDueEntry['foreground'] = 'red'
                self.addAssignmentDateDueEntry.insert(0, 'Invalid Day!')
            elif int(self.dateDueListSplit[1]) > 12 or int(self.dateDueListSplit[1]) == 0:
                self.addAssignmentDateDueEntry.delete(0, END)
                self.addAssignmentDateDueEntry['foreground'] = 'red'
                self.addAssignmentDateDueEntry.insert(0, 'Invalid Month!')
            elif len(self.dateDueListSplit[2]) != 4:
                self.addAssignmentDateDueEntry.delete(0, END)
                self.addAssignmentDateDueEntry['foreground'] = 'red'
                self.addAssignmentDateDueEntry.insert(0, 'Invalid Year!')
            else:
                self.dueDateChecked = True
        else:
            self.addAssignmentDateDueEntry.delete(0, END)
            self.addAssignmentDateDueEntry['foreground'] = 'red'
            self.addAssignmentDateDueEntry.insert(0, 'DD/MM/YYYY')
        if self.timeDueCounter == 2 and self.timeDueINTTrue:
            if int(self.timeDueListSplit[0]) > 24:
                self.addAssignmentTimeEntry.delete(0, END)
                self.addAssignmentTimeEntry['foreground'] = 'red'
                self.addAssignmentTimeEntry.insert(0, 'Invalid Hour!')
            elif int(self.timeDueListSplit[1]) > 59:
                self.addAssignmentTimeEntry.delete(0, END)
                self.addAssignmentTimeEntry['foreground'] = 'red'
                self.addAssignmentTimeEntry.insert(0, 'Invalid Minute!')
            elif int(self.timeDueListSplit[1]) != 0 and int(self.timeDueListSplit[0]) == 24:
                self.addAssignmentTimeEntry.delete(0, END)
                self.addAssignmentTimeEntry['foreground'] = 'red'
                self.addAssignmentTimeEntry.insert(0, 'Invalid Minute!')
            else:
                self.timeDueChecked = True
        else:
            self.addAssignmentTimeEntry.delete(0, END)
            self.addAssignmentTimeEntry['foreground'] = 'red'
            self.addAssignmentTimeEntry.insert(0, 'HH:MM, EX: 21:54')
        if self.dueDateChecked and self.timeDueChecked and self.assignmentNameCheck:
            with open('user_data.json', 'r+') as sp:
                self.user_data = json.load(sp)
                self.assignmentDataDict = {}
                self.timeDueValue = 0
                self.dueDateValue = 0
                self.timeDueMinute = 0
                self.dateDueDay = 0
                self.dateDueMonth = 0
                if len(self.timeDueListSplit[1]) == 1:
                    self.timeDueMinute = '0' + str(self.timeDueListSplit[1])
                else:
                    self.timeDueMinute = str(self.timeDueListSplit[1])
                if int(self.timeDueListSplit[0]) <= 12:
                    if int(self.timeDueListSplit[0]) == 12:
                        self.timeDueValue = str(self.timeDueListSplit[0]) + ":" + self.timeDueMinute + " PM"
                    elif int(self.timeDueListSplit[0]) == 0:
                        self.timeDueValue = "12" + ":" + self.timeDueMinute + " AM"
                    elif len(self.timeDueListSplit[0]) == 2:
                        self.timeDueValue = str(self.timeDueListSplit[0]) + ":" + self.timeDueMinute + " AM"
                    else:
                        self.timeDueValue = "0" + str(self.timeDueListSplit[0]) + ":" + self.timeDueMinute + " AM"
                else:
                    if int(self.timeDueListSplit[0]) - 12 == 12:
                        self.timeDueValue = str(int(self.timeDueListSplit[0]) - 12) + ":" + self.timeDueMinute + " AM"
                    else:
                        self.timeDueValue = str(int(self.timeDueListSplit[0]) - 12) + ":" + self.timeDueMinute + " PM"
                if len(self.dateDueListSplit[0]) == 1:
                    self.dateDueDay = '0' + str(self.dateDueListSplit[0])
                else:
                    self.dateDueDay = str(self.dateDueListSplit[0])
                if len(self.dateDueListSplit[1]) == 1:
                    self.dateDueMonth = '0' + str(self.dateDueListSplit[1])
                else:
                    self.dateDueMonth = str(self.dateDueListSplit[1])
                self.dueDateValue = monthFinder(int(self.dateDueListSplit[1])) + ' ' + self.dateDueDay + ' ' + \
                                    self.dateDueListSplit[2]
                self.assignmentDataDict.update({"TimeDue": self.timeDueValue})
                self.assignmentDataDict.update({"DateDue": self.dueDateValue})
                self.assignmentDataDict.update({"Description": self.description})
                self.assignmentDataDict.update({"Class": self.className})
                self.assignmentDataDict.update({"Complete": "False"})
                self.assignmentDataMainDict = {self.assignmentName: self.assignmentDataDict}
                self.user_data[user]['Assignments'].update(self.assignmentDataMainDict)
                sp.seek(0)
                sp.truncate()
                json.dump(self.user_data, sp, indent=4)
            createAssignment()


class createAssignments:
    def __init__(self, row, master, month, rowspan):
        global assignmentCounter
        self.assignmentCounter = assignmentCounter
        self.row = row
        self.master = master
        self.rowspan = rowspan
        self.month = str(month) + ", Month: " + monthFinder(month)
        self.frameAssignment = LabelFrame(master=self.master, text=self.month, font=('Georgia', 12, 'bold'), height=100,
                                          background='#333333', foreground='white')
        if self.rowspan == 8:
            self.textP1 = None
            self.textP2 = None
            self.frameAssignment.grid(column=0, row=self.row, columnspan=8, rowspan=self.rowspan, sticky='nsew',
                                      padx=15,
                                      pady=20)
            print('     Elongated Frame Assignment Created for: ' + str(month) + '\n' + "          Master: " + str(
                master))
            with open('user_data.json', 'r') as sp:
                self.user_data = json.load(sp)
                assignmentNamesList = [

                ]
                for assignmentsM, detailsM in self.user_data[user]['Assignments'].items():
                    assignmentNamesList.append(assignmentsM)
                self.details = self.user_data[user]['Assignments']
                print(assignmentCounter)
                self.textP1 = "Assignment: " + assignmentNamesList[assignmentCounter-2] + '\n' + "       Class: " + self.details[assignmentNamesList[assignmentCounter-1]]['Class'] + "\n" + "       Date Due: " + self.details[assignmentNamesList[assignmentCounter-2]]["DateDue"] + "\n" + "       Time Due: " + self.details[assignmentNamesList[assignmentCounter-2]]["TimeDue"] + "\n" + "       Description: " + self.details[assignmentNamesList[assignmentCounter-2]]['Description'] + '\n' + "       Completed: " + self.details[assignmentNamesList[assignmentCounter-2]]['Complete'] + '\n\n'
                self.textP2 = "Assignment: " + assignmentNamesList[assignmentCounter-1] + '\n' + "       Class: " + self.details[assignmentNamesList[assignmentCounter-2]]['Class'] + "\n" + "       Date Due: " + self.details[assignmentNamesList[assignmentCounter-1]]["DateDue"] + "\n" + "       Time Due: " + self.details[assignmentNamesList[assignmentCounter-1]]["TimeDue"] + "\n" + "       Description: " + self.details[assignmentNamesList[assignmentCounter-1]]['Description'] + '\n' + "       Completed: " + self.details[assignmentNamesList[assignmentCounter-1]]['Complete'] + '\n\n'
            self.assignmentInformationTextP1 = Text(master=self.frameAssignment, width=35, height=12, foreground='white', background='#2B2B2B', wrap=WORD)
            self.assignmentInformationTextP2 = Text(master=self.frameAssignment, width=35, height=12, foreground='white', background='#2B2B2B', wrap=WORD)
            self.assignmentsScrollbarP1 = ttk.Scrollbar(self.assignmentInformationTextP1, orient='vertical', command=self.assignmentInformationTextP1.yview)
            self.assignmentsScrollbarP2 = ttk.Scrollbar(self.assignmentInformationTextP2, orient='vertical', command=self.assignmentInformationTextP2.yview)
            self.assignmentInformationTextP1['state'] = 'normal'
            self.assignmentInformationTextP2['state'] = 'normal'
            self.assignmentInformationTextP1['yscrollcommand'] = self.assignmentsScrollbarP1.set
            self.assignmentInformationTextP1.delete('1.0', END)
            self.assignmentInformationTextP2.delete('1.0', END)
            self.assignmentInformationTextP1.insert('1.0', self.textP1)
            self.assignmentInformationTextP2.insert('1.0', self.textP2)
            self.assignmentInformationTextP2['yscrollcommand'] = self.assignmentsScrollbarP2.set
            self.assignmentsScrollbarP1.pack(fill='y', anchor='e', side='right', expand=True)
            self.assignmentsScrollbarP2.pack(fill='y', anchor='e', side='right', expand=True)
            self.assignmentInformationTextP1.place(relx=.1, rely=0)
            self.assignmentInformationTextP2.place(relx=.1, rely=.5)
            self.assignmentInformationTextP1['state'] = 'disabled'
            self.assignmentInformationTextP2['state'] = 'disabled'
            self.assignmentInformationTextP1.propagate(0)
            self.assignmentInformationTextP2.propagate(0)
        elif self.rowspan == 4:
            with open('user_data.json', 'r') as sp:
                self.user_data = json.load(sp)
                assignmentNamesList = [

                ]
                self.frameAssignment.grid(column=0, row=self.row, columnspan=8, rowspan=self.rowspan, sticky='nsew',
                                          padx=15,
                                          pady=20)
                for assignmentsM, detailsM in self.user_data[user]['Assignments'].items():
                    assignmentNamesList.append(assignmentsM)
                self.details = self.user_data[user]['Assignments']
                self.shortSpanText = "Assignment: " + assignmentNamesList[assignmentCounter - 1] + '\n' + self.details[assignmentNamesList[assignmentCounter-1]]['Class'] + "\n" + "       Date Due: " + \
                              self.details[assignmentNamesList[assignmentCounter - 1]][
                                  "DateDue"] + "\n" + "       Time Due: " + \
                              self.details[assignmentNamesList[assignmentCounter - 1]][
                                  "TimeDue"] + "\n" + "       Description: " + \
                              self.details[assignmentNamesList[assignmentCounter - 1]][
                                  'Description'] + '\n' + "       Completed: " + \
                              self.details[assignmentNamesList[assignmentCounter - 1]]['Complete'] + '\n\n'
                self.assignmentInformationShortSpanText = Text(master=self.frameAssignment, width=35, height=10,
                                                        foreground='white', background='#2B2B2B', wrap=WORD)
                self.assignmentsScrollbarShortSpanText = ttk.Scrollbar(self.assignmentInformationShortSpanText, orient='vertical',
                                                            command=self.assignmentInformationShortSpanText.yview)
                self.assignmentInformationShortSpanText['state'] = 'normal'
                self.assignmentInformationShortSpanText['yscrollcommand'] = self.assignmentsScrollbarShortSpanText.set
                self.assignmentInformationShortSpanText.delete('1.0', END)
                self.assignmentInformationShortSpanText.insert('1.0', self.shortSpanText)
                self.assignmentsScrollbarShortSpanText.pack(fill='y', anchor='e', side='right', expand=True)
                self.assignmentInformationShortSpanText.place(relx=.1, rely=0)
                self.assignmentInformationShortSpanText['state'] = 'disabled'
                self.assignmentInformationShortSpanText.propagate(0)
                print('     Frame Assignment Created for: ' + str(month) + '\n' + "          Master: " + str(master))
        else:
            print('Class createAssignment Error!')

class createHomeScreen():
    def __init__(self, master):
        loading(33)
        self.master = master
        self.mainFrame = ttk.Label(master=self.master, background='#333333')
        self.mainFrame.grid(column=0, row=0, sticky="nsew", columnspan=10, rowspan=10)
        self.mainFrame.grid_propagate(False)
        for i in range (0,10):
            self.mainFrame.rowconfigure(i, weight=weight_factor)
            self.mainFrame.columnconfigure(i, weight=weight_factor)
        self.pastDueFrameLabelFrame = LabelFrame(master=self.mainFrame, text='Past Due!', font=title_font, background='#2B2B2B', relief="sunken", foreground='white')
        self.dueSoonFrameLabelFrame = LabelFrame(master=self.mainFrame, text='Due Soon!', font=title_font, background='#2B2B2B', relief="sunken", foreground='white')
        self.dueNowLabelFrame = LabelFrame(master=self.mainFrame, text='Due Today!', font=title_font, background='#2B2B2B', relief="sunken", foreground='white')
        self.dueNowLabelFrame.grid_propagate(False)
        self.dueNowLabelFrame.grid(column=1, row=0, columnspan=8, rowspan=2, sticky='nsew', padx=15, pady=15)
        self.pastDueFrameLabelFrame.grid(row=2, column=1, columnspan=4, rowspan=8, sticky='nsew', padx=15, pady=15)
        self.pastDueFrameLabelFrame.grid_propagate(False)
        self.dueSoonFrameLabelFrame.grid(row=2, column=5, columnspan=4, rowspan=8, sticky='nsew', padx=15, pady=15)
        self.dueSoonFrameLabelFrame.grid_propagate(False)
        self.dueSoonText = Text(master=self.dueSoonFrameLabelFrame, wrap=WORD, height=30, width=29, font=main_font, foreground='white', background='#333333')
        self.pastDueText = Text(master=self.pastDueFrameLabelFrame, wrap=WORD, height=30, width=29, font=main_font, foreground='white', background='#333333')
        self.dueNowText = Text(master=self.dueNowLabelFrame, wrap=WORD, height=5, width=63, font=main_font, foreground='white', background='#333333')
        self.dueSoonText.grid(column=0, row=0, sticky='nsew', rowspan=1, columnspan=5, padx=8, pady=10)
        self.pastDueText.grid(column=0, row=0, sticky='nsew', rowspan=1, columnspan=5, padx=8, pady=10)
        self.dueNowText.grid(column=0, row=0, sticky='nsew', rowspan=3, columnspan=3, padx=10, pady=10)
        self.dueSoonTextData = ""
        self.pastDueTextData = ""
        self.dueNowTextData = ""
        loading(33)
        with open('user_data.json', 'r') as sp:
            user_data = json.load(sp)
            if 1 == 1:
                for assignment, detail in user_data[user]['Assignments'].items():
                    if assignment in dueNow():
                        if detail['Complete'] == 'True':
                            self.dueNowTextData += "Assigment ✅: " + assignment + "\n" + "       Date Due: " + detail[
                                "DateDue"] + "\n" + "       Time Due: " + detail["TimeDue"] + "\n" + "       Description: " + \
                                            detail['Description'] + '\n\n'
                        else:
                            self.dueNowTextData += "Assigment ❌: " + assignment + "\n" + "       Date Due: " + detail[
                                "DateDue"] + "\n" + "       Time Due: " + detail[
                                                       "TimeDue"] + "\n" + "       Description: " + \
                                                   detail['Description'] + '\n\n'
                for assignment, detail in user_data[user]['Assignments'].items():
                        if lateClassifier(assignment)[assignment] == 'Late':
                            if detail['Complete'] == 'True':
                                self.pastDueTextData += "Assigment ✅: " + assignment + "\n" + "       Date Due: " + detail[
                                    "DateDue"] + "\n" + "       Time Due: " + detail["TimeDue"] + "\n" + "       Description: " + \
                                                detail['Description'] + '\n\n'
                            else:
                                self.pastDueTextData += "Assigment ❌: " + assignment + "\n" + "       Date Due: " + detail[
                                    "DateDue"] + "\n" + "       Time Due: " + detail["TimeDue"] + "\n" + "       Description: " + \
                                                detail['Description'] + '\n\n'
                        else:
                            if lateClassifier(assignment)[assignment] == 'Not Late':
                                if detail['Complete'] == 'True':
                                    self.dueSoonTextData += "Assigment ✅: " + assignment + "\n" + "       Date Due: " + detail[
                                        "DateDue"] + "\n" + "       Time Due: " + detail[
                                                        "TimeDue"] + "\n" + "       Description: " + \
                                                    detail['Description'] + '\n\n'
                                else:
                                    self.dueSoonTextData += "Assigment ❌: " + assignment + "\n" + "       Date Due: " + detail[
                                        "DateDue"] + "\n" + "       Time Due: " + detail[
                                                        "TimeDue"] + "\n" + "       Description: " + \
                                                    detail['Description'] + '\n\n'
                self.pastDueText.insert('1.0', self.pastDueTextData)
                self.dueSoonText.insert('1.0', self.dueSoonTextData)
                self.dueNowText.insert('1.0', self.dueNowTextData)
                loading(33, False)



def getAssignmentTimeData():
    localTime = time.localtime()
    localTimeFormatted = time.strftime("%m/%d/%y", localTime)
    print(localTimeFormatted)

def lateClassifier(*assignment):
    usertime = time.localtime()
    usertimeFormatted = time.strftime("%Y %m %d %H %M")
    usertimeFormattedSorted = re.split(' ', usertimeFormatted)
    returnData = {}
    with open('user_data.json', 'r') as sp:
        user_data = json.load(sp)
        for arg in assignment:
            user_dataAssignment = user_data[user]['Assignments'][arg]
            completeDataList = [

            ]
            timeList = re.split('[/s: ]+', user_dataAssignment['TimeDue'])
            dateList = re.split(' ', user_dataAssignment['DateDue'])
            for d in dateList:
                try:
                    completeDataList.append(int(d))
                except:
                    completeDataList.append(int(monthIndexer(str(d))))
            completeDataList.append(int(timeList[1]))
            if timeList[2] == "AM":
                completeDataList.append(int(timeList[0]))
            else:
                completeDataList.append(int(timeList[0]) + 12)
            if int(completeDataList[2]) < int(usertimeFormattedSorted[0]):
                returnData.update({arg: "Late"})
                continue
            elif completeDataList[2] > int(usertimeFormattedSorted[0]):
                returnData.update({arg: "Not Late"})
                continue
            else:
                returnData.update({arg: "Not Late"})
            if completeDataList[0] < int(usertimeFormattedSorted[1]):
                returnData.update({arg: "Late"})
                continue
            elif completeDataList[0] > int(usertimeFormattedSorted[1]):
                returnData.update({arg: "Not Late"})
                continue
            else:
                returnData.update({arg: "Not Late"})
            if completeDataList[1] < int(usertimeFormattedSorted[2]):
                returnData.update({arg: "Late"})
                continue
            elif completeDataList[1] > int(usertimeFormattedSorted[2]):
                returnData.update({arg: "Not Late"})
                continue
            else:
                returnData.update({arg: "Not Late"})
            if completeDataList[4] < int(usertimeFormattedSorted[3]):
                returnData.update({arg: "Late"})
                continue
            elif completeDataList[4] > int(usertimeFormattedSorted[3]):
                returnData.update({arg: "Not Late"})
                continue
            else:
                returnData.update({arg: "Not Late"})
            if completeDataList[3] < int(usertimeFormattedSorted[4]):
                returnData.update({arg: "Late"})
                continue
            else:
                returnData.update({arg: "Not Late"})
                continue
    return(returnData)

def dueNow():
    usertime = time.localtime()
    usertimeFormatted = time.strftime("%Y %m %d %H %M")
    usertimeFormattedSorted = re.split(' ', usertimeFormatted)
    returnData = []
    with open('user_data.json', 'r') as sp:
        user_data = json.load(sp)
        for assignment, details in user_data[user]['Assignments'].items():
            user_dataAssignment = user_data[user]['Assignments'][assignment]
            completeDataList = [

            ]
            timeList = re.split('[/s: ]+', user_dataAssignment['TimeDue'])
            dateList = re.split(' ', user_dataAssignment['DateDue'])
            for d in dateList:
                try:
                    completeDataList.append(int(d))
                except:
                    completeDataList.append(int(monthIndexer(str(d))))
            completeDataList.append(int(timeList[1]))
            if timeList[2] == "AM":
                completeDataList.append(int(timeList[0]))
            else:
                completeDataList.append(int(timeList[0]) + 12)
            if int(completeDataList[2]) == int(usertimeFormattedSorted[0]) and completeDataList[0] == int(usertimeFormattedSorted[1]) and completeDataList[1] == int(usertimeFormattedSorted[2]):
                returnData.append(assignment)
    return(returnData)

# Home Screen
homeScreen = ttk.Label(master=main, background='blue')
homeScreen.grid_propagate(False)
testButton = ttk.Button(master=homeScreen, text='hey', command= lambda: lateClassifier("wdawdwad", "Spanish Quiz 2", 'Math Homework 5'))
testButton.grid(column=0, row=0, sticky='nsew')
homeScreen.grid(row=0, column=2, columnspan=8, rowspan=10, sticky='nsew')
for i in range(0, 10):
    homeScreen.columnconfigure(i, weight=weight_factor)
    homeScreen.rowconfigure(i, weight=weight_factor)

def changeHomeScreen():
    for children in homeScreen.winfo_children():
        children.destroy()
    createHomeScreen(master=homeScreen)
    homeScreen.lift()


def addAssignment(assignmentname, timedue, datedue, description, className):
    with open('user_data.json', 'r') as sp:
        user_data = json.load(sp)
        assignmentDict = {
            "TimeDue": timedue,
            "DateDue": datedue,
            "Description": description,
            "Class": className,
            "Complete": "True"
        }
        if assignmentname not in user_data[user]['Assignments']:
            user_data[user]['Assignments'].update({assignmentname, assignmentDict})
            sp.seek(0)
            sp.truncate()
            json.dump(user_data, sp, indent=4)
        else:
            print('Duplicate assignment name!')


def deleteAssignment(assignment):
    with open('user_data.json', 'r+') as sp:
        user_data = json.load(sp)
        del user_data[user]['Assignments'][assignment[:-2]]
        sp.seek(0)
        sp.truncate()
        json.dump(user_data, sp, indent=4)
    createAssignment()


def markAssignment(assignment, bool):
    try:
        with open('user_data.json', 'r+') as sp:
            user_data = json.load(sp)
            if bool:
                user_data[user]['Assignments'][assignment]['Complete'] = 'True'
            else:
                user_data[user]['Assignments'][assignment]['Complete'] = 'False'
            sp.seek(0)
            sp.truncate()
            json.dump(user_data, sp, indent=4)
    except:
        print("Unknown assignment")


def rightAssignments():
    global assignmentScreenList
    global yearFrameNum
    global assignmentCounter
    print("Assignment Counter: " + str(assignmentCounter))
    childrenCounter = 0
    for children in assignmentScreenList:
        childrenCounter += 1
    if yearFrameNum <= childrenCounter and yearFrameNum != 1:
        assignmentScreenList[::-1][yearFrameNum - 1].grid_forget()
        yearFrameNum -= 1
        assignmentScreenList[::-1][yearFrameNum - 1].grid(column=0, row=0, sticky="nsew", columnspan=11, rowspan=11)
        print(assignmentScreenList[::-1][yearFrameNum - 1])


def leftAssignments():
    global assignmentScreenList
    global yearFrameNum
    childrenCounter = 0
    for children in assignmentScreenList:
        childrenCounter += 1
    if yearFrameNum < childrenCounter:
        assignmentScreenList[::-1][yearFrameNum - 1].grid_forget()
        yearFrameNum += 1
        assignmentScreenList[::-1][yearFrameNum - 1].grid(column=0, row=0, sticky="nsew", columnspan=11, rowspan=11)


def createAssignment():
    global assignmentList
    global yearFrameNum
    global assignmentCounter
    global assignmentScreenList
    classesCheck = 0
    assignmentFrameBlock = ttk.LabelFrame()
    for i in recallclasses():
        classesCheck += 1
    if classesCheck == 100:
        assignmentFrameBlock.grid_propagate(False)
        assignmentFrameBlock.lift()
        frameBlockerText = ttk.Label(master=assignmentFrameBlock, text='No classes found, add a class first!', font=title_font)
        frameBlockerText.place(relx=.5, rely=.5, anchor='center')
        assignmentFrameBlock.grid(row=0, column=2, columnspan=8, rowspan=10, sticky='nsew')
        pass
    else:
        assignmentFrameBlock.grid_forget()
    assignmentScreenList = [

    ]
    yearFrameNum = 0
    monthFrameNum = 0
    dayFrameNum = 0
    monthindex = 0
    amtMonthCreated = 0
    monthSPECIFICCounter = 0
    monthInitializeEnlongate = 0.0
    assignmentCounter = 0
    stringResponse = ""
    initialize = True
    loading(0)
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
    dateMarker = [

    ]
    loading(25)
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
    loading(25)
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
        assignmentDateIndex.update({year: sorted(yearMonthList)})

    assignmentScreen.grid(row=0, column=2, columnspan=8, rowspan=10, sticky='nsew')
    assignmentScreen.lift()
    assignmentScreen.grid_propagate(False)
    loading(25)
    if initialize:
        yearFrameNum += 1
        createAssignmentScreen(master=assignmentScreen, text='Add an assignment!')
        initialize = False
    for year, months in assignmentDateIndex.items():
        dateMarker = [

        ]
        ##print("Assignment Date Index: " + str(assignmentDateIndex))
        monthIndex = 0
        monthFrameNum = 0
        print("New Year: " + '\n' + "    Year Frame NUM: " + str(yearFrameNum) + '\n' + "    monthList: " + str(
            monthList) + '\n' + "    yearDate: " + str(sorted(yearDate)) + '\n' + '     assignmentDateIndex: ' + str(
            assignmentDateIndex))
        for monthN in months:
            if monthInitializeEnlongate > 0.0:
                print("Skipped: " + str(monthN))
                monthInitializeEnlongate -= 0.5
                continue
            print("MonthN: " + str(monthN))
            monthIndex += 1
            if monthN not in dateMarker and monthFrameNum == 0 and monthSPECIFICCounter == 0:
                for monthsE in months:
                    if monthsE == monthN:
                        dateMarker.append(monthN)
                        monthSPECIFICCounter += 1
                        print(months)
                        if monthSPECIFICCounter % 2 == 0:
                            monthSPECIFICCounter -= 2
                            monthInitializeEnlongate += 1.0
                            print('\n' + "Elongate initialized! " + "Value: " + str(monthInitializeEnlongate))
            if monthInitializeEnlongate > 0:
                for amtNum in range(0, int(monthInitializeEnlongate)):
                    if initialize != False:
                        yearFrameNum += 1
                        createAssignmentScreen(master=assignmentScreen, text=year)
                    else:
                        initialize = True
                        assignmentList[yearFrameNum - 1]['text'] = year
                    createAssignments(row=monthFrameNum, master=assignmentList[yearFrameNum - 1], month=monthN,
                                      rowspan=8)
                    assignmentCounter += 2
                    ##print("    Assignment screen created for: " + "Year: " + str(year) + ", Month: " + str(monthN))
                    ##print("    Elongated Assignment for month, year created: " + str(monthN) + ", " + str(year) + '\n')
                monthInitializeEnlongate -= 0.5
            else:
                if monthSPECIFICCounter == 1:
                    monthSPECIFICCounter -= 1
                if monthFrameNum % 2 == 0:
                    ##print(stringResponse)
                    stringResponse = ""
                    monthFrameNum = 0
                    ##print("Assignment screen created for: " + "Year: " + str(year) + ", Month: " + str(
                    ##monthN) + ", monthSPECIFICCounter: " + str(monthSPECIFICCounter))
                    if initialize != False:
                        yearFrameNum += 1
                        createAssignmentScreen(master=assignmentScreen, text=year)
                    else:
                        initialize = True
                        assignmentList[yearFrameNum - 1]['text'] = year
                    # print("Assignment Screen List: " + str(assignmentScreenList))
                monthFrameNum += 1
                if monthFrameNum == 1:
                    print(assignmentList)
                    createAssignments(row=0, master=assignmentList[yearFrameNum - 1], month=monthN, rowspan=4)
                    assignmentCounter += 1
                else:
                    createAssignments(row=4, master=assignmentList[yearFrameNum - 1], month=monthN, rowspan=4)
                    assignmentCounter += 1
                #stringResponse += "    Assignment for month, year created: " + str(monthN) + ", " + str(year) + '\n'
                #stringResponse += "    Month Frame: " + str(monthFrameNum) + ", Year Frame Num: " + str(yearFrameNum) + '\n'
                #stringResponse += "    Assignment Screen List Index: " + str(assignmentScreenList[monthFrameNum-1]) + '\n'
                #stringResponse += "    Assignment Screen List: " + str(assignmentScreenList) + '\n'
    loading(25, False)


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
    className = addClassWidgets[0].get()
    classPeriod = addClassWidgets[1].get()
    errorLabel = addClassWidgets[2]
    intNum = False
    try:
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
    except:
        print("Add class error!")


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


def loading(step, continueLoading=True):
    global loadingscreen
    global progressionBar
    if continueLoading:
        progressionBar.step(step)
        loadingscreen.grid(column=0, row=0, columnspan=10, rowspan=10, sticky='nsew')
        loadingscreen.lift()
        loadingscreen.update()
    else:
        loadingscreen.lift()
        main.update_idletasks()
        loadingscreen.grid_forget()
        progressionBar['value'] = 0


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
    loading(25)
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
    loading(25)
    firsttime = True
    global classesScreenDict
    classesScreenDict = {}
    classFrameNum = 0
    recallclasses()
    addClassWidgets = [

    ]
    loading(25)
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
    loading(25, False)


def askchatGPT(text, textbox):
    try:
        response = Model.generate_content(text)
        textbox.configure(state='normal')
        textbox.delete('1.0', END)
        textbox.insert('1.0', response.text)
        textbox.configure(state='disabled')
    except:
        print('Content is empty!')


def changeloginscreentext(message):
    errormessage_loginmenu["text"] = message


def login():
    global user
    global homeScreen_menu
    global askAI_homescreen
    username = usernameentry_loginmenu.get()
    password = passwordentry_loginmenu.get()
    with open("user_data.json", 'r') as sp:
        userdata = json.load(sp)
        try:
            userpassword = userdata[index(username)]['Password']
            if userpassword == password:
                changeloginscreentext("Successfully logged in!")
                user = index(username)
                changeHomeScreen()
                homeScreen_menu.lift()
                askAI_homescreen.lift()
                login_menu.grid_forget()

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
    loading(33)
    main.update_idletasks()
    login_menu.grid(column=0, row=0, sticky='NSEW', columnspan=10, rowspan=10)
    loading(33)
    signupScreen.grid_forget()
    loading(33, False)


def findclassperiod(classtype):
    with open('user_data.json', 'r') as sp:
        userdata = json.load(sp)
        counter = 0
        for classes in userdata[user]['Classes']:
            if classtype == classes:
                return userdata[user]['Period'][counter]
            counter += 1


def changescreen_signupscreen():
    loading(50)
    signupscreengrid()
    loading(50, False)


def signupscreengrid():
    signupScreen.lift()
    signupScreen.grid(column=0, row=0, sticky='NSEW', columnspan=50, rowspan=50)

def logOut():
    global user
    user = None
    login_menu.lift()
    returnloginscreen()

# Home Screen
homeScreen_menu = ttk.Frame(main, padding=20, style='Card.TFrame', borderwidth=20, height=200)
homeButton_homeScreen = ttk.Button(homeScreen_menu, text='Home', style='Accent.TButton', width=40, command=changeHomeScreen)
assignmentsButton_homeScreen = ttk.Button(homeScreen_menu, text='Assignments', style='Accent.TButton', width=40,
                                          command=createAssignment)
classesButton_homeScreen = ttk.Button(homeScreen_menu, text='Classes', style='Accent.TButton', width=40,
                                      command=updateClasses)
calanderButton_homeScreen = ttk.Button(homeScreen_menu, text='Calendar', style='Accent.TButton', width=40)
profileButton_homeScreen = ttk.Button(homeScreen_menu, text='Profile', style='Accent.TButton', width=40)
logOutButton_homeScreen = ttk.Button(homeScreen_menu, text='Log Out', style='Accent.TButton', width=40, command=logOut)
mainScreen_homeScreen = ttk.Frame(main, style='Card.TFrame', borderwidth=10, height=100)
mainScreen_homeScreen.grid(row=0, column=2, sticky='nsew', columnspan=8, rowspan=10)
ignore_text = Text(master=mainScreen_homeScreen, width=50, height=20, borderwidth=20, background='gray',
                   font=main_font, state='disabled')
textInput_homeScreen = ttk.Entry(master=mainScreen_homeScreen, width=30)

HomeScreenIcon = tk.PhotoImage(file="smallerAppIcon.png")
appIcon_homescreen = ttk.Label(master=homeScreen_menu, image=HomeScreenIcon, background='#333333')
askAI_homescreen = ttk.Frame(master=main, height=10, width=20, style='Card.TFrame')
askAI_homescreen.grid(row=6, column=0, sticky='NSEW', columnspan=2, rowspan=4)
askAIText_homeScreen = Text(master=askAI_homescreen, width=15, height=10, background="#2B2B2B", foreground='white',
                            wrap=WORD)
askAI_homescreen.propagate(False)
for i in range(0, 6):
    askAI_homescreen.rowconfigure(i, weight=weight_factor)
    askAI_homescreen.columnconfigure(i, weight=weight_factor)
askAILabel = ttk.Label(master=askAI_homescreen, text='                      Ask an AI!', background='#2B2B2B',
                       font=('Georgia', 10, 'bold'), justify="center", foreground='white')
askAILabel.grid(row=1, column=2, columnspan=2, sticky='nsew')
askAIText_homeScreen.grid(row=2, column=1, sticky='nsew', pady=10, columnspan=4)
askAIEntry = ttk.Entry(master=askAI_homescreen, width=20, foreground='white')
askAIEntry.grid(row=3, column=1, columnspan=4)
askAIText_homeScreen.configure(state='disabled')
askAIButton = ttk.Button(master=askAI_homescreen, width=5, text='Ask AI!',
                         command=lambda: askchatGPT(askAIEntry.get(), askAIText_homeScreen), style='Accent.TButton')
askAIButton.grid(row=4, column=1, stick='ew', pady=5, columnspan=4)
appIcon_homescreen.grid(row=0, column=0)
logOutButton_homeScreen.grid(column=0, row=4, pady=15)
homeButton_homeScreen.grid(column=0, row=1, pady=15)
# profileButton_homeScreen.grid(column=0, row=5, pady=20)
# calanderButton_homeScreen.grid(column=0, row=4, pady=20)
classesButton_homeScreen.grid(column=0, row=3, pady=15)
assignmentsButton_homeScreen.grid(column=0, row=2, pady=15)
homeScreen_menu.grid(column=0, row=0, sticky='nsew', columnspan=2, rowspan=6)
homeScreen_menu.grid_propagate(False)

def disableAICall():
    askAIText_homeScreen['foreground'] = 'red'
    askAIText_homeScreen['state'] = 'normal'
    askAIText_homeScreen.insert(1.0, "AI CONFIGURATION FAILED!")
    askAIText_homeScreen['state'] = 'disabled'
    askAIEntry.configure(state='disabled')


if not AIConfigure:
    disableAICall()

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
signupScreen = ttk.Frame(master=main, style="Card.TFrame")
for i in range(0, 50):
    signupScreen.rowconfigure(i, weight=weight_factor)
    signupScreen.columnconfigure(i, weight=weight_factor)
signupScreen.columnconfigure(25, weight=5)
image = tk.PhotoImage(file="appIcon.png", master=login_menu)

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
passwordentry_signupscreen = ttk.Entry(master=signupScreen, foreground='white', width=30)
passwordentry_signupscreen.grid(column=25, row=20, sticky='e')
usernameentry_signupscreen = ttk.Entry(master=signupScreen, foreground='white', width=30)
usernameentry_signupscreen.grid(column=25, row=19, pady=5, sticky='e')
signupbutton_signupscreen = ttk.Button(master=signupScreen, style='Accent.TButton', text='Sign up', command=signup)
signupbutton_signupscreen.grid(column=25, row=22, sticky='ew', pady=5)
appLogo = ttk.Label(master=signupScreen, image=image, width=12, background='#333333')
appLogo.grid(column=25, row=18)
passwordlabel_signupscreen = ttk.Label(master=signupScreen, text='Password:', font=main_font, background='#333333',
                                       foreground='white', width=8)
passwordlabel_signupscreen.grid(column=25, row=20, sticky='w', padx=5)
usernamelabel_signupscreen = ttk.Label(master=signupScreen, text='Username: ', font=main_font, background='#333333',
                                       foreground='white', width=8)
usernamelabel_signupscreen.grid(column=25, row=19, sticky='w', padx=5)
returnlogin_signupscreen = ttk.Button(master=signupScreen, style='Accent.TButton', text='Return to login',
                                      command=returnloginscreen)
returnlogin_signupscreen.grid(column=25, row=23, sticky='ew', pady=5)
errormessage_signupscreen = ttk.Label(master=signupScreen, width=20, anchor="center", background="#333333",
                                      foreground='red', text='Insert a username and password!')
errormessage_signupscreen.grid(column=25, row=21, sticky='ew', pady=5)
# Classes Screen
classScreen = ttk.Frame(master=main, style='Card.TFrame')
# Classes Screen Configuration
for i in range(0, 6):
    classScreen.columnconfigure(i, weight=weight_factor)
    classScreen.rowconfigure(i, weight=weight_factor)
classScreen.grid_propagate(0)
# Loading Screen
loadingscreen = ttk.Frame(master=main, style='Card.TFrame')
progressionBar = ttk.Progressbar(master=loadingscreen, orient="horizontal", length=600)
progressionBar.place(rely=.6, relx=.5, anchor=CENTER)
appIconLoading = ttk.Label(master=loadingscreen, image=image, background='#333333')
appIconLoading.place(rely=.4, relx=.5, anchor=CENTER)

main.mainloop()