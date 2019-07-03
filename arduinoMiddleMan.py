import serial
import time
import vidTrack5
import screenMonitor as sM

prtName = "usbmodem14201"
baud    = 9600

threshold = 90
maxVal    = 225
minArea   = 400
maxArea   = 4000

#Port = serial.Serial(prtName, baud)
time.sleep(2)

Tracker = sM.Tracker(threshold, maxVal, minArea, maxArea)

nC = sM.cal(Tracker)

#You can possibly integrate a timed aspect to things, but maybe not
while True:
    subject = sM.check(Tracker, nC)
   
    if subject == 1:
        #Port.write(1)
        
        while True:
            subject = sM.check(Tracker, nC)
            if subject < 1:
                break