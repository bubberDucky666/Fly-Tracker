

from threading import Thread
from queue 	   import Queue
import sys     
import cv2     
import imageio as im

class VFS:
	def __init__(self, fsource, queueSize = 130):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream  = im.get_reader(fsource)
		self.stopped = False
 
		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queueSize)

	def start(self):
		# start a thread to read frames from the file video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
				
			# keep looping infinitely
			while True:
				
				#keep track of image indice (and an homage to img :P)
				for img in (self.stream):
					#print('i is {}'.format(i))
					#print(img)
			
					# if the thread indicator variable is set, stop the
					# thread
					if self.stopped:
						print('Done')
						return
		 
					# otherwise, ensure the queue has room in it
					if not self.Q.full():
					
						#converts all parts of frame to 8-bit
						frame    = cv2.convertScaleAbs(img)
	 
						# add the frame to the queue
						self.Q.put(frame)

	def read(self):
		# return next frame in the queue
		return self.Q.get()

	def more(self):
		#return True if there are still any frames in the queue
		return self.Q.qsize() > 0

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True












