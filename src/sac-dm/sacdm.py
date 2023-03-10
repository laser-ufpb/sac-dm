# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.signal import find_peaks, peak_prominences

#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.io

#import h5py

import sys
import time

import autocorrelation as auto
import chaos
import util

import os
import os.path as path


# def get_data_from_wav(filename):
# 	Fs, data = read(filename)
# 	data = data[:,0]
# 	return data, Fs

# Calcula SAC-DM medio total utilizando a funcao find_peaks do Python
def sac_dm_avg(data):
	peaks, _ = find_peaks(data)
	
	npeaks = 0.0 + len(peaks)
	n = len(data)
	
	return npeaks/n


# Calcula SAC-DM utilizando a funcao find_peaks do Python
def sac_dm(data, N):
	
	M = len(data)
	size = 1 + int(M/N)
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
	size = 1 + int(M/N)
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
	size = 1 + int(M/N)
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


def sac_dm_old(data, N, threshold):
	
	M = len(data)
	#M = 50000

	print ("Numero de amostras: ", M)
	rho = 0.0

	size = 1 + int(M/N)
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



def test(file1, file2):
	N = int(sys.argv[3])
	
	#mat = scipy.io.loadmat(file1)
	#mat2 = scipy.io.loadmat(file2)
	#data = mat['y1']
	#data2 = mat2['y1']
	

	# d = pd.read_csv(filename)
	# d2 = pd.read_csv(filename2)

	#criando caminho ate a pasta drone_signals
	aux_path = path.abspath(path.join("../.."))
	path_to_drone_signals = aux_path + "/files/drone_signals/"
	
	#concatenando o nome dos arquivos ao caminho criado
	path_file1 = path_to_drone_signals + filename
	path_file2 = path_to_drone_signals + filename2
	
	#convertendo o caminho criado, de str para path
	os.path.normpath(path_file1)
	os.path.normpath(path_file2)
	
	
	d = np.genfromtxt( path_file1, delimiter=';', names=['x','y','z','s','t'])
	d2 = np.genfromtxt( path_file2, delimiter=';', names=['x','y','z','s','t'])


	data = d['z'].reshape(-1)
	data2 = d2['z'].reshape(-1)


	data = data.flatten()
	data2 = data2.flatten()

	#data = np.genfromtxt(file1name, delimiter='	')
	#data2 = np.genfromtxt(file2, delimiter='	')


	sac = sac_dm(data, N)
	am = sac_am(data, N)
	#pm = sac_pm(data, N)
	#wm = sac_wm(data, N)
	
	sac2 = sac_dm(data2, N)
	am2 = sac_am(data2, N)
	#pm2 = sac_pm(data2, N)
	#wm2 = sac_wm(data2, N)
	

	util.show([sac, sac2], "SAC-DM")
	util.show([am, am2], "SAC-AM")
	#util.show(pm, pm2, "SAC-PM")
	#util.show(wm, wm2, "SAC-WM")

	
	


#************************************

	# corr = auto.autocorrelation(data, N)
	# corr2 = auto.autocorrelation(data2, N)

	# util.show([corr, corr2], "Autocorrelation")

	# #le = lyapunov_e(data[0:10000], 1000)
	# lr = chaos.lyapunov_e(data, N)
	# lr2 = chaos.lyapunov_e(data2, N)

	# #print (le.shape)
	# print (lr.shape)

	# util.show([lr, lr2], 'lyapunov coef')

	# l = max(lr)
	# l2 = max(lr2)

	# print ('lyapunov max coef: ', l)
	# print ('lyapunov max coef: ', l2)

	plt.show()

	return 0


#********* Main ********
filename = sys.argv[1]
filename2 = sys.argv[2]

test(filename, filename2)


#comando para execucao
#                  arquivo1        arquivo2         pontos por pico
# python3 sacdm.py accel_80_F0.csv accel_80_F14.csv 10000
	





