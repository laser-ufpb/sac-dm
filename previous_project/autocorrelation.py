
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.interpolate import spline


import math

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import wave

import sys



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
#main:


filename = sys.argv[1]

# Este e o unico ponto que voce deve configurar, de acordo com o formato do arquivo de entrada

#data = np.genfromtxt(filename, delimiter='', names=['y'])
#data = np.genfromtxt(filename, delimiter=' ', names=['x', 'y'])
data = np.genfromtxt(filename, delimiter=';', names=['x', 'y','z'])
#data = np.genfromtxt(filename, delimiter=',', names=['x', 'y','z','s','t'])
#data = np.genfromtxt(filename, delimiter=';', names=['z','x','y'])
#data = np.genfromtxt(filename, delimiter=',', names=['x','z','y','t','d'])




N = int(sys.argv[2]) # quantidade de colunas

result = autocorrelation(data['z'], N)


#************************************
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

ax3.plot(data['z'], color='b', label='Signal')


# Grafico Butterfly
#plt.plot(data['y'],data['z'],'r-',linewidth=2.0)
#plt.title('Phase space',{'fontsize':12})
#plt.xlim([-4.5,4.5])
#plt.xlabel('Y',{'fontsize':12})
#plt.ylabel('Z',{'fontsize':12})
#plt.tick_params(axis='both',labelsize=12)


plt.show()




