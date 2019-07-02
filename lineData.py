import matplotlib.pyplot as plt
import _pickle 			 as pickle
import numpy 			 as np

def loadFile(pname):
	with open(pname, 'r+b') as file:
		pos = pickle.load(file)
		return pos

def arrange(name):
	mean = np.mean(name)
	return mean

def unpack(form, pos):
	global errorCount
	try:
		#print(len(pos))
		for i in pos:
			for j in i:
				#print(form+'\n')
				form.append(-((j[0]-640)/640))
		return form
	except TypeError:
		errorCount = errorCount+1
		print('\n\n\n\n___________________________________________________\n\n\n\n')


def main():

	pos1 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos3.vd')
	pos2 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos5.vd')
	pos3 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos7.vd')
	pos4 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos8.vd')
	pos5 = loadFile('/Users/JKTechnical/Codes/FlyWork/pos/pos9.vd')

	ctr = []
	d1  = []
	d2  = []
	ln1 = []
	op  = []

	means = []

	for i in range(len(pos4)):
		for j in range(len(pos4[i])):
			mx   		  = pos4[i][j][0]
			p    		  = (-mx + 640)/640
			pos4[i][j][0] = p


	unpack(ctr, pos1[:1])
	unpack(ctr, pos2[:1])
	unpack(ctr, pos3[:1])
	unpack(ctr, pos4[4:])   
	unpack(ctr, pos5[:1])
	std1 = np.std(ctr)
	means.append(arrange(ctr))

	unpack(d1, pos1[1:])
	unpack(d1, pos2[1:]) 
	unpack(d1, pos3[1:3]) 
	unpack(d1, pos5[4:]) 
	std2 = np.std(d1)
	means.append(arrange(d1))

	unpack(d2, pos1[3:])
	unpack(d2, pos4[1:4]) 
	unpack(d2, pos5[4])
	std3 = np.std(d2)  
	means.append(arrange(d2))

	unpack(ln1, pos3[3:])
	unpack(ln1, pos4[:1])
	std4 = np.std(ln1)
	means.append(arrange(ln1))

	unpack(op, pos5[2:3])
	std5 =  np.std(op)
	means.append(arrange(op))

	print('{} errors were detected'.format(errorCount))
	print(std1)
	print(std2)
	print(std3)
	print(std4)
	print(std5)		

	fig1, ax1 = plt.subplots()

	ax1.bar(1, height = means[0])
	ax1.errorbar(1, means[0], yerr=std1)
	print('ctrl height is {}'.format(means[0]))
	
	ax1.bar(2, height = means[1])
	ax1.errorbar(2, means[1], yerr=std2)
	print('d1 height is {}'.format(means[1]))

	ax1.bar(3, height = means[2])
	ax1.errorbar(3, means[2], yerr=std3)
	print('d2 height is {}'.format(means[2]))

	ax1.bar(4, height = means[3])
	ax1.errorbar(4, means[3], yerr=std4)
	print('ln1 height is {}'.format(means[3]))

	ax1.bar(5, height = means[4])
	ax1.errorbar(5, means[4], yerr=std5)
	print('op height is {}'.format(means[4]))

	ax1.set(title='Line Preference Index')
	plt.show()


if __name__ == '__main__':
	errorCount = 0

	main()





