from PIL import Image, ImageTk
import tkinter
import tkinter.messagebox
from tkinter.constants import *
import numpy as np

window = None
ALL_NUM = 4
NUM_PER_ROW = 5

def FFT_2D(num1 = 1, num2 = 2, num3 = 3):
    global LoadList, ImgList
    f1 = np.fft.fft2(np.array(LoadList[num1]))
    fshift1 = np.fft.fftshift(f1)

    f2 = np.fft.fft2(np.array(LoadList[num2]))
    fshift2 = np.fft.fftshift(f2)

    fshift3 = np.fft.ifftshift(fshift1)

    magnitude_spectrum = 20 * np.log(np.abs(fshift1))
    phase_spectrum = np.angle(fshift2)
    inverse = np.abs(np.fft.ifft2(fshift3))
    

    dst1 = Image.fromarray(magnitude_spectrum)
    image1 = ImageTk.PhotoImage(dst1)
    ImgList[num1].config(image = image1)
    ImgList[num1].image = image1

    dst2 = Image.fromarray(phase_spectrum)
    image2 = ImageTk.PhotoImage(dst2)
    ImgList[num2].config(image = image2)
    ImgList[num2].image = image2

    dst3 = Image.fromarray(inverse)
    image3 = ImageTk.PhotoImage(dst3)
    ImgList[num3].config(image = image3)
    ImgList[num3].image = image3


def Question2():
    global window, ImgList, render
    window = tkinter.Tk()
    window.title("Hw 3-2")

    LoadPicture("lenna.tif")

    TitleList = [
        "Origin",
        "Magnitude",
        "Phase",
        "Inverse 2D FFT"
    ]

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
        
    FFT_2D()

    # size control
    window.geometry('1150x330')
    window.mainloop()

def LoadPicture(pictureName):
    global window, ImgList, LoadList, render, load
    LoadList = []
    ImgList = []
    load = Image.open(pictureName).resize((256,256))
    render = ImageTk.PhotoImage(load)
    for i in range(ALL_NUM):
        ImgList.append(tkinter.Label(window))
        LoadList.append(Image.open(pictureName))
        LoadList[i] = LoadList[i].resize((256,256))
        ImgList[i].config(image = render, width = 256, height = 256)
        ImgList[i].image = render

if __name__ == '__main__':
    Question2()