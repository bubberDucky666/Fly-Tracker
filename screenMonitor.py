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
    while var:
        neutAr = []
        for i in range(3):
            img = ig.grab()
            img = np.array(img)

            val = Tracker.getContours(img)
            neutAr.append(val)
            #cv2.imshow("ye", img )
        c0 = len(neutAr[0])
        c1 = len(neutAr[1])
        c2 = len(neutAr[2])

        print(c0, c1, c2)

        if c0 == c1 and c1 ==c2:
            nC  = neutAr[1]
            var = False

    print("Calibration compleate")
    input("Hit enter/space, then start recording. Hit same button to end.")
    return len(nC)

def check(Tracker, nC):

    img   = ig.grab()
    img.show()
    frame = np.array(img)

    val = len(Tracker.getContours(frame))  
    c = val                 #need to modify output and take into account premptively detected contours

    input(c)

    if c == nC+1:
        print("One object added")
        Tracker.subject = 1
    elif c == nC -1:
        print("One object lost")
    elif c < nC -1:
        print("Multiple objects lost")
        Tracker.subject = 1
    elif c > nC+1:
        print("Multiple objects added")
    else:
        print("No changes")
    
    return Tracker.subject




