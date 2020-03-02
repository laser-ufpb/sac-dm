
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

filename = sys.argv[1]

Fs, data = read(filename)


data = data[:,0]
print ("Frequency: ", Fs)



fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Hive")    
ax1.set_xlabel('time')
ax1.set_ylabel('amplitude')

ax1.plot(data, color='r', label='Hive Sound')

leg = ax1.legend()


#Autocorrelation:

 
#%% MATRIX NxM
dataset_size = len(data) # %tamanho do sinal / amostragem
#N = 16 # amostras
N = int(sys.argv[2])
M = int(math.floor(dataset_size/N)) #numero de linhas
 
flag = 0 
matriz = [[0.0 for x in range(N)] for y in range(M)]

print 'data size ', dataset_size
print 'colunas ', N
print 'linhas ', M

# N = columns 
# M = lines

for i in range (0,M):
	for j in range(0,N):
		matriz[i][j] =  data[flag]
		flag = flag + 1
		#print 'flag ', flag

#%% ******************* Produto pela 1a coluna *******************************

c = [[0.0 for x in range(N)] for y in range(M)]
for i in range (0,M):
	for j in range(0,N):
		c[i][j] = matriz[i][0]*matriz[i][j]
    

 #%% ******************* Media das colunas *******************************

media_I = [0.0 for x in range(N)] 
soma = 0.0
for j in range(0,N):
	for i in range (0,M):
		soma = soma + c[i][j]
	media_I[j] = soma/M
	soma = 0.0


#*************** Autocorrelacao **********************
corr = [0.0 for x in range(N)] 
for j in range(0,N):
	#result = result + matriz[i][0]*matriz[i][j]	
	corr[j] = media_I[j]/media_I[0]
	
#print '%.18e' % corr[0]    
   
#*Comprimento a meia altura***********************************

x1=0.0 
x2=0.0
y1=0.0
y2 = 0.0
coef = 0.0
comp = 0

print "Autocorrelation:"
for k in range(0,50):
	print corr[k]
 
#************************************
fig2 = plt.figure()
plt.ylabel('Correlation') 
plt.xlabel('Time')

ax2 = fig2.add_subplot(111)
ax2.set_title("Autocorrelation") 

ax2.plot(corr, color='g', label='Autocorrelation')


#************************************
fig3 = plt.figure()
plt.ylabel('Amplitude') 
plt.xlabel('Time (ms)')

ax3 = fig3.add_subplot(111)
ax3.set_title("Signal") 

ax3.plot(data, color='b', label='Signal')


# Grafico Butterfly
#plt.plot(data['y'],data['z'],'r-',linewidth=2.0)
#plt.title('Phase space',{'fontsize':12})
#plt.xlim([-4.5,4.5])
#plt.xlabel('Y',{'fontsize':12})
#plt.ylabel('Z',{'fontsize':12})
#plt.tick_params(axis='both',labelsize=12)


plt.show()






