# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 13:50:41 2016

@author: zidali
"""
import matplotlib.pyplot as plt 
import time
from scipy import misc 
from skimage.filters import threshold_otsu, threshold_adaptive
from scipy.ndimage.morphology import binary_closing, binary_fill_holes
from skimage.morphology import disk
from skimage.measure import label, regionprops
import numpy as np
import Tkinter as tk
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
#from Tkinter.filedialog import askopenfilename
import pandas as pd
import os

def fetch_file():
    global entry1
    entry1.delete(0)
    entry1.insert(0, tkFileDialog.askopenfilename( \
    initialdir = r"C:\Users\zidali\Google Drive\0 Research\Shared Folders\Zhiheng-Zida\Zhiheng\Analyzed Results", \
    filetypes = [('TIFF', '.tif'), ('all files', '.*')])) #Setting the option of initialdir might be helpful.


def get_file():
    global entry1
    root = tk.Tk()
    root.title("Folder path")
    root.geometry("400x70")
    
    frame = tk.Frame(root)
    frame.pack()
    
    label1 = tk.Label(frame, text = "Folder directory:")
    label1.grid(row = 0, column = 1)
    
    pathvar = tk.StringVar()
    entry1 = tk.Entry(frame, textvariable = pathvar)
    entry1.config(width = 30)
    entry1.grid(row = 0, column = 2)
    
    button1 = tk.Button(frame, text = 'Open', command = fetch_file)
    button1.grid(row = 0, column = 3)
    
    button2 = tk.Button(frame, text = 'OK', command = root.destroy)
    button2.config(width = 30)
    button2.grid(row = 1, columnspan = 3)
    
    root.mainloop()
    
    return pathvar.get()

def imgRead():
    path_this = get_file()    
    img = misc.imread(path_this)
    return img

def imgRead_gray():
    path_this = get_file()    
    img = misc.imread(path_this, flatten = True)
    return img
    
def imgHist(img, bns = 10, rnge = None):
    plt.figure()
    plt.hist(img.ravel(), bins = bns, range = rnge)
    





    

def centroid_vs_disksize(i):
    selem = disk(i)
    closed_img = binary_fill_holes(binary_closing(binary_img, selem))
#    plt.figure()
#    plt.imshow(closed_img)
    
    return get_pattern_centroid(closed_img)

def get_pattern_centroid(closed_img):
    labeled_img = label(closed_img)
    regions = regionprops(labeled_img)
    circle = max(regions, key=lambda item: item.area)
    y, x = circle.centroid
    centroid = np.array([int(x), int(y)])
    return centroid
   
   
if __name__ == '__main__':
    img = imgRead()
    imgHist(img, bns = 50)
    gray_img = imgRead_gray()
    imgHist(gray_img, bns = 50)
    
   
   
   
   
   
   
   
#a = plt.imread(r"E:\0 experiment\2016\20160705\16 Time Lapse\ExportedImage\D3-0002_c3.TIF")
#
#gray_img = a
##start_time = time.time()
##
#global_thresh = threshold_otsu(gray_img)
##
##end_time = time.time()
##print "Time took to build up the dist2xys mapping strategy:", end_time - start_time
##print global_thresh
#
#binary_img = (gray_img > global_thresh)
#plt.figure()
#plt.imshow(binary_img)
#selem = disk(6)
#closed_img = binary_fill_holes(binary_closing(binary_img, selem))
#plt.imshow(closed_img)
#
#thresholded_img = np.multiply(binary_img, gray_img)
#get_pattern_centroid(closed_img)
##
##for i in range(20):
##    cen = centroid_vs_disksize(i)
##    print 'disksize = ', i, ':', cen   
   
   
   
   

#b = plt.imread(r'E:\0 experiment\2016\20160705\16 Time Lapse\ExportedImage\D3-0002_c3.TIF')
#
#plt.hist(b.ravel(), bins = 60, range = (125, 600))
#
#threshold_otsu(b)













