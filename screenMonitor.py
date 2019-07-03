import cv2
import time
from PIL import ImageGrab as ig
import numpy as np
from vidTrack5 import Tracker
import serial

dur         = 1
threshold 	= 90
maxVal		= 100
minArea 	= 400
maxArea     = 4000

# Initial calibration period
def cal(Tracker):
    input("Open camera software but do not add fly to video")
    print("Calibration starting")

    var    = True
    neutAr = []
    while var:
        for i in range(3):
            img    = ig.grab()
            neutAr.append(Tracker.getContours(img))
        if neutAr[0] == neutAr[1] and neutAr[1] == neutAr[2]:
            nC  = neutAr[1]
            var = False

    print("Calibration compleate")
    input("Hit enter/space, then start recording. Hit same button to end.")
    return nC

def check(Tracker, nC, output):

    img   = ig.grab()
    frame = np.array(img)  
    c = Tracker.getContours(frame)  #need to modify output and take into account premptively detected contours
    if c > nC:
        if c-1 == nC:
            print("One object added")
            Tracker.subject = 1
        elif nC - 1 == c:
            print("One object lost")
        elif c+1 < nC:
            print("Multiple objects added")
            Tracker.subject = 1
        else:
            print("Multiple objects lost")
    
    return Tracker.subject









    





