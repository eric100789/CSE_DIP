import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy
import matplotlib.pyplot as plt

window = tk.Tk()
window.geometry("1200x900")
name = None
load = None
load2 = None
render = None
pixel = None
pixel2 = None

def OpenFile():#function for opening file
	global btn, img, img2, load, load2, pixel
	name = fd.askopenfilename()#為一個str儲存檔案的路徑
	load2 = Image.open(name)
	load = Image.open(name)
	pixel = load.load()#儲存圖片每個pixel的灰階值
	render = ImageTk.PhotoImage(load)
	img.config(image = render, width = 512, height = 512)
	img.image = render
	img2.config(image = render, width = 512, height = 512)
	img2.image = render
	
def save_file():#function for saving file
	global load2, btn2
	f = fd.asksaveasfile(mode = 'wb', filetypes = (("JPG file", "*.jpg"), ("TIF file", "*.tif"), ("All Files", "*.*")))
	if load2:
		load.save(f)

def gray_level_slicing():
	global img, img2, btn3, sb, sb2, cbtn, load, load2, pixel, pixel2
	if load2:
		a, b = load2.size
		pixel2 = load2.load()
		for x in range(a):
			for y in range(b):
				g = pixel[x,y]#使用原圖進行修正
				if var1.get() == 0:
					if g >= int(sb.get()) and g <= int(sb2.get()):
						pixel2[x,y] = 255
					else:
						pixel2[x,y] = pixel[x,y]#沒在範圍內，回復原值
				elif var1.get() == 1:
					if g >= int(sb.get()) and g <= int(sb2.get()):
						pixel2[x,y] = 255
					else:
						pixel2[x,y] = 0	#black
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def bit_plane(v):
	global img, img2, btn3, sb, sb2, cbtn, load, load2, pixel, pixel2
	if load2:
		a, b = load2.size
		pixel2 = load2.load()
		for x in range(a):
			for y in range(b):
				if bin(pixel[x,y] + 256)[-(int(v) + 1)] == '1':
					pixel2[x,y] = 255
				else:
					pixel2[x,y] = 0
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def Smoothing():#模糊化
	global img, img2, btn11, load, load2
	if load2:
		load2 = load2.filter(ImageFilter.GaussianBlur(radius = 2))
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def Sharpening():#銳利化
	global img, img2, btn12, load, load2
	if load2:
		load2 = load2.filter(ImageFilter.SHARPEN)
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		mg2.image = render

def FFT():
	global img, img2, btn21, load, load2
	if load2:
		f = numpy.fft.fft2(numpy.array(load2))
		fshift = numpy.fft.fftshift(f)
		magnitude_spectrum = 20 * numpy.log(numpy.abs(fshift))
		dst = Image.fromarray(magnitude_spectrum)
		image = ImageTk.PhotoImage(dst)
		img2.config(image = image)
		img2.image = image

def TwoDimension_FFT_Amplitude():
	global img, img2, btn22, load, load2
	if load2:
		f = numpy.fft.fft2(numpy.array(load2))
		fshift = 1 + numpy.fft.fftshift(f)
		spectrum = 20 * numpy.log(numpy.abs(fshift))
		sep = numpy.abs(f)
		imgsep = numpy.real(numpy.fft.ifft2(sep))
		fig = plt.figure()
		ax1 = fig.add_subplot(121)
		ax2 = fig.add_subplot(122)
		ax1.imshow(spectrum, cmap = 'gray')
		ax2.imshow(imgsep, cmap = 'gray')
		ax1.title.set_text('spectrum')
		ax2.title.set_text('Inverse 2DFFT')
		plt.show()

def TwoDimension_FFT_Phase():
	global img, img2, btn22, load, load2
	if load2:
		f = numpy.fft.fft2(numpy.array(load2))
		fshift = numpy.fft.fftshift(f)
		spectrum = numpy.angle(fshift)
		sep = numpy.exp(1j * numpy.angle(f))
		imgsep = numpy.real(numpy.fft.ifft2(sep))
		fig = plt.figure()
		ax1 = fig.add_subplot(121)
		ax2 = fig.add_subplot(122)
		ax1.imshow(spectrum, cmap = 'gray')
		ax2.imshow(imgsep, cmap = 'gray')
		ax1.title.set_text('spectrum')
		ax2.title.set_text('Inverse 2DFFT')
		plt.show()

var1 = tk.IntVar()
var2 = tk.IntVar()
#圖片
img = tk.Label(window,relief = 'solid', width = 63, height = 24)
img2 = tk.Label(window,relief = 'solid', width = 63, height = 24)
#開檔存檔
btn = tk.Button(window, text = 'open', bg = 'light cyan', font = ('Arial', 18), width = 7, height = 1, command = OpenFile)
btn2 = tk.Button(window, text = 'save', bg = 'light yellow', font = ('Arial', 18), width = 7, height = 1, command = save_file)
#按下按鈕後顯示Gray-level slicing後的圖片
btn3 = tk.Button(window, text = 'Gray-level slicing', bg = 'yellow2', font = ('Arial', 18), width = 14, height = 1, command = gray_level_slicing)
#調整範圍時,不修正圖片
sb = tk.Spinbox(window, from_ = 0, to = 255, increment = 1)
sb2 = tk.Spinbox(window, from_ = 0, to = 255, increment = 1)
cbtn = tk.Checkbutton(window, text = 'display unselected area as black color', variable = var1, onvalue = 1, offvalue = 0)
#按下按鈕後顯示Bit-Plane image
sca = tk.Scale(window, label ='Bit-Plane images', from_= 0, to = 7, orient ='horizontal', length = 900, showvalue = 1,variable = var2, tickinterval = 1, resolution = 1, command = bit_plane)
#Smoothing
btn11 = tk.Button(window, text = 'Smoothing', bg = 'DarkSeaGreen1', font = ('Arial', 18), width = 9, height = 1, command = Smoothing)
#Sharpening
btn12 = tk.Button(window, text = 'Sharpening', bg = 'SkyBlue1', font = ('Arial', 18), width = 9, height = 1, command = Sharpening)
#FFT
btn21 = tk.Button(window, text = 'FFT', bg = 'DarkOrchid1', font = ('Arial', 18), width = 9, height = 1, command = FFT)
#2d-FFT
btn31 = tk.Button(window, text = '2D-FFT (Amplitude)', bg = 'Purple1', font = ('Arial', 18), width = 16, height = 1, command = TwoDimension_FFT_Amplitude)
btn32 = tk.Button(window, text = '2D-FFT (Phase)', bg = 'Purple2', font = ('Arial', 18), width = 16, height = 1, command = TwoDimension_FFT_Phase)

img.place(x = 150, y = 20)
img2.place(x = 675, y = 20)
btn.place(x = 20, y = 20)
btn2.place(x = 20, y = 80)
btn3.place(x = 150, y = 560)
tk.Label(window, text = 'A').place(x = 370, y = 540)
tk.Label(window, text = 'B').place(x = 570, y = 540)
sb.place(x = 370, y = 570)
sb2.place(x = 570, y = 570)
cbtn.place(x = 750, y = 570)
sca.place(x = 150, y = 620)
btn11.place(x = 150, y = 760)
btn12.place(x = 350, y = 760)
btn21.place(x = 550, y = 760)
btn31.place(x = 750, y = 750)
btn32.place(x = 750, y = 790)
window.mainloop()