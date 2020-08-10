# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 00:33:26 2020

@author: nguye
"""
import numpy
import cv2
import os
import curses
import time
from PCA9685 import PCA9685
from bonjour import bonjour
from missing import missing
from cachecache import cachecache
# Load the cascade
# ========================================================================
# faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
# faceCascade.load('data/haarcascade_frontalface_default.xml')

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
#cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_eye_tree_eyeglasses.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
# Read the input image
print(cascPath)
# Start video capture
video_capture = cv2.VideoCapture(0)

# font 
font = cv2.FONT_HERSHEY_SIMPLEX  
# org 
org = (50, 50)   
# fontScale 
fontScale = 1   
# Blue color in BGR 
color = (255, 0, 0)   
# Line thickness of 2 px 
thickness = 2

# ========================================================================
sync_freq = 0 
# ========================================================================
# get the curses screen window
# screen = curses.initscr()
# # turn off input echoing
# curses.noecho()
# # respond to keys immediately (don't wait for enter)
# curses.cbreak()
# # map arrow keys to special values
# screen.keypad(True)

#setting start up serrvo positions
# ========================================================================
pwm = PCA9685()
pwm.setPWMFreq(50)

max_PAN      = 180
max_TILT     = 145
min_PAN      = 0
min_TILT     = 0

max_rate_TILT = 3
max_rate_PAN  = 3
    
step_PAN     = 1
step_TILT    = 1
current_PAN  = 90
current_TILT = 60
pwm.setRotationAngle(1, current_PAN) #PAN    
pwm.setRotationAngle(0, current_TILT) #TILT

# pseudo-PID control
k_PAN = 0.015
k_TILT = -0.015

kd_PAN = 0.095
kd_TILT = -0.095

error_acceptance = 15
# ========================================================================
previous_x = 0
previous_y = 0

previous_h = 0
previous_w = 0                  

delta_x = 0
delta_y = 0

previous_delta_x = 0
previous_delta_y = 0

delta_x_dot = 0
delta_y_dot = 0

rectangle_found = 0

# make some fun
bonjour = bonjour()
missing = missing()
cachecache = cachecache()

bonjour_ind = 0
missing_ind = 0
cachecache_ind = 0

#
# main loop
# ========================================================================
# https://techvidvan.com/tutorials/face-recognition-project-python-opencv/

try:
    while True:

        # Try to reduce lagging issues
        if sync_freq == 0:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=4, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            
        if sync_freq < 0:
            sync_freq += 1
            # stopping blinking rectangle
#             if rectangle_found > 0:
#                 cv2.rectangle(frame, (previous_x, previous_y), (x+previous_w, y+previous_h), (0, 255, 0), 2)            
        #
        else:            
            sync_freq = 0
            rectangle_found = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                rectangle_found += 1
                if rectangle_found == 1:                    
                    print(' x y previous ', previous_x, previous_y)                    
# ========================================================================================
                    # stay away from me !
#                     delta_x = previous_x - x
#                     delta_y = previous_y - y

                    # get in touch !                   
                    
                    delta_x = 300 - x
                    delta_y = 200 - y
                    
                    
                    delta_x_dot = delta_x - previous_delta_x
                    delta_y_dot = delta_y - previous_delta_y
                    
# ========================================================================================
                    # ignoring small error
                    if abs(delta_x) < error_acceptance:
                        delta_x     = 0
                        delta_x_dot = 0
                        
                    if abs(delta_y) < error_acceptance:
                        delta_y     = 0
                        delta_y_dot = 0
# ========================================================================================
                    print(' x y new ', x, y)
                    
                    previous_x = x
                    previous_y = y
                    
                    previous_h = h
                    previous_w = w
                    
                    previous_delta_x = delta_x
                    previous_delta_y = delta_y
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, str(x) + " " + str(y), (x, y), font, fontScale, (75, 75, 0), thickness, cv2.LINE_AA)
       
        # wait for keypress
        # ===========================================================
        char = cv2.waitKey(20)
        #print('key pressed', char)
        
        if char == ord('q'):
            break
        if char == ord('p'):
            #if p is pressed take a photo!
    #         camera.capture('image%s.jpg' % pic)
    #         pic = pic +1
    #         screen.addstr(0, 0, 'picture taken! ')
            cv2.putText(frame, 'another day in paradise !', (50,50) , font, fontScale, color, thickness, cv2.LINE_AA)
        elif char == 83:
            current_PAN = max(min_PAN, current_PAN - step_PAN)
            pwm.setRotationAngle(1, current_PAN) #PAN 
            #time.sleep(0.001)
            cv2.putText(frame, 'right ', (20, 20), font, fontScale, (0, 255, 0), thickness, cv2.LINE_AA) 
            
        elif char == 81:
            current_PAN = min(max_PAN, current_PAN + step_PAN)
            pwm.setRotationAngle(1, current_PAN) #PAN 
            #time.sleep(0.001)
            cv2.putText(frame, 'left ', (20, 20), font, fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
            
        elif char == 82:
            current_TILT = max(min_TILT, current_TILT - step_TILT)
            pwm.setRotationAngle(0, current_TILT) #TILT 
            #time.sleep(0.001)
            cv2.putText(frame, 'up ', (20, 20), font, fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
            
        elif char == 84:
            current_TILT = min(max_TILT, current_TILT + step_TILT)
            pwm.setRotationAngle(0, current_TILT) #TILT 
            #time.sleep(0.001)            
            cv2.putText(frame, 'down ', (20, 20), font, fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
            
        elif rectangle_found > 0 and (abs(delta_x) < 500 and abs(delta_y) < 500) and char == -1:
            # stay away
#             k_PAN = -0.01
#             k_TILT = +0.01
            # get in touch            
            print('pan tilt -- current ', current_PAN, current_TILT)

            # pseu-do PID
            delta_TILT = k_TILT * delta_y + kd_TILT * delta_y_dot
            # rate-limiter
            delta_TILT = min(abs(delta_TILT), max_rate_TILT)*numpy.sign(delta_TILT)
            # noise exclude
            if abs(delta_TILT) < step_TILT:
                delta_TILT = 0
            # here we go
            current_TILT = current_TILT + delta_TILT

            
            if current_TILT > max_TILT:
                current_TILT = max_TILT                
            if current_TILT < min_TILT:                
                current_TILT = min_TILT
                
            print('delta tilt ', delta_TILT)
            # pseu-do PID
            delta_PAN = k_PAN * delta_x + kd_PAN * delta_x_dot
            # rate-limiter
            delta_PAN = min(abs(delta_PAN), max_rate_PAN)*numpy.sign(delta_PAN)
            # noise exclude
            if abs(delta_PAN) < step_PAN:
                delta_PAN = 0            
            # here we go
            
            current_PAN = current_PAN + delta_PAN
                
            if current_PAN > max_PAN:
                current_PAN = max_PAN                
            if current_PAN < min_PAN:                
                current_PAN = min_PAN           
            
            print('delta PAN ', delta_PAN)
            
            print('delta_x delta_y ', delta_x, delta_y)
            
            print('pan tilt -- new ', current_PAN, current_TILT)            
            
            pwm.setRotationAngle(1, current_PAN)
            pwm.setRotationAngle(0, current_TILT)

        elif char == -1:
            cv2.putText(frame, 'on air !', (20, 20), font, fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
            #print('on air !')
            
        # Display the resulting frame
        cv2.imshow('face_tracking', frame)            
#             
finally:
    # shut down cleanly
    pwm.exit_PCA9685()
    
    video_capture.release()
    cv2.destroyAllWindows()