from PIL import Image, ImageTk, ImageFilter
import tkinter
import tkinter.messagebox
from tkinter.constants import *
import numpy as np
from math import cos

window = None
ALL_NUM = 15
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
            rgba = (255-pixel1[x,y][0],255-pixel2[x,y][0],255-pixel3[x,y][0])
            #LoadList[num1].putpixel((x,y), (rgba[0],rgba[0],rgba[0]))
            #LoadList[num2].putpixel((x,y), (rgba[1],rgba[1],rgba[1]))
            #LoadList[num3].putpixel((x,y), (rgba[2],rgba[2],rgba[2]))
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

def Enhance(num = 9):
	global LoadList, ImgList
	LoadList[num] = LoadList[num].filter(ImageFilter.SHARPEN)
	render = ImageTk.PhotoImage(LoadList[num])
	ImgList[num].config(image = render)
	ImgList[num].image = render

def SharpenFilter5x5(tar = 0, num = 10):
    global LoadList, ImgList
    loaded = LoadList[tar]
    pixel = LoadList[tar].load()
    np_r, np_g, np_b = [],[],[]
    dt = np.dtype(np.float64)

    for x in range(loaded.size[0]):
        arr_r = []
        arr_g = []
        arr_b = []
        for y in range(loaded.size[1]):
            arr_r.append(pixel[x,y][0])
            arr_g.append(pixel[x,y][1])
            arr_b.append(pixel[x,y][2])
        np_r.append(arr_r.copy())
        np_g.append(arr_g.copy())
        np_b.append(arr_b.copy())
    np_r = np.array(np_r, dt)
    np_g = np.array(np_g, dt)
    np_b = np.array(np_b, dt)

    np_r = np.c_[np_r,np.zeros((loaded.size[1],2))]
    np_r = np.c_[np.zeros((loaded.size[1],2)),np_r]
    np_r = np.r_[np.zeros((2,loaded.size[0]+4)),np_r]
    np_r = np.r_[np_r,np.zeros((2,loaded.size[0]+4))]

    np_g = np.c_[np_g,np.zeros((loaded.size[1],2))]
    np_g = np.c_[np.zeros((loaded.size[1],2)),np_g]
    np_g = np.r_[np.zeros((2,loaded.size[0]+4)),np_g]
    np_g = np.r_[np_g,np.zeros((2,loaded.size[0]+4))]

    np_b = np.c_[np_b,np.zeros((loaded.size[1],2))]
    np_b = np.c_[np.zeros((loaded.size[1],2)),np_b]
    np_b = np.r_[np.zeros((2,loaded.size[0]+4)),np_b]
    np_b = np.r_[np_b,np.zeros((2,loaded.size[0]+4))]

    _np_r = np_r.copy()
    _np_g = np_g.copy()
    _np_b = np_b.copy()
            
    for x in range(1,loaded.size[0]+1):
        for y in range(1,loaded.size[1]+1):
            temp_r = 0
            temp_g = 0
            temp_b = 0

            temp_r = 16*np_r[x][y] - 2*(np_r[x][y-1] + np_r[x][y+1] + np_r[x+1][y] + np_r[x-1][y])
            temp_r -= np_r[x][y-2] + np_r[x][y+2] + np_r[x+2][y] + np_r[x-2][y] + np_r[x-1][y-1] + np_r[x+1][y-1] + np_r[x+1][y+1] + np_r[x-1][y+1]
            
            temp_b = 16*np_b[x][y] - 2*(np_b[x][y-1] + np_b[x][y+1] + np_b[x+1][y] + np_b[x-1][y])
            temp_b -= np_b[x][y-2] + np_b[x][y+2] + np_b[x+2][y] + np_b[x-2][y] + np_b[x-1][y-1] + np_b[x+1][y-1] + np_b[x+1][y+1] + np_b[x-1][y+1]

            temp_g = 16*np_g[x][y] - 2*(np_g[x][y-1] + np_g[x][y+1] + np_g[x+1][y] + np_g[x-1][y])
            temp_g -= np_g[x][y-2] + np_g[x][y+2] + np_g[x+2][y] + np_g[x-2][y] + np_g[x-1][y-1] + np_g[x+1][y-1] + np_g[x+1][y+1] + np_g[x-1][y+1]

            _np_r[x][y] = round( temp_r )
            _np_g[x][y] = round( temp_g )
            _np_b[x][y] = round( temp_b )

    for x in range(2,loaded.size[0]+2):
        for y in range(2,loaded.size[1]+2):
            LoadList[num].putpixel((x-2,y-2) , (int(_np_r[x][y]),int(_np_g[x][y]),int(_np_b[x][y])) )
    render = ImageTk.PhotoImage(LoadList[num])
    ImgList[num].config(image = render)
    ImgList[num].image = render

def SmoothFilter5x5(tar = 0, num = 12):
    global LoadList, ImgList
    loaded = LoadList[tar]
    pixel = LoadList[tar].load()
    np_r, np_g, np_b = [],[],[]
    dt = np.dtype(np.float64)

    for x in range(loaded.size[0]):
        arr_r = []
        arr_g = []
        arr_b = []
        for y in range(loaded.size[1]):
            arr_r.append(pixel[x,y][0])
            arr_g.append(pixel[x,y][1])
            arr_b.append(pixel[x,y][2])
        np_r.append(arr_r.copy())
        np_g.append(arr_g.copy())
        np_b.append(arr_b.copy())
    np_r = np.array(np_r, dt)
    np_g = np.array(np_g, dt)
    np_b = np.array(np_b, dt)

    np_r = np.c_[np_r,np.zeros((loaded.size[1],2))]
    np_r = np.c_[np.zeros((loaded.size[1],2)),np_r]
    np_r = np.r_[np.zeros((2,loaded.size[0]+4)),np_r]
    np_r = np.r_[np_r,np.zeros((2,loaded.size[0]+4))]

    np_g = np.c_[np_g,np.zeros((loaded.size[1],2))]
    np_g = np.c_[np.zeros((loaded.size[1],2)),np_g]
    np_g = np.r_[np.zeros((2,loaded.size[0]+4)),np_g]
    np_g = np.r_[np_g,np.zeros((2,loaded.size[0]+4))]

    np_b = np.c_[np_b,np.zeros((loaded.size[1],2))]
    np_b = np.c_[np.zeros((loaded.size[1],2)),np_b]
    np_b = np.r_[np.zeros((2,loaded.size[0]+4)),np_b]
    np_b = np.r_[np_b,np.zeros((2,loaded.size[0]+4))]

    _np_r = np_r.copy()
    _np_g = np_g.copy()
    _np_b = np_b.copy()
            
    for x in range(1,LoadList[tar].size[0]+1):
        for y in range(1,LoadList[tar].size[1]+1):
            temp_r = 0
            temp_g = 0
            temp_b = 0
            for i in (0,1,-1,2,-2):
                for j in (0,1,-1,2,-2):
                    temp_r += np_r[x+i][y+j]
                    temp_g += np_g[x+i][y+j]
                    temp_b += np_b[x+i][y+j]
            _np_r[x][y] = round( temp_r/25 )
            _np_g[x][y] = round( temp_g/25 )
            _np_b[x][y] = round( temp_b/25 )

    for x in range(2,loaded.size[0]+2):
        for y in range(2,loaded.size[1]+2):
            LoadList[num].putpixel((x-2,y-2) , (int(_np_r[x][y]),int(_np_g[x][y]),int(_np_b[x][y])) )
    render = ImageTk.PhotoImage(LoadList[num])
    ImgList[num].config(image = render)
    ImgList[num].image = render

def ProperMask(num = 14):
    global LoadList, ImgList, load
    hue,sat,intense = LoadList[4], LoadList[5], LoadList[6]
    h_load, s_load, i_load = hue.load(), sat.load(), intense.load()

    for x in range(LoadList[0].size[0]):
        for y in range(LoadList[0].size[1]):
            if h_load[x,y][0]!=0 and s_load[x,y][0]>125 :
                LoadList[num].putpixel( (x,y), (255,255,255) )
            else:
                LoadList[num].putpixel((x,y), (0,0,0))
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
        "ColorComplement",
        "RGB Enhance",
        "RGB Sharpen Filter 5x5",
        "HSI Sharpen Filter 5x5",
        "RGB Smoothing Filter 5x5",
        "HSI Smoothing Filter 5x5",
        "Proper Mask (Hue=0, Saturation>125)"
    ]

    ColorImage("R", num= 1)
    ColorImage("G", num= 2)
    ColorImage("B", num= 3)
    RGBtoHSIGray()
    ColorComplement()
    Enhance()
    SharpenFilter5x5(tar=0 , num=10)
    SharpenFilter5x5(tar=7 , num=11)
    SmoothFilter5x5(tar=0 , num=12)
    SmoothFilter5x5(tar=7 , num=13)
    ProperMask(num = 14)

    for i in range(ALL_NUM):
        try:
            title = tkinter.Label(window, text=TitleList[i], font=("Arial",18))
        except IndexError:
            title = tkinter.Label(window, text="IndexError", font=("Arial",18))
        temp = 2*(i//5)

        if i==14:
            title = tkinter.Label(window, text=TitleList[i], font=("Arial",12))

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