from configparser import Interpolation
from distutils.cmd import Command
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
import tkinter
import tkinter.messagebox
from tkinter.constants import *
from math import exp,log
import matplotlib.pyplot as plt
import cv2

# used _img_tk to save img which is adjusted by users
_img_tk = None
# save adjusted data to make users can have lots of setting 
Picture_data = {
    "enhance" : (-1,-1,-1),
    "rotate" : 0,
    "size" : 1,
    "upper": 0,
    "lower": 0,
    "graySlice": False,
    "preserve": False
}

def setPicture(enhance=None, rotate=None, size=None, upper=None, lower=None, graySlice=None, save=None, name=None):
    global lbl_picture,img,window,_img_tk,Picture_data

    if(enhance):
        Picture_data["enhance"] = enhance
    if(rotate):
        Picture_data["rotate"] = rotate
    if(size):
        Picture_data["size"] = size
    if(graySlice == True):
        if(upper == None or lower == None):
            raise(SyntaxError)
        else:
            Picture_data["upper"] = upper
            Picture_data["lower"] = lower
            Picture_data["graySlice"] = True
    elif(graySlice == False):
        Picture_data["graySlice"] = False


    if(Picture_data["enhance"][2] == -1):
        pass

    elif(Picture_data["enhance"][2] == 1):
        _img = Image.new("L", (img.size[0], img.size[1]))
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                val = Picture_data["enhance"][0] * img.getpixel((x, y)) + Picture_data["enhance"][1]
                if val >= 255:
                    val = 255
                if val <= 0:
                    val = 0
                _img.putpixel((x, y), int(val))

    elif(Picture_data["enhance"][2] == 2):
        _img = Image.new("L", (img.size[0], img.size[1]))
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                val = exp(Picture_data["enhance"][0]) * img.getpixel((x, y)) + Picture_data["enhance"][1]
                if val >= 255:
                    val = 255
                if val <= 0:
                    val = 0
                _img.putpixel((x, y), int(val))

    elif(Picture_data["enhance"][2] == 3):
        _img = Image.new("L", (img.size[0], img.size[1]))
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                val = log(Picture_data["enhance"][0]) * img.getpixel((x, y)) + Picture_data["enhance"][1]
                if val >= 255:
                    val = 255
                if val <= 0:
                    val = 0
                _img.putpixel((x, y), int(val))

    _img = _img.rotate(Picture_data["rotate"])

    if(Picture_data["graySlice"]):
        sliced_img = Image.new("L", (_img.size[0], _img.size[1]))
        for x in range(_img.size[0]):
            for y in range(_img.size[1]):
                val = _img.getpixel((x, y))
                if val >= Picture_data["lower"] and val <= Picture_data["upper"]:
                    val = 255
                elif not Picture_data["preserve"]:
                    val = 0
                sliced_img.putpixel((x, y), int(val))
        _img = sliced_img

    if(size and not save):
        new_img = _img.resize((int(300*Picture_data["size"]),int(300*Picture_data["size"])))
        new_img.show()

    if(save):
        new_img = _img.resize((int(300*Picture_data["size"]),int(300*Picture_data["size"])))
        if(not name):
            name = "NoName"
        new_img.save(name+".jpg")
        tkinter.messagebox.showinfo(title = 'Nice! My Homework done.', message = "file saved")  
        


    _img_tk = ImageTk.PhotoImage(_img)

    lbl_picture = tkinter.Label(window, image=_img_tk)
    lbl_picture.grid(row=100,column=2)

def ClickLinButton(button,a,b):
    try:
        setPicture(enhance = (float(a),float(b),1) )
    except:
        msg = "Please input floating number"
        tkinter.messagebox.showerror(title = 'Error:Enhance', message = msg)  

def ClickExpButton(button,a,b):
    try:
        setPicture(enhance=(float(a),float(b),2))
    except:
        msg = "Please input floating number"
        tkinter.messagebox.showerror(title = 'Error:Enhance', message = msg)  

def ClickLogButton(button,a,b):
    try:
        setPicture(enhance=(float(a),float(b),3))
    except:
        msg = "Please input floating number"
        tkinter.messagebox.showerror(title = 'Error:Enhance', message = msg)  

def ClickRotateButton(degree):
    try:
        setPicture(rotate=float(degree))
    except:
        msg = "Please input floating number"
        tkinter.messagebox.showerror(title = 'Error:Rotate', message = msg)  

def ClickZoomButton(size):
    try:
        setPicture(size=float(size))
    except:
        msg = "Please input floating number"
        tkinter.messagebox.showerror(title = 'Error:Zoom', message = msg) 

def ClickSliceOff(lower,upper):
    try:
        setPicture(lower=int(lower), upper=int(upper), graySlice=True)
        but_slic = tkinter.Button(window, text= "On", command=lambda: ClickSliceOn(ent_slic_lower.get(),ent_slic_upper.get()))
        but_slic.grid(row=10, column=1)

    except:
        msg = "Please input integer number"
        tkinter.messagebox.showerror(title = 'Error:GreySlicing', message = msg) 

def ClickSliceOn(lower,upper):
    setPicture(lower=int(lower), upper=int(upper), graySlice=False)
    but_slic = tkinter.Button(window, text= "Off", command=lambda: ClickSliceOff(ent_slic_lower.get(),ent_slic_upper.get()))
    but_slic.grid(row=10, column=1)

def ClickSlicePreserveOff():
    Picture_data["preserve"] = True
    but_slic_preserve = tkinter.Button(window, text= "On", command=lambda: ClickSlicePreserveOn())
    but_slic_preserve.grid(row=10, column=2)
    but_slic = tkinter.Button(window, text= "Off", command=lambda: ClickSliceOff(ent_slic_lower.get(),ent_slic_upper.get()))
    but_slic.grid(row=10, column=1)

def ClickSlicePreserveOn():
    Picture_data["preserve"] = False
    but_slic_preserve = tkinter.Button(window, text= "Off", command=lambda: ClickSlicePreserveOff())
    but_slic_preserve.grid(row=10, column=2)
    but_slic = tkinter.Button(window, text= "Off", command=lambda: ClickSliceOff(ent_slic_lower.get(),ent_slic_upper.get()))
    but_slic.grid(row=10, column=1)

def ClickSaveButton(name, size):
    try:
        setPicture(save=True, name=name, size=int(size))
    except:
        setPicture(save=True, name=name)

if __name__ == '__main__':
    print("main.py is ready")

    # create a new window
    window = tkinter.Tk()
    window.title("Homework 1")

    # size control
    window.geometry('800x700')

    # image loading
    img = Image.open("LennaGray256.jpg")
    img_tk = ImageTk.PhotoImage(img)

    # title
    lbl_title = tkinter.Label(window, text = "Homework 1", font=("Arial",18))
    lbl_title.grid(row=0,column=1)

    # show picture
    lbl_picture = tkinter.Label(window, image=img_tk)
    lbl_picture.grid(row=100,column=2)

    # input a
    lbl_a = tkinter.Label(window, text = "Please input your a:", font=("Arial",9))
    ent_a = tkinter.Entry(window, width=20)
    
    lbl_a.grid(row=2,column=1,pady=5)
    ent_a.grid(row=2,column=2)

    # input b
    lbl_b = tkinter.Label(window, text = "Please input your b:", font=("Arial",9))
    ent_b = tkinter.Entry(window, width=20)
    
    lbl_b.grid(row=3,column=1)
    ent_b.grid(row=3,column=2)

    # button and its functions
    but_line = tkinter.Button(window, text="Linearly", command=lambda:ClickLinButton(but_line, ent_a.get(), ent_b.get()))
    but_exp = tkinter.Button(window, text="Exponentially", command=lambda:ClickExpButton(but_line, ent_a.get(), ent_b.get()))
    but_log = tkinter.Button(window, text="Logarithmically", command=lambda:ClickLogButton(but_line, ent_a.get(), ent_b.get()))
    
    but_line.grid(row=5,column=1,padx=20,pady=5)
    but_exp.grid(row=5, column=2,padx=20,pady=5)
    but_log.grid(row=5, column=3,padx=20,pady=5)

    # room and buttons
    lbl_zoom = tkinter.Label(window, text = "Input zoom size:", font=("Arial",9))
    ent_zoom = tkinter.Entry(window, width=20)

    lbl_zoom.grid(row=6, column=1,pady=5)
    ent_zoom.grid(row=6,column=2)
    but_zoom = tkinter.Button(window, text="Zoom", command=lambda:ClickZoomButton(ent_zoom.get()))
    but_zoom.grid(row=6, column=3,padx=20,pady=5)

    # rotation and buttons
    lbl_rot = tkinter.Label(window, text = "Input roation degree:", font=("Arial",9))
    ent_rot = tkinter.Entry(window, width=20)

    lbl_rot.grid(row=7, column=1,pady=5)
    ent_rot.grid(row=7,column=2)
    but_rot = tkinter.Button(window, text="Rotation", command=lambda:ClickRotateButton(ent_rot.get()))
    but_rot.grid(row=7, column=3,padx=20,pady=5)
    
    # gray slicing
    lbl_slic = tkinter.Label(window, text = "Gray Slicing (On/Off)", font=("Arial",9))
    but_slic = tkinter.Button(window, text= "Off", command=lambda: ClickSliceOff(ent_slic_lower.get(),ent_slic_upper.get()))
    lbl_slic_upper = tkinter.Label(window, text = "Upper", font=("Arial",9))
    ent_slic_upper = tkinter.Entry(window, width=10)
    lbl_slic_lower = tkinter.Label(window, text = "Lower", font=("Arial",9))
    ent_slic_lower = tkinter.Entry(window, width=10)
    lbl_slic_preserve = tkinter.Label(window, text = "Preserve (On/Off)", font=("Arial",9))
    but_slic_preserve = tkinter.Button(window, text= "Off", command=lambda: ClickSlicePreserveOff())

    lbl_slic.grid(row=8, column=1, padx= 10, pady=5)
    but_slic.grid(row=10, column=1)
    but_slic_preserve.grid(row=10, column=2)
    lbl_slic_preserve.grid(row=8, column=2, padx= 10, pady=5)
    lbl_slic_lower.grid(row=8, column=3, padx= 10, pady=5)
    lbl_slic_upper.grid(row=8, column=4, padx= 10, pady=5)
    ent_slic_lower.grid(row=10, column=3, padx= 10, pady=5)
    ent_slic_upper.grid(row=10, column=4, padx= 10, pady=5)

    # save button
    lbl_save = tkinter.Label(window, text = "Input Picture Name:", font=("Arial",9))
    ent_save = tkinter.Entry(window, width=20)
    but_save = tkinter.Button(window, text = "Save", command=lambda: ClickSaveButton(ent_save.get(), ent_zoom.get()))

    lbl_save.grid(row=12, column=1, padx= 10, pady=5)
    ent_save.grid(row=12, column=2, padx= 10, pady=5)
    but_save.grid(row=13, column=1, padx=30)
    

    # draw the window, and start the application
    window.mainloop()
    
    