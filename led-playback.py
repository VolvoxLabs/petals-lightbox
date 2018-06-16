#!/usr/bin/env python3

# Run 'sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python led_playback.py'

from __future__ import division
import threading
import multiprocessing as mp
import time
import random
import sys
import numpy as np
import itertools as it
from neopixel import *

running = True

perRow = 42 
perSect = 4*3
perDisplay = 3

print("Starting LED display")
print("Press CTRL + C to quit")


colors = []
colors2 = []


iterator = 0

LED_1_COUNT      = 1008      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL)

LED_2_COUNT      = 504     
LED_2_PIN        = 13      
LED_2_FREQ_HZ    = 800000  
LED_2_DMA        = 14      
LED_2_BRIGHTNESS = 128     
LED_2_INVERT     = False   
LED_2_CHANNEL    = 1     
strip2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL)



# convert video pixel in grb format to np.int32 (for ws2812 strip)
def convertHextoStripColor(color):
    color = color.lstrip('#')
    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    return Color(g,r,b)


# slice text file into #number_of_frames items, and each item contains 42*12 values 
def sliceTextFile():
    global colors
    global colors2
    with open('frame.txt') as f:
        with open('frame2.txt') as g:
            while True:
                nextLines = list(it.islice(f, 42*12)) + list(it.islice(g, 42*12))
                colors.append(nextLines)
                if not nextLines:
                    break
    
    with open('frame3.txt') as h:
        while True:
            nextLines2 = list(it.islice(h, 42*12))
            colors2.append(nextLines2)
            if not nextLines2:
                break
            
            
def updateCanvas():
    global iterator
    global strip1
    global strip2
    global colors
    global colors2
    while True:
	color1 = colors[iterator]
	color2 = colors2[iterator]
	if len(color1) == LED_1_COUNT and len(color2) == LED_2_COUNT:
	    for j in range(0, perSect):
		for i in range(0, perRow):
                    if j % 2 == 0:
                        strip1.setPixelColor(j*perRow+i,convertHextoStripColor(color1[j*perRow+i]))
                        strip1.setPixelColor(j*perRow+i+42*12, convertHextoStripColor(color1[j*perRow+i+42*12]))
                        strip2.setPixelColor(j*perRow+i, convertHextoStripColor(color2[j*perRow+i]))
		    else:
                        strip1.setPixelColor(j*perRow+(perRow-1-i), convertHextoStripColor(color1[j*perRow+i]))
                        strip1.setPixelColor(j*perRow+(perRow-1-i)+42*12, convertHextoStripColor(color1[j*perRow+i+42*12]))
                        strip2.setPixelColor(j*perRow+(perRow-1-i), convertHextoStripColor(color2[j*perRow+i]))
                        
            strip1.show()            
            time.sleep(50.0/1000.0)
            strip2.show()
            time.sleep(50.0/1000.0)
            iterator=iterator+1
	else:
            running = False
            sys.exit()
            break

if __name__ == '__main__':
    strip1.begin()
    strip2.begin()
    print ('Press Ctrl-C to quit.')
    
    try:
        sliceTextFile()
        print ('Text file slicing done. Start updating LED display')
        while running:
            updateCanvas()

    except KeyboardInterrupt:
        print ('quiting')