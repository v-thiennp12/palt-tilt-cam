# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 00:33:26 2020

@author: nguye
"""
import numpy
import cv2
import os

# Load the cascade
# faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
# faceCascade.load('data/haarcascade_frontalface_default.xml')

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
# Read the input image

# https://techvidvan.com/tutorials/face-recognition-project-python-opencv/
video_capture = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=4, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
video_capture.release()
cv2.destroyAllWindows()