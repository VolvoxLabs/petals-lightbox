from __future__ import division
from tkinter import *
import threading
import time
import random
import sys
import numpy as np
import cv2

running = True

perRow = 42
perSect = 4*3
perDisplay = 3

print("Starting visualizer")
print("Press CTRL + C to quit")

##master = Tk()
##canvas = Canvas(master, bg="grey", height = 600, width = 540)
##canvas.grid(row=0, columnspan=2)
leds = []

textname = sys.argv[1]
moviename = sys.argv[2]
f = open(textname, 'w')

def addZero(w):
    if(len(w) == 1):
        w = "0" + w
    if(len(w) == 0):
        w = "00"
    return w

def convertRGBtoHex(color):
    b = addZero("%x" % color[0])
    g = addZero("%x" % color[1])
    r = addZero("%x" % color[2])

    hexa = "#" + r + g + b
    return hexa

for y in range(0, perSect):
    for x in range(0, perRow):
        radius = 10
        xspace = 2
        yspace = 40
##        leds.append(canvas.create_oval(x*radius+(x+1)*xspace,y*radius+(y+1)*yspace,(x+1)*radius+(x+1)*xspace, (y+1)*radius+(y+1)*yspace, fill="black"))

def playback():
    cap = cv2.VideoCapture(moviename)
	
    if(cap.isOpened() == False):
        print("Error opening video stream")

    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret):
            cv2.imshow(textname, frame)
            updateCanvas(frame)
        else:
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()
            running = False
##            master.quit()
            break
        cv2.waitKey(1)

def updateCanvas(frame):
    for j in range(0, perSect):
        for i in range(0, perRow):
            hexa = convertRGBtoHex(frame[j,i])
##            canvas.itemconfig(leds[j*perRow+i], fill=hexa)
            f.write(str(hexa) + '\n')
	
if __name__ == '__main__':
    try:
        playback()
    except KeyboardInterrupt:
        sys.exit()