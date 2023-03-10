import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import matplotlib.colors as mcolors

def moving_average(a, n=3) :
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

def compress(a, n=3):
	i=0
	j=n
	k=0
	ret = np.zeros(1)
	for k in range(int(len(a)/n)):
		ret = np.append(ret,np.average(a[i:j]))
		i = j
		j = j+n
	return ret
    

def show(dataset, title):
	
	print("dataset ", len(dataset))
	fig, ax = plt.subplots()

	plt.ylabel(title) 
	plt.xlabel('Time (ms)')
	
	ax.set_title(title)  
	colors = list(mcolors.CSS4_COLORS) 
	for i in range(len(dataset)):
		print("sub dataset ", len(dataset[i]))
		ax.plot(dataset[i],color=colors[i+10], label=("Data" ,i))
		
		
	plt.legend(loc='upper left')


	#plt.show()
	return 1
