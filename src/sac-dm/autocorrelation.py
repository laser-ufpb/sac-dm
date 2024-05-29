
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz



import math

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import wave

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/alisson/SAC-DM')

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def autocorrelation(data, N):

	dataset_size = len(data) # %tamanho do sinal / amostragem
	M = int(math.floor(dataset_size/N)) #numero de linhas
 
	flag = 0 
	matriz = np.zeros(shape=(M,N))

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
'''


filename = sys.argv[1]

# Este e o unico ponto que voce deve configurar, de acordo com o formato do arquivo de entrada

#data = np.genfromtxt(filename, delimiter='', names=['y'])
#data = np.genfromtxt(filename, delimiter=' ', names=['x', 'y'])
#data = np.genfromtxt(filename, delimiter=';', names=['x', 'y','z'])
data = np.genfromtxt(filename, delimiter=',', names=['t', 'x','y','z'])
#data = np.genfromtxt(filename, delimiter=';', names=['z','x','y'])
#data = np.genfromtxt(filename, delimiter=',', names=['x','z','y','t','d'])


#mat = scipy.io.loadmat('M1_H1_CCW_current_03.mat')
mat = scipy.io.loadmat('M1_H2_CW_current_02.mat')
data = mat['y1']

N = 1000 # quantidade de colunas

result = autocorrelation(data, N)


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

ax3.plot(data, color='b', label='Signal')


# Grafico Butterfly
#plt.plot(data['y'],data['z'],'r-',linewidth=2.0)
#plt.title('Phase space',{'fontsize':12})
#plt.xlim([-4.5,4.5])
#plt.xlabel('Y',{'fontsize':12})
#plt.ylabel('Z',{'fontsize':12})
#plt.tick_params(axis='both',labelsize=12)


plt.show()


'''


