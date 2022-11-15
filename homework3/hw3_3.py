from PIL import Image, ImageTk
import tkinter
import tkinter.messagebox
from tkinter.constants import *
import numpy as np
import cv2

window = None
ALL_NUM = 7
NUM_PER_ROW = 4

def MultiplyWeirdNumber(fromnum = 1 ,num = 1):
    global LoadList, ImgList
    nparr = []
    for x in range(LoadList[fromnum].size[0]):
        arr = []
        for y in range(LoadList[fromnum].size[1]):
            arr.append((LoadList[fromnum].getpixel((x, y))) * (-1)**(x+y))
        nparr.append(arr.copy())

    new_img = LoadList[num].load()

    for x in range(LoadList[num].size[0]):
        for y in range(LoadList[num].size[1]):
            new_img[x,y] = int(nparr[x][y])
    render = ImageTk.PhotoImage(LoadList[num])
    ImgList[num].config(image = render)
    ImgList[num].image = render
    LoadList[num].save("temp.tif")

def DFT_2D(gotnum = 1, num1 = 2, num2 = 3, num3 = 4, num4 = 5):
    global LoadList, ImgList
    f1 = np.fft.fft2(np.array(LoadList[gotnum]))
    fshift1 = np.fft.fftshift(f1)

    f2 = cv2.imread('temp.tif',)
    f2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(f2), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    f2result = 10 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

    fshift3 = np.fft.ifftshift(fshift1)

    magnitude_spectrum = 20 * np.log(np.abs(fshift1))
    inverse = np.abs(np.fft.ifft2(fshift3))
    

    dst1 = Image.fromarray(magnitude_spectrum)
    image1 = ImageTk.PhotoImage(dst1)
    ImgList[num1].config(image = image1)
    ImgList[num1].image = image1

    nparr = []
    for x in range(LoadList[num2].size[0]):
        arr = []
        for y in range(LoadList[num2].size[1]):
            arr.append(f2result[x][y])
        nparr.append(arr.copy())

    new_img = LoadList[num2].load()

    for x in range(LoadList[num2].size[0]):
        for y in range(LoadList[num2].size[1]):
            new_img[x,y] = int(nparr[x][y])
    render = ImageTk.PhotoImage(LoadList[num2])
    ImgList[num2].config(image = render)
    ImgList[num2].image = render

    dst3 = Image.fromarray(inverse)
    image3 = ImageTk.PhotoImage(dst3)
    ImgList[num3].config(image = image3)
    ImgList[num3].image = image3

    ishift = np.fft.ifftshift(dft_shift)
    iimg = cv2.idft(ishift)
    iresult = cv2.magnitude(iimg[:, :, 0], iimg[:, :, 1])

    nparr = []
    for x in range(LoadList[num4].size[0]):
        arr = []
        for y in range(LoadList[num4].size[1]):
            arr.append(iresult[x][y])
        nparr.append(arr.copy())

    new_img = LoadList[num4].load()

    for x in range(LoadList[num4].size[0]):
        for y in range(LoadList[num4].size[1]):
            new_img[x,y] = int(nparr[x][y])
    render = ImageTk.PhotoImage(LoadList[num4])
    ImgList[num4].config(image = render)
    ImgList[num4].image = render


def Question3():
    global window, ImgList, render
    
    window = tkinter.Tk()
    window.title("Hw 3-3")

    LoadPicture("DIP_image.tif")

    TitleList = [
        "Origin",
        "Multiplied",
        "FFT",
        "DFT",
        "Inverse FFT",
        "Inverse DFT",
        "Multiplied"
    ]
    explain = tkinter.Label(window, text="Explain:\n傅利葉轉換後的逆轉換\n圖片會一樣\n而共軛會讓圖片倒過來", font=("Arial",18))
    explain.grid(row=3,column=3)

    for i in range(ALL_NUM):
        try:
            title = tkinter.Label(window, text=TitleList[i], font=("Arial",18))
        except IndexError:
            title = tkinter.Label(window, text="IndexError", font=("Arial",18))
        temp = 2*(i//NUM_PER_ROW)

        if i==14:
            title = tkinter.Label(window, text=TitleList[i], font=("Arial",12))

        title.grid(row=temp,column=i%NUM_PER_ROW,padx=10,pady=2)
        ImgList[i].grid(row=temp+1,column=i%NUM_PER_ROW,padx=10,pady=2)
        
    MultiplyWeirdNumber()
    DFT_2D()
    MultiplyWeirdNumber(5,6)

    # size control
    window.geometry('1220x625')
    window.mainloop()

def LoadPicture(pictureName):
    global window, ImgList, LoadList, render, load
    LoadList = []
    ImgList = []
    load = Image.open(pictureName).resize((256,256))
    load.convert("L")
    render = ImageTk.PhotoImage(load)
    for i in range(ALL_NUM):
        ImgList.append(tkinter.Label(window))
        LoadList.append(Image.open(pictureName))
        LoadList[i].convert("L")
        LoadList[i] = LoadList[i].resize((256,256))
        ImgList[i].config(image = render, width = 256, height = 256)
        ImgList[i].image = render

if __name__ == '__main__':
    Question3()