import tkinter
import tkinter.messagebox
from tkinter.constants import *
from hw3_1 import Question1

def BarTest():
    tkinter.messagebox.showinfo(title = 'Running', message = "請稍等至視窗跳出")
    window.destroy()
    Question1()

def Lenna():
    pass

def DIPimg():
    pass

def LennaColor():
    pass

if __name__ == '__main__':
    print("main.py is ready")

    # create a new window
    window = tkinter.Tk()
    window.title("Homework 3")

    # size control
    window.geometry('190x400')

    lbl_title = tkinter.Label(window, text = "Homework 3", font=("Arial",18))
    
    button1 = tkinter.Button(window, text = 'Question 1', bg = 'light cyan', font = ('Arial', 18), width = 10, height = 1, command = BarTest)
    button2 = tkinter.Button(window, text = 'Question 2', bg = 'light cyan', font = ('Arial', 18), width = 10, height = 1, command = Lenna)
    button3 = tkinter.Button(window, text = 'Question 3', bg = 'light cyan', font = ('Arial', 18), width = 10, height = 1, command = DIPimg)
    button4 = tkinter.Button(window, text = 'Question 4', bg = 'light cyan', font = ('Arial', 18), width = 10, height = 1, command = LennaColor)

    lbl_title.place(x=10, y=0)
    button1.place(x = 20, y = 50)
    button2.place(x = 20, y = 125)
    button3.place(x = 20, y = 200)
    button4.place(x = 20, y = 275)

    window.mainloop()
    
