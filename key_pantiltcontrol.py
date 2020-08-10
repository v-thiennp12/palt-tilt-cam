#Raspberry-Pi pan and tilt using arrow keys script
#must be run from Pi's terminal!
#use code "python pantilt.py" after you cd into the correct folder!

#By Tucker Shannon @ tucksprojects.com 11-08-16

#importing required libraries
import curses
import os
import time
import picamera

#!/usr/bin/python
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

#setting up camera
camera = picamera.PiCamera()
camera.resolution = (512, 384)
camera.start_preview()

#flipping the camera for so its not upside down
# camera.vflip = True
# camera.hflip = True

# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

#setting start up serrvo positions

pwm = PCA9685()
pwm.setPWMFreq(50)

max_PAN      = 180
max_TILT     = 145
min_PAN      = 0
min_TILT     = 0
    
step_PAN     = 10
step_TILT    = 10
current_PAN  = 90
current_TILT = 90
pwm.setRotationAngle(1, current_PAN) #PAN    
pwm.setRotationAngle(0, current_TILT) #TILT

# print doesn't work with curses, use addstr instead
pic = 1
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            #if q is pressed quit
            break
        if char == ord('p'):
            #if p is pressed take a photo!
            camera.capture('image%s.jpg' % pic)
            pic = pic +1
            screen.addstr(0, 0, 'picture taken! ')
            
        elif char == curses.KEY_RIGHT:
            screen.addstr(0, 0, 'right ')
            current_PAN = max(min_PAN, current_PAN - step_PAN)
            pwm.setRotationAngle(1, current_PAN) #PAN 
            time.sleep(0.001)
            
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')
            current_PAN = min(max_PAN, current_PAN + step_PAN)
            pwm.setRotationAngle(1, current_PAN) #PAN 
            time.sleep(0.001)
            
        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'up ')
            current_TILT = max(min_TILT, current_TILT - step_TILT)
            pwm.setRotationAngle(0, current_TILT) #TILT 
            time.sleep(0.001)
            
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'up ')
            current_TILT = min(max_TILT, current_TILT + step_TILT)
            pwm.setRotationAngle(0, current_TILT) #TILT 
            time.sleep(0.001)
finally:
    # shut down cleanly
    pwm.exit_PCA9685()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()