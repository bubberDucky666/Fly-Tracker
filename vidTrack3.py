"""
	
			THE CODE IS (AS OF RIGHT NOW) BUILT SO THAT IT IDENTIFIES NOTABLE CONTOURS (after thresholding) AND THEN TRACKS THE POSITION OF THEIR CENTROIDS
						IF A CONTOUR IS LOST FOR WHATEVER REASON, THE PROGRAM WILL STOP TRACKING IT UNDER THE SAME INDEX
							
			NEED TO FIX/ADD/ADDRESS IN ORDER OF IMPORTANCE:
				- Get threading to work
				- Find a way for multiple position files to be made automatically
				- Prove to Kevin that this is viable

"""
import matplotlib.pyplot as plt
import imageio 			 as im
import numpy   			 as np
import time
import cv2
import _pickle 			 as pickle
import vidThreading      as vT

#------------ Constants --------------

fsource		= '/Users/JKTechnical/Codes/FlyWork/180627/testyWesty.avi'
threshold 	= 90
maxVal		= 100
minArea 	= 400
pname 		= 'posTest.vD'
numContours = 7

#--------------------------------------

#----------- Get type of footage -------------

def vfGet(fsource):
	b = False
	if fsource[-4:] == '.avi':
		#vf    = im.get_reader(fsource)
		b     = True
	elif fsource != '':
		pass
		#vf 	  = cv2.VideoCapture(fsource)
	else:
		pass
		#vf 	  = cv2.VideoCapture(0)

	return b#, vf

#---------------------------------------------

################################################################ Tracker Class ################################################################
#
#       The tracker class is one instance of video tracking; ie it will take one collection of frames and analyize it in order. It can be
# 	    initialized multiple times to analyze multiple videos. Should be able to analyze any video type, however .avi files are generally more 
#		diffifuclt.
#
# 		Required parameters for initialization: 
#			- threshold (type=int): The intensity value used to threshold frame
#			- maxVal 	(type=int): Unimportant, but the intensity of thresholded image 
#			- minArea   (type=int): Minimum area size of tracked contours
#		
#		Attributes:
#			-self.threshold
#			-self.maxVal
#			-self.minArea
#			-self.frame
#			-self.pos
#
#		.getContours() returns a contoured image, a list of contours, and a return boolean. The image can generally be ignored. The list of 
#			contours integral for analyzation. The return value should be checked as well to ensure that the method worked; in the event of a 
#			numContours related error, the method's return boolean will be false
#			Parameters:
#				- frame 	  (type=np.ndarray): An image array
#				- numContours (type=int)       : Optional parameter that specifies number of tracked bodies (prevents errors)
#		
#	
#		.contourAnalyze() method gets positions and saves them based on a contours list. It finds viable contours (based on minArea) and then tracks 
#			centroid. It will add visual indicators (ie boxes and circles) to the given image to aid in visualization. Finally, a list containing the 
#			tracked positions for each body will be saved to a given file. 
#			Parameters:
#				- contours (type=np.ndarray): An array of contours (pixels maybe?)
#				- pname    (type=string)    : Path to output file	
#
#		.preview() will create a named window showing the sequence of frames (as a video) as it recieves them. It will resize the photo as well using a
#			resize factor. If no sizing change is wanted, simply put zero)
#			Parameters:
#				-pic 		  (type=np.ndarray): An image array
#				-resizeFactor (type=int)       : The number by which the image will be scaled 
#				-message      (type=str)   	   : The text displayed above the window
#
#
########################################################################################################################################################

class Tracker(object):
	
	def __init__(self, threshold, maxVal, minArea):
		self.threshold = threshold
		self.maxVal    = maxVal
		self.minArea   = minArea

	def getContours(self, frame, **numContours):
		#intermediate states where frame is being edited'
		self.frame = frame

		frame2     = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame2 	   = cv2.GaussianBlur(frame2, (21,21), 0)
		
		thresh     = cv2.threshold(frame2, threshold, maxVal, cv2.THRESH_BINARY)[1]
		#incredibly important for using imageio to cv2 
		thresh     = cv2.convertScaleAbs(thresh)
		thresh 	   = cv2.dilate(thresh, None, iterations=3)
				
		img, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		#takes into account optional number of contours parameter and 
		#returns False bools if a discrepancy is picked up
		#if ('num' in numContours):
			#if len(contours) != (numContours['num']+1):
				#return False, None, None

		return True, contours, img

	def contourAnalyze(self, contours, pname):
		for i in range(len(contours)):
			#------ Basic Declarations ---------------------

			p       = contours[i]
			area    = cv2.contourArea(contours[i])
			ind1    = -1
					
			#-------------------------------------------------
			
			#------- Contour Calculations --------------------
			 
			if area >= minArea:

				#increase the first indice for position saving
				ind1 = ind1 + 1
				
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
				cv2.circle(self.frame, (mx,my), 5, (0,0,255), 2)
			 
			 #-------------------------------------------------

			 #--------- Positions List Loading/Saving ------------------------
			 
			 	#opens file with positions array as list
			 	#saves to pos, then clears file
				with open(pname, 'r+b') as file:
					pos = pickle.load(file)
					file.truncate(0)

			 	#appends contours' positions to their overall group list
			 	#or creates a new group list and then appends (otherwise return error)
				try:
					pos[ind1].append([mx, my])
					self.pos = pos
				except AttributeError: #IndexError:
					pos.append([])
					pos[ind1].append([mx, my])
					self.pos = pos
				else:
					('OOPSIE WOOPSIE!! UwU We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this!')
			 	
			 	#saves newly edited pos to file
				with open(pname, 'r+b') as file:
					pickle.dump(pos, file)

			 #--------------------------------------------------

	def preview(self, pic, reziseFactor, message):
	 	pic = cv2.resize(pic, None, fx = .5, fy=.5, interpolation=cv2.INTER_AREA)
	 	cv2.imshow(message, pic)
	 	if cv2.waitKey(1) == 27:
	 		input()

	#----------- Show Movement Path -------------
	def plotAllPos(self, pname, cIndice):
		
		with open(pname, 'r+b') as file:
			pos = pickle.load(file)

		g 	  = pos[cIndice]
		t_pos = list(zip(*g))
		x	  = t_pos[0]
		y	  = t_pos[1]

		plt.plot(x,y)
		plt.scatter(x,y)
		plt.draw()

	#---------------------------------------------

	def plotCurrentPos(self, ind):
		g = self.pos[ind]
		x = g[-1][0]
		y = g[-1][1]
		plt.plot(x, y)
		plt.draw()




if __name__ == "__main__":
	#input(fsource[ (len(fsource))-4 : ])
	Tester = Tracker(fsource, maxVal, minArea)
	val    = vfGet(fsource)

	print("Starting video file thread...")
	fvs = vT.VFS(fsource).start()
	time.sleep(1)

	if val:
		start = time.time()
		#for i, pic in enumerate(vf):
			#print('Frame#: ', i)
			#print(time.time()-start, 'seconds\n')

		while fvs.more():
			pic = fvs.read()
			print('pic')
			cv2.imshow('pic', pic)
			
			#if i%4 == 0:
			check, contours, img = Tester.getContours(pic, num=7)

			#check if there are more/less objects than there should be; pass over the frame if so
			if check:				
				Tester.contourAnalyze(contours, pname)

				frame = Tester.frame
				Tester.preview(frame, .25, 'final')
				print('cycle done')
				#Tester.preview(img, .5, 'contoured')

			else:
				print('numContour error')
				pass
		#else:
			#pass

	else:
			__, pic = vf.read()
			img, contours = Tester.getContours(pic, num=7)
			Tester.contourAnalyze(contours, pname)
			
			frame = Tester.frame
			Tester.preview(frame, .5, 'final')
			#Tester.preview(img, .5, 'contoured')


