"""
	
			THE CODE IS (AS OF RIGHT NOW) BUILT SO THAT IT IDENTIFIES NOTABLE CONTOURS (after thresholding) AND THEN TRACKS THE POSITION OF THEIR CENTROIDS
						IF A CONTOUR IS LOST FOR WHATEVER REASON, THE PROGRAM WILL STOP TRACKING IT UNDER THE SAME INDEX
							
			NEED TO FIX/ADD/ADDRESS IN ORDER OF IMPORTANCE:
				- When a contour irregularity is found, save the frame number (and maybe the edited frame as well?)
				- Check position file after a full run-through with matplotlib
				- Edit pseudocode
-
"""

import matplotlib.pyplot as plt
import imageio 			 as im
import numpy   			 as np
import time
import cv2
import _pickle 			 as pickle
import vidThreading      as vT
import os

#------------ Constants --------------

#fsource		= '/Users/JKTechnical/Codes/FlyWork/dNeurons/(2)AA_ctrl_d1_d2_2018-06-26-105036-0000.avi'
threshold 	= 90
maxVal		= 255
minArea 	= 400
maxArea     = 4000
#pname 		= '/Users/JKTechnical/Codes/FlyWork/pos(2).vD'
numContours = 7


class Tracker(object):
	
	def __init__(self, threshold, maxVal, minArea, maxArea):
		self.threshold = threshold
		self.maxVal    = maxVal
		self.minArea   = minArea
		self.maxArea   = maxArea
		self.errInd    = []
		self.subject   = 0

	def getContours(self, frame):
		#intermediate states where frame is being edited'
		self.frame = frame

		frame2     = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame2 	   = cv2.GaussianBlur(frame2, (25,25), 0)
		
		thresh     = cv2.threshold(frame2, self.threshold, self.maxVal, cv2.THRESH_BINARY)[1]
		
		#incredibly important for using imageio to cv2 
		thresh     = cv2.convertScaleAbs(thresh)
		thresh 	   = cv2.dilate(thresh, None, iterations=1)
				
		img, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		return contours, img

	def contourAnalyze(self, contours, pname, **numContours):

		if ('num' in numContours):
			self.numContours = numContours['num']
			#print(self.numContours)

		#takes contours above {minArea} and below {maxArea}
		rcontours = [] 
		#holds the {# of contours} indices
		indList   = []
		#holds the {# of contours} positions
		mxyList   = []
		

		ind1      = -1
		
		for i in range(len(contours)):
			#------ Basic Declarations ---------------------

			p         = contours[i]
			#desired area
			area      = cv2.contourArea(contours[i])
			
			#-------------------------------------------------
			
			#------- Contour Calculations --------------------
			 
			if area >= self.minArea and area <= self.maxArea:

				#increase the first indice for position saving
				ind1 = ind1 + 1
				indList.append(ind1)
				
				#make rotating boxes around points
				rect = cv2.minAreaRect(p)
				box	 = cv2.boxPoints(rect)
				box  = np.int0(box)

			 	#put the box onto the original frame
				cv2.drawContours(self.frame, [box], 0, (0,255,0), 2)
				
			 	#store the position of the contoured objects
			 	#ASSUMES THAT NEW CONTOURS AREN'T BEING INTRODUCED				
				m  = cv2.moments(p)
				mx = int(m['m10']/m['m00'])
				my = int(m['m01']/m['m00'])
				mxyList.append([mx,my])
				cv2.circle(self.frame, (mx,my), 5, (0,0,255), 2)
				cv2.putText(self.frame, 'HEY', (mx,my), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
				rcontours.append(p)

		if len(rcontours) != self.numContours:	
			#print('\nduck\n')
			return False, rcontours

		
		elif len(rcontours) == self.numContours:
			#print('\nPEEPEE\n')
			self.save(pname, indList, mxyList, pos)	
		
			#saves newly edited pos to file
			with open(pname, 'w+b') as file:
				pickle.dump(pos, file)

			#returns check and contours that meet area standards	
			return True, rcontours
			 #-------------------------------------------------

			 #--------- Positions List Loading/Saving ------------------------
	def save(self, pname, indList, mxyList, pos):		 

		for ind1 in indList:
		 	mx = mxyList[ind1][0]
		 	my = mxyList[ind1][1]
			
			#appends contours' positions to their overall group list
		 	#or creates a new group list and then appends (otherwise return error)
		 	try:
		 		pos[ind1].append([mx, my])
		 	except IndexError:
		 		pos.append([])
		 	#print('list len is {}'.format(len(pos[ind1])))

			 #--------------------------------------------------

	def preview(self, pic, rF, message):

	 	pic = cv2.resize(pic, None, fx = rF, fy= rF, interpolation=cv2.INTER_AREA)
	 	cv2.imshow(message, pic)
	 	if cv2.waitKey(1) == 27:
	 		input()


if __name__ == "__main__":
	
	for fsource in os.listdir('/Users/JKTechnical/Codes/FlyWork/analyzeMe'):
		
		#clears the global pos variable
		pos = [[] for i in range(numContours)]
		print('pos list cleaned')
		print('|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|')
		print('starting new fsource: {}'.format(str(fsource)))


		#print(fsource[-4:])
		if fsource[-4:] == '.avi':

			vidID = str(fsource)[1:2]
			pname = '/Users/JKTechnical/Codes/FlyWork/pos/pos'+ vidID +'.vd'

			Tester = Tracker(threshold, maxVal, minArea, maxArea)

			print("Starting video file thread...\n")
			fvs = vT.VFS('/Users/JKTechnical/Codes/FlyWork/analyzeMe/'+fsource).start()
			time.sleep(3.5)

			iteration = 0

			aaa    = []
			iFrame = []
			fframe = []

			#while there are more frames in the queue
			while fvs.more():

				tFrame = fvs.read()
				time.sleep(.125/6)
				print('butt')
				aaa.append(tFrame)

				iFrame = np.add(list(i for i in aaa))
			for i in range(len(iFrame)):
				for j in range(len(iFrame)):
					iFrame[i][j] = (iFrame[i][j] / len(iFrame))

			cv2.imshow('Average', iFrame)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			input()

			'''
				pic = fvs.read()

				contours, img    = Tester.getContours(pic)
				
				numCheck, rcontours = Tester.contourAnalyze(contours, pname, num=numContours)
				frame            = Tester.frame
				
				#check if there are more/less objects than there should be; pass over the frame if so
				if numCheck:				
					
					print('Frame {} done \n'.format(iteration))
					iteration = iteration + 1

				else:
					
					print('numContour error. Detected ' + str(len(rcontours)))
					Tester.errInd.append(iteration)
					print('This is error number ' + str(len(Tester.errInd)))
					iteration = iteration + 1
'''

	print('done')
	print('There were {} total errors\n\n'.format(str(len(Tester.errInd))))
	
	print("list 5 sublengths:")
	with open('/Users/JKTechnical/Codes/FlyWork/pos/pos5.vd', 'r+b') as file:
		a = pickle.load(file)
		for i in a:
			print(len(i))












