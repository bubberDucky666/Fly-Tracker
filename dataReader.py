import matplotlib.pyplot 					as plt
import _pickle 			 					as pickle
import numpy 			 					as np
from scipy             import stats  		as st
import xlsxwriter       			 		as xl 

def loadFile(pname):
	with open(pname, 'r+b') as file:
		pos = pickle.load(file)
	#input(len(pos[1]))
	return pos

def chartMake(pos):
	posList = pos5
	xList      = []
	fig, axs = plt.subplots(7, 1, num='Experiment 5')
	#print(len(posList))

	for i in range(len(posList)):

		#print(posList[i])
		t_pos = np.array(list(zip(*posList[i])))	

		xList.append(list((i/640.)-1 for i in t_pos[0]))
		input(len(xList))
		
		axs[i].plot(range(len(posList[i])), xList[i])
		if i == 0:
			axs[i].set_title('Fly Position Over Time')
		if i == 6:
			axs[i].set_xlabel('Frame')
		if i == 3:
			axs[i].set_ylabel('Position')
		print('made an axis')

	print('about to show')
	plt.show()
	print('done')

def ttest(pos):
	rDict = {}
	for i in range(len(pos)):
		for j in range(len(pos[i+1:])):
			r                                          = st.ttest_ind(pos[i][0],pos[j][0])
			rDict['{} with {}'.format(pos[i], pos[j])] = r
			print('burp')

	for item in rDict:
		print(rDict[item])
		print('\n')


pos3 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos3.vd')
pos5 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos5.vd')
pos7 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos7.vd')
pos8 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos8.vd')
pos9 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos9.vd')

ttest(pos5)










