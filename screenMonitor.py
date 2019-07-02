import cv2
import time
from PIL import ImageGrab as ig
import numpy as np
from vidTrack5 import Tracker

dur = 70
threshold 	= 90
maxVal		= 100
minArea 	= 400
maxArea     = 4000

Trackoi = Tracker(threshold, maxVal, minArea, maxArea)

# Initial calibration period
def cal():
    input("Open camera software but do not add fly to video")
    print("Calibration starting")

    var    = True
    neutAr = []
    while var:
        for i in range(3):
            img    = ig.grab()
            neutAr.append(Trackoi.getContours(img))
        if neutAr[0] == neutAr[1] and neutAr[1] == neutAr[2]:
            nC  = neutAr[1]
            var = False

    print("Calibration compleate")
    input("Hit enter/space, then start recording. Hit same button to end.")

def check(nC):

    img   = ig.grab()
    frame = np.array(img)  
    c = Trackoi.getContours(frame)  #need to modify output and take into account premptively detected contours
    if c > nC:
        if c-1 == nC:
            print("One object added")
            Trackoi.subject = True
        elif nC - 1 == c:
            print("One object lost")
        elif c+1 < nC:
            print("Multiple objects added")
            Trackoi.subject = True
        else:
            print("Multiple objects lost")
    return Trackoi.subject







    





