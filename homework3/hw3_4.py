from PIL import Image, ImageTk
import tkinter
import tkinter.messagebox
from tkinter.constants import *
import numpy as np
from statistics import median
from math import cos

window = None
ALL_NUM = 9
NUM_PER_ROW = 5

def ColorImage(color='R',num = 1):
    global LoadList, ImgList
    width, height = load.size
    for y in range(height):
        for x in range(width):
            rgba = load.getpixel((x,y))
            if color == 'R':
                rgba = (rgba[0], 0, 0)
            elif color == 'G':
                rgba = (0, rgba[1], 0)
            elif color == 'B':
                rgba = (0, 0, rgba[2])
            LoadList[num].putpixel((x,y), rgba)
    render = ImageTk.PhotoImage(LoadList[num])
    ImgList[num].config(image = render)
    ImgList[num].image = render

def RGBtoHSIGray(num1 = 4, num2 = 5,num3 = 6, num4 = 7):
    global ImgList, LoadList, load
    a, b = load.size
    pixel = LoadList[0].load()
    pixel1 = LoadList[num1].load()
    pixel2 = LoadList[num2].load()
    pixel3 = LoadList[num3].load()
	
    for x in range(LoadList[num1].size[0]):
        for y in range(LoadList[num1].size[1]):
            r,g,b = pixel[x,y]
            sita = 1/cos((0.5*(r-g)+(r-b))/((r-g)**2+(r-b)*(g-b))**(1/2))
            if b>g:
                pixel1[x,y]=(int(360-sita),int(360-sita),int(360-sita))
            else:
                pixel1[x,y]=(int(sita),int(sita),int(sita))

    for x in range(LoadList[num2].size[0]):
        for y in range(LoadList[num2].size[1]):
            r,g,b = pixel[x,y]
            sita = 1/cos((0.5*(r-g)+(r-b))/((r-g)**2+(r-b)*(g-b))**(1/2))
            pixel2[x,y]=(int(255*(1-((3/(r+g+b))*(min(r,g,b))))),int(255*(1-((3/(r+g+b))*(min(r,g,b))))),int(255*(1-((3/(r+g+b))*(min(r,g,b))))))

    for x in range(LoadList[num3].size[0]):
        for y in range(LoadList[num3].size[1]):
            r,g,b = pixel[x,y]
            sita = 1/cos((0.5*(r-g)+(r-b))/((r-g)**2+(r-b)*(g-b))**(1/2))
            pixel3[x,y]=(int((r+g+b)/3),int((r+g+b)/3),int((r+g+b)/3))

    for x in range(LoadList[num4].size[0]):
        for y in range(LoadList[num4].size[1]):
            rgba = (pixel1[x,y][0],pixel2[x,y][0],pixel3[x,y][0])
            LoadList[num4].putpixel((x,y), rgba)
    
    render1 = ImageTk.PhotoImage(LoadList[num1])
    render2 = ImageTk.PhotoImage(LoadList[num2])
    render3 = ImageTk.PhotoImage(LoadList[num3])
    render4 = ImageTk.PhotoImage(LoadList[num4])
    ImgList[num1].config(image = render1)
    ImgList[num2].config(image = render2)
    ImgList[num3].config(image = render3)
    ImgList[num4].config(image = render4)
    ImgList[num1].image = render1
    ImgList[num2].image = render2
    ImgList[num3].image = render3
    ImgList[num4].image = render4

def ColorComplement(num = 8):
    global ImgList, LoadList, load
    width, height = load.size
    for y in range(height):
            for x in range(width):
                rgba = load.getpixel((x,y))
                rgba = (255-rgba[0], 255-rgba[1], 255-rgba[2]);
                LoadList[num].putpixel((x,y), rgba)
    render = ImageTk.PhotoImage(LoadList[num])
    ImgList[num].config(image = render)
    ImgList[num].image = render

def Question4():
    global window, ImgList, render
    window = tkinter.Tk()
    window.title("Hw 3-4")

    LoadPicture()

    TitleList = [
        "Origin",
        "Red Component",
        "Green Component",
        "Blue Component",
        "Hue",
        "Saturation",
        "Intensity",
        "HSI",
        "ColorComplement"
    ]

    ColorImage("R", num= 1)
    ColorImage("G", num= 2)
    ColorImage("B", num= 3)
    RGBtoHSIGray()
    ColorComplement()

    for i in range(ALL_NUM):
        try:
            title = tkinter.Label(window, text=TitleList[i], font=("Arial",18))
        except IndexError:
            title = tkinter.Label(window, text="IndexError", font=("Arial",18))
        temp = 2*(i//5)
        title.grid(row=temp,column=i%5,padx=10,pady=2)
        ImgList[i].grid(row=temp+1,column=i%5,padx=10,pady=2)
        

    # size control
    window.geometry('1600x950')
    window.mainloop()

def LoadPicture():
    global window, ImgList, LoadList, render, load

    LoadList = []
    ImgList = []
    load = Image.open("Lenna_512_color.tif").resize((256,256))
    render = ImageTk.PhotoImage(load)
    for i in range(ALL_NUM):
        ImgList.append(tkinter.Label(window))
        LoadList.append(Image.open("Lenna_512_color.tif"))
        LoadList[i] = LoadList[i].resize((256,256))
        ImgList[i].config(image = render, width = 256, height = 256)
        ImgList[i].image = render


if __name__ == '__main__':
    Question4()