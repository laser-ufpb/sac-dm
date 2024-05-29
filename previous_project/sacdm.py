
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.signal import find_peaks, peak_prominences

#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import h5py

import sys
import time


from scipy.interpolate import spline

def get_data_from_wav(filename):
	Fs, data = read(filename)
	data = data[:,0]
	return data, Fs

# Calcula SAC-DM medio total utilizando a funcao find_peaks do Python
def sac_dm_avg(data):
	peaks, _ = find_peaks(data)
	
	npeaks = 0.0 + len(peaks)
	n = len(data)
	
	return npeaks/n


# Calcula SAC-DM utilizando a funcao find_peaks do Python
def sac_dm(data, N):
	
	M = len(data)
	size = 1 + int(M)/N
	sacdm=[0.0] * size


	inicio = 0
	fim = N
	for k in range(size):
		peaks, _ = find_peaks(data[inicio:fim])
		v = np.array(peaks)
		sacdm[k] = 1.0*len(v)/N
		inicio = fim
		fim = fim + N

		
	
	return sacdm

# Calcula SAC-AM (amplitude media dos maximos) utilizando a funcao find_peaks do Python
def sac_am(data, N):
	
	M = len(data)
	size = 1 + int(M)/N
	sacdm=[0.0] * size


	inicio = 0
	fim = N
	for k in range(size):
		peaks, _ = find_peaks(data[inicio:fim])
		v = np.abs(data[peaks])
		s = sum(v)
		sacdm[k] = 1.0*s/N
		inicio = fim
		fim = fim + N

		
	
	return sacdm

# Calcula SAC-DM utilizando a funcao find_peaks do Python
def sac_dm_slow(data, N):
	peaks, _ = find_peaks(data)
	
	M = len(data)
	size = 1 + int(M)/N
	sacdm=[0.0] * size
	picos=[0.0] * size

	inicio = 0
	fim = N

	v = np.array(peaks)
	for k in range(size):
		#sum(v<fim) retorna a quantidade de elementos em v menores que fim. Ou seja, a quantidade de True da clausula
		sacdm[k] = sum(v<fim) - sum(v<inicio)
		inicio = fim
		fim = fim + N
	
	return np.true_divide(sacdm,N),peaks


# Calcula SAC-PM a prominencia (altura) media dos picos utilizando a funcao peak_prominences do Python
def sac_pm(data):
	peaks, _ = find_peaks(data)
	return peaks


# Calcula SAC-AM a largura  media dos picos utilizando a funcao peak_width do Python
def sac_wm(data):
	peaks, _ = find_peaks(data)
	return len(peaks)/len(data)


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def sac_dm_old(data, N, threshold):
	
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

			if rho != 0:
				sacdm[j] = rho 
				#sacdm[j]=1/(6*rho)
				#print "peaks: ", peaks , " N: ", N, " rho: ", rho, "sacdm: ", sacdm[j]
			else:
				sacdm[j] = 0
			j = j + 1
			n = n + N
			peaks = 0
		i = i+1

	#plot SAC-DM:
	#print data
	return sacdm

	


#********* Main ********

million = 1000*10000
x =  np.random.randn(million) 


start_time = time.time()
sac = sac_dm_old(x, 1000, 0.1)
end_time = time.time()

avg = np.average(sac)
print "SAC-DM Data (old): ", avg , end_time-start_time, "seconds"


start_time = time.time()
sac = sac_dm(x, 1000)
end_time = time.time()

avg = np.average(sac)
print "SAC-DM Data (slow2): ", avg , end_time-start_time, "seconds"

start_time = time.time()
sac = sac_am(x, 1000)
end_time = time.time()

avg = np.average(sac)
print "SAC-AM: ", avg , end_time-start_time, "seconds"



start_time = time.time()
sac2 = sac_dm_avg(x)
end_time = time.time()

print "SAC-DM: ", sac2, end_time-start_time, "seconds"



#plot(sac, peaks)

#print sac

#plt.plot(x)
#plt.plot(peaks, x[peaks], "x")
#plt.vlines(x=peaks, ymin=contour_heights, ymax=x[peaks])
#plt.show()



'''

N = int(sys.argv[2])
filename = sys.argv[1]


#data = np.genfromtxt(filename, delimiter=',', names=['x', 'y','z','s','t'])

	#data = np.genfromtxt(filename, delimiter=';', names=['y', 'z','x'])
	#data = np.genfromtxt(filename, delimiter=' ', names=['y'])

data = np.genfromtxt(filename, delimiter=',', names=['t', 'x','y','z'])


sac = sac_dm(data['z'], N, 0.1)

fig3 = plt.figure()

plt.ylabel('Number of requests') 
plt.xlabel('Time (ms)')
ax3 = fig3.add_subplot(111)
ax3.set_title("SAC-DM")   
ax3.plot(sac,color='r', label='MACCD2')
#ax3.plot(sac2,color='g', label='Outro')

ax3.legend(['y = MACCD2'], loc='upper left')
#ax3.legend(['y = MACCD2', 'y = Outro'], loc='upper left')



plt.show()




'''
	





