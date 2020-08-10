#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
    
try:
    print ("This is an PCA9685 routine")
    pwm = PCA9685()
    pwm.setPWMFreq(50)
    pwm.setRotationAngle(1, 0) #PAN    
    pwm.setRotationAngle(0, 0) #TILT

    time.sleep(5)
    
    max_PAN  = 170
    max_TILT = 110
    while True:
        # setServoPulse(2,2500)
        
        # go leap
        for i in range(1,100,1): 
            pwm.setRotationAngle(1, (i/100)*max_PAN)
            pwm.setRotationAngle(0, (i/100)*max_TILT)   
            time.sleep(0.2)
            
        time.sleep(5)
        # return leap
        for i in range(100,1,-1): 
            pwm.setRotationAngle(1, (i/100)*max_PAN)
            pwm.setRotationAngle(0, (i/100)*max_TILT)   
            time.sleep(0.2)

except:
    pwm.setRotationAngle(1, 0) #PAN    
    pwm.setRotationAngle(0, 0) #TILT    
    pwm.exit_PCA9685()
    print("\nProgram end")
    exit()