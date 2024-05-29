
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.signal import find_peaks, peak_prominences

from scipy.io.wavfile import read, write
from numpy.fft import fft, ifft


#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import h5py

import sys

from scipy.interpolate import spline

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

def sac_dm_file_old(filename, N, threshold):


	# Este e o unico ponto que voce deve configurar, de acordo com o formato do arquivo de entrada

	#data = np.genfromtxt(filename, delimiter=',', names=['x', 'y','z','s','t'])

	#data = np.genfromtxt(filename, delimiter=';', names=['y', 'z','x'])
	Fs, data = read(filename)
	data = data[:,0]
	#print 'Frequencia de amostragem do audio: ', Fs

	N = Fs
	#data = np.genfromtxt(filename, delimiter=' ', names=['y'])


	#index = peakutils.indexes(data['y'], thres=threshold, min_dist=distance)


	M = len(data)
	#M = 50000

	#print "Numero de amostras: ", M
	rho = 0.0

	size = 1 + int(M)/N
	sacdm=[0.0] * size
	sacam=[0.0] * size


	amp = 0
	peaks = 0.0
	i = 0
	n = N
	j = 0
	while i < M-2:
		a = data[i]
		b = data[i+1]
		c = data[i+2]

		if b > (a*(1+threshold)) and b > (c*(1+threshold)):
			peaks = peaks + 1
			if (b-a)>(b-c):
				amp = amp + (b-c)
			else:
				amp = amp + (b-a)
		if i == n:
			rho =  peaks/float(N)
			sacam = amp/float(N)
			if rho != 0:
				sacdm[j] = rho 
				#sacdm[j]=1/(6*rho)
				#print "peaks: ", peaks , " N: ", N, " rho: ", rho, "sacdm: ", sacdm[j]
			else:
				sacdm[j] = 0
			j = j + 1
			n = n + N
			peaks = 0.0
			amp = 0.0
		i = i+1

	#plot SAC-DM:
	#print data
	return sacdm, sacam, data

	
def get_data_from_wav(filename):
	Fs, data = read(filename)
	data = data[:,0]
	return data, Fs


#file1 = "ddos/dados/maccdc2012_00008_tratado_pacotes.csv"
#file2 = "ddos/dados/access.log_pacotesporsegundo"

threshold = 0.0

data, N = get_data_from_wav(sys.argv[1])



sac = sac_am(data, N)
avg = np.average(sac)
std = np.std(sac)


print sys.argv[1], ";", avg, ";", std

'''
fig3 = plt.figure()

plt.ylabel('Peaks/sec.') 
plt.xlabel('Time (sec.)')
ax3 = fig3.add_subplot(111)
ax3.set_title("SAC-DM")   
ax3.plot(sac,color='r', label='With queen')
ax3.plot(sac2,color='g', label='Without queen')

ax3.legend(['Hive with a queen', 'Hive without a queen'], loc='upper right')
#ax3.legend(['y = MACCD2', 'y = Outro'], loc='upper left')

plt.savefig(file + ".png")





plt.show()

'''

'''
fig = plt.figure()

plt.ylabel('dB') 
plt.xlabel('Time (sec.)')
ax = fig.add_subplot(111)
ax.set_title("Sound")   
ax.plot(sinal,color='r', label='With queen')
ax.plot(sinal2,color='g', label='Without queen')
ax.legend(['Hive with a queen', 'Hive without a queen'], loc='upper right')

plt.show()

'''



	





