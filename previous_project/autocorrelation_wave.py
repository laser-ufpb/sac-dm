
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal

from scipy.io.wavfile import read, write
from numpy.fft import fft, ifft

import math

from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz


#import pandas as pd
#import peakutils

# the ipython magic below must be commented out in the .py file, since it doesn't work.
#get_ipython().magic(u'matplotlib inline')
#get_ipython().magic(u"config InlineBackend.figure_format = 'retina'")
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import h5py

import sys


#Autocorrelation:

def autocorrelation(data, N):

	dataset_size = len(data) # %tamanho do sinal / amostragem
	M = int(math.floor(dataset_size/N)) #numero de linhas
 
	flag = 0 
	matriz = np.zeros(shape=(M,N))

	print 'data size ', dataset_size
	print 'colunas ', N
	print 'linhas ', M

	# N = columns, M = lines

	for i in range (0,M):
		for j in range(0,N):
			matriz[i][j] =  data[flag]
			flag = flag + 1
		
	#%% ******************* Produto pela 1a coluna *******************************

	c = np.zeros(shape=(M,N))

	for i in range (0,M):
		for j in range(0,N):
			c[i][j] = matriz[i][0]*matriz[i][j]
    

 	#%% ******************* Media das colunas *******************************

	media_I = c.mean(0)

	corr = np.zeros(shape=(N))


	for j in range(0,N):
		corr[j] = media_I[j]/media_I[0]
   
   	return corr
 
#************************************


filename = sys.argv[1]

Fs, data = read(filename)
data = data[:,0]
print ("Frequency: ", Fs)


#N = 16 # amostras
N = int(sys.argv[2])

result = autocorrelation(data, N)

fig2 = plt.figure()
plt.ylabel('Correlation') 
plt.xlabel('Time')

ax2 = fig2.add_subplot(111)
ax2.set_title("Autocorrelation") 

ax2.plot(result, color='g', label='Autocorrelation')


#************************************
fig3 = plt.figure()
plt.ylabel('Amplitude') 
plt.xlabel('Time (ms)')

ax3 = fig3.add_subplot(111)
ax3.set_title("Signal") 

ax3.plot(data, color='b', label='Signal')


plt.show()






