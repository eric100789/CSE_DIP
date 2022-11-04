from PIL import Image, ImageTk
import tkinter
import tkinter.messagebox
from tkinter.constants import *
import numpy as np
from statistics import median

window = None

def LoadPicture():
    global img, img1, img2, img3, img4, load, load1, load2, load3, load4, pixel, window, render
    load = None
    load1 = None
    load2 = None
    load3 = None
    load4 = None
    pixel = None
    img = tkinter.Label(window)
    img1 = tkinter.Label(window)
    img2 = tkinter.Label(window)
    img3 = tkinter.Label(window)
    img4 = tkinter.Label(window)
    load1 = Image.open("BarTest.tif")
    load2 = Image.open("BarTest.tif")
    load3 = Image.open("BarTest.tif")
    load4 = Image.open("BarTest.tif")
    load = Image.open("Bartest.tif")
    pixel = load.load()
    render = ImageTk.PhotoImage(load)
    img.config(image = render, width = 300, height = 300)
    img.image = render
    img1.config(image = render, width = 300, height = 300)
    img1.image = render
    img2.config(image = render, width = 300, height = 300)
    img2.image = render
    img3.config(image = render, width = 300, height = 300)
    img3.image = render
    img4.config(image = render, width = 300, height = 300)
    img4.image = render

def MeanFilter7x7():
    global load1,img1
    nparr = []
    dt = np.dtype(np.float64)

    for x in range(load1.size[0]):
        arr = []
        for y in range(load1.size[1]):
            arr.append(load1.getpixel((x, y)))
        nparr.append(arr.copy())
    nparr = np.array(nparr, dt)

    nparr = np.c_[nparr,np.zeros((load1.size[1],3))]
    nparr = np.c_[np.zeros((load1.size[1],3)),nparr]
    nparr = np.r_[np.zeros((3,load1.size[0]+6)),nparr]
    nparr = np.r_[nparr,np.zeros((3,load1.size[0]+6))]

    _nparr = nparr.copy()
            
    for x in range(1,load1.size[0]+1):
        for y in range(1,load1.size[1]+1):
            temp = 0
            for i in (0,1,-1,2,-2,3,-3):
                for j in (0,1,-1,2,-2,3,-3):
                    temp += nparr[x+i][y+j]
            _nparr[x][y] = round( temp/49 )

    new_img = load1.load()

    for x in range(1,load1.size[0]+1):
        for y in range(1,load1.size[1]+1):
            new_img[x-1,y-1] = int(_nparr[x][y])
    render = ImageTk.PhotoImage(load1)
    img1.config(image = render)
    img1.image = render

def MeanFilter3x3():
    global load2,img2
    nparr = []
    dt = np.dtype(np.float64)

    for x in range(load2.size[0]):
        arr = []
        for y in range(load2.size[1]):
            arr.append(load2.getpixel((x, y)))
        nparr.append(arr.copy())
    nparr = np.array(nparr, dt)
    nparr = np.c_[nparr,np.zeros((load2.size[1],1))]
    nparr = np.c_[np.zeros((load2.size[1],1)),nparr]
    nparr = np.r_[np.zeros((1,load2.size[0]+2)),nparr]
    nparr = np.r_[nparr,np.zeros((1,load2.size[0]+2))]
    _nparr = nparr.copy()
            
    for x in range(1,load2.size[0]+1):
        for y in range(1,load2.size[1]+1):
            _nparr[x][y] = round((nparr[x][y]+nparr[x-1][y]+nparr[x+1][y]+nparr[x+1][y+1]+nparr[x-1][y-1]+nparr[x][y+1]+nparr[x][y-1]+nparr[x-1][y+1]+nparr[x+1][y-1])/9)

    new_img = load2.load()

    for x in range(1,load2.size[0]+1):
        for y in range(1,load2.size[1]+1):
            new_img[x-1,y-1] = int(_nparr[x][y])
    render = ImageTk.PhotoImage(load2)
    img2.config(image = render)
    img2.image = render

def MedianFilter7x7():
    global load3,img3
    nparr = []
    dt = np.dtype(np.float64)

    for x in range(load3.size[0]):
        arr = []
        for y in range(load3.size[1]):
            arr.append(load3.getpixel((x, y)))
        nparr.append(arr.copy())
    nparr = np.array(nparr, dt)

    nparr = np.c_[nparr,np.zeros((load3.size[1],3))]
    nparr = np.c_[np.zeros((load3.size[1],3)),nparr]
    nparr = np.r_[np.zeros((3,load3.size[0]+6)),nparr]
    nparr = np.r_[nparr,np.zeros((3,load3.size[0]+6))]

    _nparr = nparr.copy()
            
    for x in range(1,load3.size[0]+1):
        for y in range(1,load3.size[1]+1):
            temp = []
            for i in (0,1,-1,2,-2,3,-3):
                for j in (0,1,-1,2,-2,3,-3):
                    temp.append(nparr[x+i][y+j])
            _nparr[x][y] = round(median(temp))

    new_img = load3.load()

    for x in range(1,load3.size[0]+1):
        for y in range(1,load3.size[1]+1):
            new_img[x-1,y-1] = int(_nparr[x][y])
    render = ImageTk.PhotoImage(load3)
    img3.config(image = render)
    img3.image = render

def MedianFilter3x3():
    global load4,img4
    nparr = []
    dt = np.dtype(np.float64)

    for x in range(load4.size[0]):
        arr = []
        for y in range(load4.size[1]):
            arr.append(load4.getpixel((x, y)))
        nparr.append(arr.copy())
    nparr = np.array(nparr, dt)
    nparr = np.c_[nparr,np.zeros((load4.size[1],1))]
    nparr = np.c_[np.zeros((load4.size[1],1)),nparr]
    nparr = np.r_[np.zeros((1,load4.size[0]+2)),nparr]
    nparr = np.r_[nparr,np.zeros((1,load4.size[0]+2))]
    _nparr = nparr.copy()
            
    for x in range(1,load4.size[0]+1):
        for y in range(1,load4.size[1]+1):
            _nparr[x][y] = round(median([nparr[x][y],nparr[x-1][y],nparr[x+1][y],nparr[x+1][y+1],nparr[x-1][y-1],nparr[x][y+1],nparr[x][y-1],nparr[x-1][y+1],nparr[x+1][y-1]]))

    new_img = load4.load()

    for x in range(1,load4.size[0]+1):
        for y in range(1,load4.size[1]+1):
            new_img[x-1,y-1] = int(_nparr[x][y])
    render = ImageTk.PhotoImage(load4)
    img4.config(image = render)
    img4.image = render

def Question1():
    global window, render
    window = tkinter.Tk()
    window.title("Hw 3-1")

    LoadPicture()
    MeanFilter7x7()
    MeanFilter3x3()
    MedianFilter7x7()
    MedianFilter3x3()

    title = tkinter.Label(window, text = "Origin", font=("Arial",18))
    title1 = tkinter.Label(window, text = "7x7 arithmetic mean filter", font=("Arial",18))
    title2 = tkinter.Label(window, text = "3x3 arithmetic mean filter", font=("Arial",18))
    title3 = tkinter.Label(window, text = "7x7 median filter", font=("Arial",18))
    title4 = tkinter.Label(window, text = "3x3 median filter", font=("Arial",18))
    title.grid(row=0,column=1,padx=10,pady=2)
    title1.grid(row=0,column=2,padx=10,pady=2)
    title2.grid(row=0,column=3,padx=10,pady=2)
    title3.grid(row=0,column=4,padx=10,pady=2)
    title4.grid(row=0,column=5,padx=10,pady=2)
    img.grid(row=1,column=1,padx=10,pady=2)
    img1.grid(row=1,column=2,padx=10,pady=2)
    img2.grid(row=1,column=3,padx=10,pady=2)
    img3.grid(row=1,column=4,padx=10,pady=2)
    img4.grid(row=1,column=5,padx=10,pady=2)

    # size control
    window.geometry('1620x400')
    window.mainloop()

if __name__ == '__main__':
    Question1()