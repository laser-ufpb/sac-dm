
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz

#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import h5py

import sys

from scipy.interpolate import spline


def sac_dm(data, N, threshold):


	
	M = len(data)
	#M = 50000

	print "Numero de amostras: ", M
	rho = 0.0

	size = 1 + int(M)/N
	sacdm=[0.0] * size


	up = 0
	peaks = 0
	i = 0
	n = N
	j = 0
	while i < M-2:
		a = data[i]
		b = data[i+1]
		c = data[i+2]

		if b > (a*(1+threshold)) and b > (c*(1+threshold)):
			peaks = peaks + 1
			
		if i == n:
			rho =  peaks/float(N)

			sacdm[j] = rho 
			
			j = j + 1
			n = n + N
			peaks = 0
		i = i+1

	#plot SAC-DM:
	#print data
	return sacdm

	


#********* Main ********



N = int(sys.argv[3])
file = sys.argv[1]
file2 = sys.argv[2]

data1 = np.genfromtxt(file, delimiter=',', names=['t', 'x', 'y','z'])
data2 = np.genfromtxt(file2, delimiter=',', names=['t', 'x', 'y','z'])


sac = sac_dm(data1['y'], N, 0.0)
sac2 = sac_dm(data2['y'], N, 0.0)


fig = plt.figure()


ax = fig.add_subplot(211)
ax.set_title("Original Signals and SAC-DM")   
ax.plot(data1['z'],color='r', label='Signal 1')
ax.plot(data2['z'],color='g', label='Signal 2')
plt.ylabel('Amplitude') 
#plt.xlabel('Time (sec.)')
ax.legend(['Healthy', 'Failure'], loc='upper right')

x = np.array(range(0, len(sac)))
x = x * N

x2 = np.array(range(0, len(sac2)))
x2 = x2 * N


ax3 = fig.add_subplot(212)
ax3.plot(x, sac, color='r', label='SAC-DM 1')
ax3.plot(x2, sac2, color='g', label='SAC-DM 2')
plt.ylabel('Frequency') 
plt.xlabel('Time (sec.)')
#ax3.legend(['SAC-DM 1', 'SAC-DM 2'], loc='upper right')



fig2 = plt.figure()
ax2 = fig2.add_subplot(111)


kwargs = dict(histtype='stepfilled', alpha=0.3, density=True, bins=40, ec="k")

plt.hist(sac, **kwargs)
plt.hist(sac2, **kwargs)


plt.show()





	





