from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.constants import *
from math import exp,log
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import values
from statistics import median

load = None
_load = None
pixel = None

def ClickOpen():#function for opening file
    global img, _img, load, _load, pixel
    name = fd.askopenfilename()
    if name[-3:] == "raw":
        with open(name, 'rb') as f:
            name = Image.frombytes("L", (512, 512), f.read(), 'raw')
        _load = name
        load = name.copy()
        pixel = load.load()
        render = ImageTk.PhotoImage(load)
        img.config(image = render, width = 512, height = 512)
        img.image = render
        _img.config(image = render, width = 512, height = 512)
        _img.image = render
    else:
        _load = Image.open(name)
        load = Image.open(name)
        pixel = load.load()
        render = ImageTk.PhotoImage(load)
        img.config(image = render, width = 512, height = 512)
        img.image = render
        _img.config(image = render, width = 512, height = 512)
        _img.image = render

def ClickSave():
    global _load
    if not _load:
        msg = "從來沒出現過，要怎麼留住呢？"
        tkinter.messagebox.showerror(title = '你留不住我的', message = msg)
    else:
        f = fd.asksaveasfile(mode = 'wb', filetypes = (("JPG file", "*.jpg"), ("TIF file", "*.tif"), ("All Files", "*.*")))
        load.save(f)

def ClickReset():
    global img, _img, load, _load, pixel
    if not _load:
        msg = "我們的關係無法重來。"
        tkinter.messagebox.showerror(title = '你根本連開始都沒有', message = msg)
    else:
        _load = load.copy()
        render = ImageTk.PhotoImage(load)
        _img.config(image = render, width = 512, height = 512)
        _img.image = render

def ClickHistogram():
    if not _load:
        msg = "解析無法，宛如你對我的愛意，零。"
        tkinter.messagebox.showerror(title = '要記得放圖片', message = msg)
    else:
        img_data = [0] * 256
        for x in range(_load.size[0]):
            for y in range(_load.size[1]):
                img_data[_load.getpixel((x, y))] += 1
        plt.bar(np.array([i for i in range(256)]), np.array(img_data))
        plt.show()

def ClickHistogramEqu():
    global _load, render, _img
    if not _load:
        msg = "我心中現在感到極度不平衡"
        tkinter.messagebox.showerror(title = '在我跟空白之間你選擇了空白', message = msg)
    else:
        img_data = [0] * 256
        img_data_num = [0] * 256
        for x in range(_load.size[0]):
            for y in range(_load.size[1]):
                img_data[_load.getpixel((x, y))] += 1
        img_sum = sum(img_data)
        for i in range(len(img_data)):
            if i == 0:
                img_data[i] = img_data[i]/img_sum
            else:
                img_data[i] = img_data[i]/img_sum + img_data[i-1]
        for i in range(len(img_data)):
            img_data[i] = round(img_data[i]*255)
        new_img = Image.new("L", (_load.size[0], _load.size[1]))
        for x in range(_load.size[0]):
            for y in range(_load.size[1]):
                val = img_data[_load.getpixel((x, y))]
                if(val >= 255):
                    new_img.putpixel((x, y),255)
                else:
                    new_img.putpixel((x, y),val)
                img_data_num[new_img.getpixel((x, y))] += 1
        render = ImageTk.PhotoImage(new_img)
        _img.config(image = render, width = 512, height = 512)
        _img.image = render
        plt.bar(np.array([i for i in range(256)]), np.array(img_data_num))
        plt.show()

def ClickBitPlane():
    global select_window
    select_window = tkinter.Tk()

    def ClickOK(tar_input):
        global _img , window, load, pixel
        try:
            new_img = _load.load()
            for x in range(_load.size[0]):
                for y in range(_load.size[1]):
                    if bin(pixel[x,y] + 256)[-(int(tar_input)+1)] == '1':
                        new_img[x,y] = 255
                    else:
                        new_img[x,y] = 0
            render = ImageTk.PhotoImage(_load)
            _img.config(image = render)
            _img.image = render
        except Exception as t:
            print(t)
            msg = "不要再這樣鬧了"
            tkinter.messagebox.showerror(title = '我受夠了', message = msg)
        select_window.destroy()

    if not _load:
        select_window.destroy()
        msg = "我婉拒了你，因為你根本不在乎我。"
        tkinter.messagebox.showerror(title = '我的圖片呢', message = msg)
    else:
        select_window.title("Choose your bit plane")
        lbl = tkinter.Label(select_window, text = "Choose your bit plane",font=("Arial",9))
        lst = ttk.Combobox(select_window, values = [str(i) for i in range(0,8)])
        btn_a = tkinter.Button(select_window, width = 7, height = 1, font=("Arial",9), text= "OK", command= lambda: ClickOK(lst.get()))
        btn_b = tkinter.Button(select_window, width = 7, height = 1, font=("Arial",9), text= "Cancel", command=lambda: select_window.destroy())
        lbl.grid(column=1, row=0)
        lst.grid(column=1, row=1, pady=10)
        btn_a.grid(column=0, row=2,padx=10,pady=10)
        btn_b.grid(column=2, row=2,padx=10,pady=10)
        select_window.mainloop()

def ClickSharpen(num):
    global _load
    if not _load:
        msg = "多麼尖銳的處理，都無法再對毫無感情的我造成傷害"
        tkinter.messagebox.showerror(title = '沒有圖片，沒有愛情', message = msg)
    else:
        try:
            num = float(num)
            enhancer = ImageEnhance.Sharpness(_load)
            _load = enhancer.enhance(num)
            _render = ImageTk.PhotoImage(_load)
            _img.config(image = _render, width = 512, height = 512)
            _img.image = _render
        except:
            msg = "我以為你會正常地對待我，結果是我被騙了"
            tkinter.messagebox.showerror(title = '請輸入浮點數', message = msg)

def ClickSmooth(num):
    global _load
    if not _load:
        msg = "不用柔和地安慰我了，習慣了^^"
        tkinter.messagebox.showerror(title = '沒放圖就別想用花言巧語釣我', message = msg)
    else:
        try:
            num = float(num)
            _load = _load.filter(ImageFilter.GaussianBlur(radius = num))
            _render = ImageTk.PhotoImage(_load)
            _img.config(image = _render, width = 512, height = 512)
            _img.image = _render
        except:
            msg = "不要轉移我的話題，說愛我..."
            tkinter.messagebox.showerror(title = '請輸入浮點數', message = msg)
def ClickMask():
    global select_window

    if not _load:
        msg = "什麼樣的面具都遮不住沒面子的人"
        tkinter.messagebox.showerror(title = '圖片還是沒有', message = msg)
        return
        
    select_window = tkinter.Tk()

    def DoMask(mode = "Normal Mask"):
        global _load,render,_img
        try:
            nparr = []
            dt = np.dtype(np.float64)

            for x in range(_load.size[0]):
                arr = []
                for y in range(_load.size[1]):
                    arr.append(_load.getpixel((x, y)))
                nparr.append(arr.copy())
            nparr = np.array(nparr, dt)
            nparr = np.c_[nparr,np.zeros((_load.size[1],1))]
            nparr = np.c_[np.zeros((_load.size[1],1)),nparr]
            nparr = np.r_[np.zeros((1,_load.size[0]+2)),nparr]
            nparr = np.r_[nparr,np.zeros((1,_load.size[0]+2))]
            _nparr = nparr.copy()
            
            if(mode == "Laplacian 1st"):
                for x in range(1,_load.size[0]+1):
                    for y in range(1,_load.size[1]+1):
                        _nparr[x][y] = round(nparr[x][y]*4 - nparr[x-1][y] - nparr[x+1][y] - nparr[x][y+1] - nparr[x][y-1])
                _nparr = _nparr+nparr
            elif(mode == "Laplacian 2st"):
                for x in range(1,_load.size[0]+1):
                    for y in range(1,_load.size[1]+1):
                        _nparr[x][y] = round(nparr[x][y]*8 - nparr[x-1][y] - nparr[x+1][y] - nparr[x+1][y+1] - nparr[x-1][y-1] - nparr[x][y+1] - nparr[x][y-1] - nparr[x-1][y+1] - nparr[x+1][y-1])
                _nparr = _nparr+nparr
            elif(mode == "Laplacian 3st"):
                for x in range(1,_load.size[0]+1):
                    for y in range(1,_load.size[1]+1):
                        _nparr[x][y] = round(nparr[x][y]*4 - nparr[x-1][y]*2 - nparr[x+1][y]*2 + nparr[x+1][y+1] + nparr[x-1][y-1] - nparr[x][y+1]*2 - nparr[x][y-1]*2 + nparr[x-1][y+1] + nparr[x+1][y-1])
                _nparr = _nparr+nparr
            elif(mode == "3x3 Median Filter"):
                for x in range(1,_load.size[0]+1):
                    for y in range(1,_load.size[1]+1):
                        _nparr[x][y] = round(median([nparr[x][y],nparr[x-1][y],nparr[x+1][y],nparr[x+1][y+1],nparr[x-1][y-1],nparr[x][y+1],nparr[x][y-1],nparr[x-1][y+1],nparr[x+1][y-1]]))
            else:
                for x in range(1,_load.size[0]+1):
                    for y in range(1,_load.size[1]+1):
                        _nparr[x][y] = round((nparr[x][y] + nparr[x-1][y] + nparr[x+1][y] + nparr[x+1][y+1] + nparr[x-1][y-1] + nparr[x][y+1] + nparr[x][y-1] + nparr[x-1][y+1] + nparr[x+1][y-1])/9)
            
            new_img = _load.load()

            for x in range(1,_load.size[0]+1):
                for y in range(1,_load.size[1]+1):
                    new_img[x-1,y-1] = int(_nparr[x][y])
            render = ImageTk.PhotoImage(_load)
            _img.config(image = render)
            _img.image = render
        except:
            pass
        select_window.destroy()

    select_window.title("Choose your mask mode")
    lbl = tkinter.Label(select_window, text = "Choose your mask mode",font=("Arial",9))
    lst = ttk.Combobox(select_window, values = ["3x3 Averaging Mask","3x3 Median Filter","Laplacian 1st","Laplacian 2st","Laplacian 3st"])
    btn_a = tkinter.Button(select_window, width = 7, height = 1, font=("Arial",9), text= "OK", command= lambda: DoMask(mode = lst.get()))
    btn_b = tkinter.Button(select_window, width = 7, height = 1, font=("Arial",9), text= "Cancel", command=lambda: select_window.destroy())
    lbl2 = tkinter.Label(select_window, text = "附註：3x3 Median Filter需先手動按一邊",font=("Arial",9))
    lbl.grid(column=1, row=0)
    lst.grid(column=1, row=1, pady=10)
    btn_a.grid(column=0, row=2,padx=10,pady=10)
    btn_b.grid(column=2, row=2,padx=10,pady=10)
    lbl2.grid(column=1, row=3)
    select_window.mainloop()


if __name__ == '__main__':
    print("main.py is ready")

    # create a new window
    window = tkinter.Tk()
    window.title("Homework 2")

    # create two picture
    img = tkinter.Label(window,relief = 'solid', width = 63, height = 24)
    _img = tkinter.Label(window,relief = 'solid', width = 63, height = 24)

    # size control
    window.geometry('1600x900')

    # title
    lbl_title = tkinter.Label(window, text = "Homework 1", font=("Arial",18))

    # open file
    btn_open = tkinter.Button(window, text = 'Open', bg = 'light cyan', font = ('Arial', 18), width = 7, height = 1, command = ClickOpen)

    # save file
    btn_save = tkinter.Button(window, text = 'Save', bg = 'light cyan', font = ('Arial', 18), width = 7, height = 1, command = ClickSave)

    # reset photo
    btn_reset = tkinter.Button(window, text = 'Reset', bg = 'light cyan', font = ('Arial', 18), width = 7, height = 1, command = ClickReset)

    # histogram of images
    btn_hist = tkinter.Button(window, text = 'Histogram', bg = 'yellow', font = ('Arial', 18), width = 8, height = 1, command = ClickHistogram)

    # histogram of images
    btn_eq_hist = tkinter.Button(window, text = 'HistoEqu', bg = 'yellow', font = ('Arial', 18), width = 8, height = 1, command = ClickHistogramEqu)

    # bit plane image
    btn_plane = tkinter.Button(window, text = 'Bit Plane', bg = 'yellow', font = ('Arial', 18), width = 8, height = 1, command = ClickBitPlane)

    # click sharpen
    btn_sharpen = tkinter.Button(window, text = 'Sharpen', bg = 'yellow', font = ('Arial', 18), width = 8, height = 1, command = lambda : ClickSharpen(ent_sharpen.get()))
    ent_sharpen = tkinter.Entry(window,width=10, background="yellow")

    # click smoothing
    btn_smoothing = tkinter.Button(window, text = 'Smoothing', bg = 'yellow', font = ('Arial', 18), width = 8, height = 1, command = lambda : ClickSmooth(ent_smoothing.get()))
    ent_smoothing = tkinter.Entry(window,width=10, background="yellow")

    # click cover
    btn_cover1 = tkinter.Button(window, text = 'Mask', bg = 'yellow', font = ('Arial', 18), width = 8, height = 1, command = lambda : ClickMask())

    #place
    img.place(x = 175, y = 20)
    _img.place(x = 700, y = 20)
    lbl_title.place(x=10, y=0)
    btn_open.place(x = 20, y = 50)
    btn_save.place(x = 20, y = 125)
    btn_reset.place(x = 20, y = 200)
    btn_hist.place(x=15, y= 275)
    btn_eq_hist.place(x=15, y= 350)
    btn_plane.place(x=15, y= 425)
    btn_sharpen.place(x=15, y= 500)
    ent_sharpen.place(x=15, y= 550)
    btn_smoothing.place(x=15, y= 575)
    ent_smoothing.place(x=15, y= 625)
    btn_cover1.place(x=15, y=650)

    # draw the window, and start the application
    window.mainloop()