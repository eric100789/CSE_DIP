import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import cv2
from math import cos

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

def homomorphic_filter():
	img = cv2.imread('Fig0460a.tif')
	plt.subplot(1,2,1),plt.imshow(img),plt.title('Origin')
	img = np.double(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
	m,n = img.shape 
	rL = 0.4
	rH = 3.0
	c = 5
	d0 = 20 
	I1 = np.log(img+1) 
	FI = np.fft.fft2(I1) 
	n1 = np.floor(m/2) 
	n2 = np.floor(n/2) 
	D = np.zeros((m,n)) 
	H = np.zeros((m,n)) 
	for i in range(m): 
		for j in range(n): 
			D[i,j]=((i-n1)**2+(j-n2)**2) 
			H[i,j]=(rH-rL)*(np.exp(c*(-D[i,j]/(d0**2))))+rL
	I2 = np.fft.ifft2(H*FI) 
	I3 = np.real(np.exp(I2)) 
	plt.subplot(1,2,2),plt.imshow(I3, cmap ='gray'),plt.title('After') 
	plt.show()

def red_component_image():
	global btn4, img, img2, load, load2
	if(load2):
		width, height = load.size
		for y in range(height):
			for x in range(width):
				rgba = load.getpixel((x,y))
				rgba = (rgba[0], 0, 0);
				load2.putpixel((x,y), rgba)
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def green_component_image():
	global btn5, img, img2, load, load2
	if(load2):
		width, height = load.size
		for y in range(height):
			for x in range(width):
				rgba = load.getpixel((x,y))
				rgba = (0, rgba[1], 0);
				load2.putpixel((x,y), rgba)
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def blue_component_image():
	global btn6, img, img2, load, load2
	if(load2):
		width, height = load.size
		for y in range(height):
			for x in range(width):
				rgba = load.getpixel((x,y))
				rgba = (0, 0, rgba[2]);
				load2.putpixel((x,y), rgba)
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def rgb_to_hsi():
	global btn7, img, img2, load, load2,pixel, pixel2
	plt.subplot(2,2,1),plt.imshow(load),plt.title('Origin')
	a, b = load.size
	pixel2 = load2.load()
	for x in range(load2.size[0]):
		for y in range(load2.size[1]):
			r,g,b = pixel[x,y]
			sita = 1/cos((0.5*(r-g)+(r-b))/((r-g)**2+(r-b)*(g-b))**(1/2))
			if b>g:
				pixel2[x,y]=(int(360-sita),int(360-sita),int(360-sita))
			else:
				pixel2[x,y]=(int(sita),int(sita),int(sita))
	plt.subplot(2,2,2),plt.imshow(load2, cmap ='gray'),plt.title('Hue')
	
	for x in range(load2.size[0]):
		for y in range(load2.size[1]):
			r,g,b = pixel[x,y]
			sita = 1/cos((0.5*(r-g)+(r-b))/((r-g)**2+(r-b)*(g-b))**(1/2))
			pixel2[x,y]=(int(255*(1-((3/(r+g+b))*(min(r,g,b))))),int(255*(1-((3/(r+g+b))*(min(r,g,b))))),int(255*(1-((3/(r+g+b))*(min(r,g,b))))))
	plt.subplot(2,2,3),plt.imshow(load2, cmap ='gray'),plt.title('Saturation')

	for x in range(load2.size[0]):
		for y in range(load2.size[1]):
			r,g,b = pixel[x,y]
			sita = 1/cos((0.5*(r-g)+(r-b))/((r-g)**2+(r-b)*(g-b))**(1/2))
			pixel2[x,y]=(int((r+g+b)/3),int((r+g+b)/3),int((r+g+b)/3))
	plt.subplot(2,2,4),plt.imshow(load2, cmap ='gray'),plt.title('Intensity')
	plt.show()

def color_complements():
	global btn8, img, img2, load, load2
	if(load2):
		width, height = load.size
		for y in range(height):
			for x in range(width):
				rgba = load.getpixel((x,y))
				rgba = (255-rgba[0], 255-rgba[1], 255-rgba[2]);
				load2.putpixel((x,y), rgba)
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def sharping():
	global img, img2, btn12, load, load2
	if load2:
		load2 = load2.filter(ImageFilter.SHARPEN)
		render = ImageTk.PhotoImage(load2)
		img2.config(image = render)
		img2.image = render

def segment():
	global plt, load
	plt = cv2.cvtColor(np.asarray(load),cv2.COLOR_RGB2BGR)
	HSV = cv2.cvtColor(plt, cv2.COLOR_BGR2HSV)

	BottomPurple = np.array([125, 43, 46])
	UpperPurple = np.array([155, 255, 255])
	mask = cv2.inRange(HSV, BottomPurple, UpperPurple)
	Purple_Things = cv2.bitwise_and(plt, plt, mask = mask)
	Purple_Things = cv2.cvtColor(Purple_Things, cv2.COLOR_HSV2BGR)
	plt = Image.fromarray(cv2.cvtColor(Purple_Things,cv2.COLOR_BGR2RGB))
	plt.show()

#圖片
img = tk.Label(window,relief = 'solid', width = 63, height = 24)
img2 = tk.Label(window,relief = 'solid', width = 63, height = 24)
#開檔存檔
btn = tk.Button(window, text = 'open', bg = 'light cyan', font = ('Arial', 18), width = 7, height = 1, command = OpenFile)
btn2 = tk.Button(window, text = 'save', bg = 'light yellow', font = ('Arial', 18), width = 7, height = 1, command = save_file)
#homomorphic_filter
btn3 = tk.Button(window, text = 'homomorphic_filter', bg = 'gray79', font = ('Arial', 18), width = 18, height = 1, command = homomorphic_filter)
btn4 = tk.Button(window, text = 'Red component image', bg = 'red', font = ('Arial', 18), width = 18, height = 1, command = red_component_image)
btn5 = tk.Button(window, text = 'Green component image', bg = 'green', font = ('Arial', 18), width = 18, height = 1, command = green_component_image)
btn6 = tk.Button(window, text = 'Blue component image', bg = 'blue', font = ('Arial', 18), width = 18, height = 1, command = blue_component_image)
btn7 = tk.Button(window, text = 'RGB to HSI', bg = 'DarkSeaGreen1', font = ('Arial', 18), width = 18, height = 1, command = rgb_to_hsi)
btn8 = tk.Button(window, text = 'color complements', bg = 'SkyBlue1', font = ('Arial', 18), width = 18, height = 1, command = color_complements)
btn9 = tk.Button(window, text = 'sharping with the Laplacian', bg = 'DarkOrchid1', font = ('Arial', 18), width = 20, height = 1, command = sharping)
btn10 = tk.Button(window, text = 'segment', bg = 'Purple1', font = ('Arial', 18), width = 20, height = 1, command = segment)

img.place(x = 150, y = 20)
img2.place(x = 675, y = 20)
btn.place(x = 20, y = 20)
btn2.place(x = 20, y = 80)
btn3.place(x = 150, y = 560)
btn4.place(x = 150, y = 640)
btn5.place(x = 450, y = 640)
btn6.place(x = 750, y = 640)
btn7.place(x = 150, y = 720)
btn8.place(x = 450, y = 720)
btn9.place(x = 150, y = 800)
btn10.place(x = 500, y = 800)
window.mainloop()