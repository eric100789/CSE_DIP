from PIL import Image, ImageTk
import tkinter
import tkinter.messagebox
from tkinter.constants import *
import numpy as np
from statistics import median
import cv2
from matplotlib import pyplot as plt

window = None

def FFT_2D():
    global load, load1, load2, img, img1, img2
    f1 = np.fft.fft2(np.array(load1))
    fshift1 = np.fft.fftshift(f1)

    f2 = np.fft.fft2(np.array(load2))
    fshift2 = np.fft.fftshift(f2)

    magnitude_spectrum = 20 * np.log(np.abs(fshift1))
    phase_spectrum = np.angle(fshift2)

    dst1 = Image.fromarray(magnitude_spectrum)
    image1 = ImageTk.PhotoImage(dst1)
    img1.config(image = image1)
    img1.image = image1

    dst2 = Image.fromarray(phase_spectrum)
    image2 = ImageTk.PhotoImage(dst2)
    img2.config(image = image2)
    img2.image = image2

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
    load1 = Image.open("lenna.tif")
    load2 = Image.open("lenna.tif")
    load3 = Image.open("lenna.tif")
    load4 = Image.open("lenna.tif")
    load = Image.open("lenna.tif")
    pixel = load.load()
    render = ImageTk.PhotoImage(load)
    img.config(image = render, width = 512, height = 512)
    img.image = render
    img1.config(image = render, width = 512, height = 512)
    img1.image = render
    img2.config(image = render, width = 512, height = 512)
    img2.image = render
    img3.config(image = render, width = 512, height = 512)
    img3.image = render
    img4.config(image = render, width = 512, height = 512)
    img4.image = render


def Question1():
    global window, render
    window = tkinter.Tk()
    window.title("Hw 3-1")

    LoadPicture()
    FFT_2D()

    title = tkinter.Label(window, text = "Origin", font=("Arial",18))
    title1 = tkinter.Label(window, text = "2D FFT", font=("Arial",18))
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