import cv2
import time
from PIL import ImageGrab as ig
import numpy as np

dur = 70
threshold 	= 90
maxVal		= 100
minArea 	= 400
pname 		= 'posTest.vD'
numContours = 7


sT = time.time()

with time.time() as nT:
    while nT % dur == 0:
        img = ig.grab()
        frame = np.array(img)  
        frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        thresh = cv2.threshold(frame, threshold, maxVal, cv2.THRESH_BINARY)[1]
        thresh     = cv2.convertScaleAbs(thresh)
		thresh 	   = cv2.dilate(thresh, None, iterations=3)	
		img, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    





