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


def plot_SAC_AM_DM_drone_signals():
	N = int(sys.argv[1])

	#Abrindo arquivos
	F0 = np.genfromtxt( "../../files/drone_signals/accel_80_F0.csv", delimiter=';', names=['x','y','z','s','t'])
	F6 = np.genfromtxt( "../../files/drone_signals/accel_80_F6.csv", delimiter=';', names=['x','y','z','s','t'])
	F14 = np.genfromtxt( "../../files/drone_signals/accel_80_F14.csv", delimiter=';', names=['x','y','z','s','t'])
	F22 = np.genfromtxt( "../../files/drone_signals/accel_80_F22.csv", delimiter=';', names=['x','y','z','s','t'])

	#Extraindo eixos
	F0_x = F0['x'].reshape(-1)
	F0_y = F0['y'].reshape(-1)
	F0_z = F0['z'].reshape(-1)

	F6_x = F6['x'].reshape(-1)
	F6_y = F6['y'].reshape(-1)
	F6_z = F6['z'].reshape(-1)

	F14_x = F14['x'].reshape(-1)
	F14_y = F14['y'].reshape(-1)
	F14_z = F14['z'].reshape(-1)

	F22_x = F22['x'].reshape(-1)
	F22_y = F22['y'].reshape(-1)
	F22_z = F22['z'].reshape(-1)

	#Obtendo SAC_DM
	sac_dm_F0_x = sac_dm(F0_x, N)
	sac_dm_F0_y = sac_dm(F0_y, N)
	sac_dm_F0_z = sac_dm(F0_z, N)

	sac_dm_F6_x = sac_dm(F6_x, N)
	sac_dm_F6_y = sac_dm(F6_y, N)
	sac_dm_F6_z = sac_dm(F6_z, N)

	sac_dm_F14_x = sac_dm(F14_x, N)
	sac_dm_F14_y = sac_dm(F14_y, N)
	sac_dm_F14_z = sac_dm(F14_z, N)

	sac_dm_F22_x = sac_dm(F22_x, N)
	sac_dm_F22_y = sac_dm(F22_y, N)
	sac_dm_F22_z = sac_dm(F22_z, N)

	#Obtendo SAC_AM
	sac_am_F0_x = sac_am(F0_x, N)
	sac_am_F0_y = sac_am(F0_y, N)
	sac_am_F0_z = sac_am(F0_z, N)

	sac_am_F6_x = sac_am(F6_x, N)
	sac_am_F6_y = sac_am(F6_y, N)
	sac_am_F6_z = sac_am(F6_z, N)

	sac_am_F14_x = sac_am(F14_x, N)
	sac_am_F14_y = sac_am(F14_y, N)
	sac_am_F14_z = sac_am(F14_z, N)

	sac_am_F22_x = sac_am(F22_x, N)
	sac_am_F22_y = sac_am(F22_y, N)
	sac_am_F22_z = sac_am(F22_z, N)

	#Removendo ultima amostra
	sac_dm_F0_x.pop()
	sac_dm_F0_y.pop()
	sac_dm_F0_z.pop()
	
	sac_dm_F6_x.pop()
	sac_dm_F6_y.pop()
	sac_dm_F6_z.pop()

	sac_dm_F14_x.pop()
	sac_dm_F14_y.pop()
	sac_dm_F14_z.pop()

	sac_dm_F22_x.pop()
	sac_dm_F22_y.pop()
	sac_dm_F22_z.pop()

	sac_am_F0_x.pop()
	sac_am_F0_y.pop()
	sac_am_F0_z.pop()
	
	sac_am_F6_x.pop()
	sac_am_F6_y.pop()
	sac_am_F6_z.pop()

	sac_am_F14_x.pop()
	sac_am_F14_y.pop()
	sac_am_F14_z.pop()

	sac_am_F22_x.pop()
	sac_am_F22_y.pop()
	sac_am_F22_z.pop()

	# #					Plotando teste e treino do mesmo arquivo

	# util.showTreinamentoM([sac_am_F0_x, sac_am_F0_y, sac_am_F0_z], "SAC-AM: F0", "F0")
	# util.showTreinamentoM([sac_dm_F0_x, sac_dm_F0_y, sac_dm_F0_z], "SAC-DM: F0", "F0")

	# # Plotando na mesma figura 3 graficos( 1 para cada eixo ), contendo o treinamento e o teste feitos em arquivos diferentes
	
	# #								SAC-AM
	# util.showSAC_figUnicaComTreinoM( ([[sac_am_F0_x, sac_am_F0_y, sac_am_F0_z], [sac_am_F6_x, sac_am_F6_y, sac_am_F6_z], [sac_am_F14_x, sac_am_F14_y, sac_am_F14_z],
	#  								   [sac_am_F22_x, sac_am_F22_y, sac_am_F22_z]]), (f"SAC-AM: Treinamento Metade - N{N}"), ["F0","F6","F14","F22"])

	# #								SAC-DM
	# util.showSAC_figUnicaComTreinoM( ([[sac_dm_F0_x, sac_dm_F0_y, sac_dm_F0_z], [sac_dm_F6_x, sac_dm_F6_y, sac_dm_F6_z], [sac_dm_F14_x, sac_dm_F14_y, sac_dm_F14_z],
	#  								   [sac_dm_F22_x, sac_dm_F22_y, sac_dm_F22_z]]), (f"SAC-DM: Treinamento Metade - N{N}"), ["F0","F6","F14","F22"])


	# # Plotando graficos de forma individual

	# #								SAC-AM
	# util.showSacUnicoEixo([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], "SAC-AM: Eixo X", ["F0","F6","F14","F22"])
	# util.showSacUnicoEixo([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], "SAC-AM: Eixo Y", ["F0","F6","F14","F22"])
	# util.showSacUnicoEixo([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], "SAC-AM: Eixo Z", ["F0","F6","F14","F22"])

	# #								SAC-DM
	# util.showSacUnicoEixo([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], "SAC-DM: Eixo X", ["F0","F6","F14","F22"])
	# util.showSacUnicoEixo([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], "SAC-DM: Eixo Y", ["F0","F6","F14","F22"])
	# util.showSacUnicoEixo([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], "SAC-DM: Eixo Z", ["F0","F6","F14","F22"])


	# # 								Matriz de confusao
	# util.confusionMatrix([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X")
	# util.confusionMatrix([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y")
	# util.confusionMatrix([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z")

	# util.confusionMatrix([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X")
	# util.confusionMatrix([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y")
	# util.confusionMatrix([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z")

	# # 								Matriz de confusao em um arquivo txt e Plot
	# util.cleanTxt()
	# util.confusionMatrixPlotAndTxt([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X", N)
	# util.confusionMatrixPlotAndTxt([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y", N)
	# util.confusionMatrixPlotAndTxt([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z", N)

	# util.confusionMatrixPlotAndTxt([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X", N)
	# util.confusionMatrixPlotAndTxt([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y", N)
	# util.confusionMatrixPlotAndTxt([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z", N)
	
	# # 								Janela Deslizante em um arquivo txt
	util.cleanTxtSliding(int(sys.argv[2]), N)
	util.slidingWindowInTxt([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X", int(sys.argv[2]), N)
	util.slidingWindowInTxt([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y", int(sys.argv[2]), N)
	util.slidingWindowInTxt([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z", int(sys.argv[2]), N)

	util.slidingWindowInTxt([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X", int(sys.argv[2]), N)
	util.slidingWindowInTxt([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y", int(sys.argv[2]), N)
	util.slidingWindowInTxt([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z", int(sys.argv[2]), N)

	# # 								Janela Pulante em um arquivo txt
	# util.cleanTxtJumping(int(sys.argv[2]), N)
	# util.jumpingWindowInTxt([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X", int(sys.argv[2]), N)
	# util.jumpingWindowInTxt([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y", int(sys.argv[2]), N)
	# util.jumpingWindowInTxt([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z", int(sys.argv[2]), N)

	# util.jumpingWindowInTxt([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X", int(sys.argv[2]), N)
	# util.jumpingWindowInTxt([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y", int(sys.argv[2]), N)
	# util.jumpingWindowInTxt([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z", int(sys.argv[2]), N)
	
	plt.show()

	return 0

def plot_SAC_AM_DM_motor_signals():
	N = int(sys.argv[1])

	#Abrindo arquivos
	C0 = np.genfromtxt( "../../files/motor_signals/F0-C0-1797rpm.txt", delimiter=';', names=['x','y','z','t'])
	C2 = np.genfromtxt( "../../files/motor_signals/F0-C2-1794rpm.txt", delimiter=';', names=['x','y','z','t'])
	C4 = np.genfromtxt( "../../files/motor_signals/F0-C4-1790rpm.txt", delimiter=';', names=['x','y','z','t'])
	C10 = np.genfromtxt( "../../files/motor_signals/F0-C10-1776rpm.txt", delimiter=';', names=['x','y','z','t'])
	C20 = np.genfromtxt( "../../files/motor_signals/F0-C20-1748rpm.txt", delimiter=';', names=['x','y','z','t'])

	#Extraindo eixos
	C0_x = C0['x'].reshape(-1)
	C0_y = C0['y'].reshape(-1)
	C0_z = C0['z'].reshape(-1)
	C0_t = C0['t'].reshape(-1)

	C2_x = C2['x'].reshape(-1)
	C2_y = C2['y'].reshape(-1)
	C2_z = C2['z'].reshape(-1)
	C2_t = C2['t'].reshape(-1)

	C4_x = C4['x'].reshape(-1)
	C4_y = C4['y'].reshape(-1)
	C4_z = C4['z'].reshape(-1)
	C4_t = C4['t'].reshape(-1)

	C10_x = C10['x'].reshape(-1)
	C10_y = C10['y'].reshape(-1)
	C10_z = C10['z'].reshape(-1)
	C10_t = C10['t'].reshape(-1)

	C20_x = C20['x'].reshape(-1)
	C20_y = C20['y'].reshape(-1)
	C20_z = C20['z'].reshape(-1)
	C20_t = C20['t'].reshape(-1)

	#Obtendo SAC_DM
	sac_dm_C0_x = sac_dm(C0_x, N)
	sac_dm_C0_y = sac_dm(C0_y, N)
	sac_dm_C0_z = sac_dm(C0_z, N)

	sac_dm_C2_x = sac_dm(C2_x, N)
	sac_dm_C2_y = sac_dm(C2_y, N)
	sac_dm_C2_z = sac_dm(C2_z, N)

	sac_dm_C4_x = sac_dm(C4_x, N)
	sac_dm_C4_y = sac_dm(C4_y, N)
	sac_dm_C4_z = sac_dm(C4_z, N)

	sac_dm_C10_x = sac_dm(C10_x, N)
	sac_dm_C10_y = sac_dm(C10_y, N)
	sac_dm_C10_z = sac_dm(C10_z, N)

	sac_dm_C20_x = sac_dm(C20_x, int(N/4))
	sac_dm_C20_y = sac_dm(C20_y, int(N/4))
	sac_dm_C20_z = sac_dm(C20_z, int(N/4))

	#Obtendo SAC_AM
	sac_am_C0_x = sac_am(C0_x, N)
	sac_am_C0_y = sac_am(C0_y, N)
	sac_am_C0_z = sac_am(C0_z, N)

	sac_am_C2_x = sac_am(C2_x, N)
	sac_am_C2_y = sac_am(C2_y, N)
	sac_am_C2_z = sac_am(C2_z, N)

	sac_am_C4_x = sac_am(C4_x, N)
	sac_am_C4_y = sac_am(C4_y, N)
	sac_am_C4_z = sac_am(C4_z, N)

	sac_am_C10_x = sac_am(C10_x, N)
	sac_am_C10_y = sac_am(C10_y, N)
	sac_am_C10_z = sac_am(C10_z, N)

	sac_am_C20_x = sac_am(C20_x, int(N/4))
	sac_am_C20_y = sac_am(C20_y, int(N/4))
	sac_am_C20_z = sac_am(C20_z, int(N/4))

	#Removendo ultima amostra
	sac_dm_C0_x.pop()
	sac_dm_C0_y.pop()
	sac_dm_C0_z.pop()
	
	sac_dm_C2_x.pop()
	sac_dm_C2_y.pop()
	sac_dm_C2_z.pop()

	sac_dm_C4_x.pop()
	sac_dm_C4_y.pop()
	sac_dm_C4_z.pop()

	sac_dm_C10_x.pop()
	sac_dm_C10_y.pop()
	sac_dm_C10_z.pop()

	sac_dm_C20_x.pop()
	sac_dm_C20_y.pop()
	sac_dm_C20_z.pop()

	sac_am_C0_x.pop()
	sac_am_C0_y.pop()
	sac_am_C0_z.pop()
	
	sac_am_C2_x.pop()
	sac_am_C2_y.pop()
	sac_am_C2_z.pop()

	sac_am_C4_x.pop()
	sac_am_C4_y.pop()
	sac_am_C4_z.pop()

	sac_am_C10_x.pop()
	sac_am_C10_y.pop()
	sac_am_C10_z.pop()

	sac_am_C20_x.pop()
	sac_am_C20_y.pop()
	sac_am_C20_z.pop()

	# # Criando e plotando graficos para o treinamento de SAC-AM

	# Plotando graficos de forma individual

	# #								SAC-AM
	# util.showTreinamentoM([sac_am_C0_x, sac_am_C0_y, sac_am_C0_z], (f"SAC-AM: Arquivo C0 - N{N}"), "C0")
	# util.showTreinamentoM([sac_am_C2_x, sac_am_C2_y, sac_am_C2_z], (f"SAC-AM: Arquivo C2 - N{N}"), "C2")
	# util.showTreinamentoM([sac_am_C4_x, sac_am_C4_y, sac_am_C4_z], (f"SAC-AM: Arquivo C4 - N{N}"), "C4")
	# util.showTreinamentoM([sac_am_C10_x, sac_am_C10_y, sac_am_C10_z], (f"SAC-AM: Arquivo C10 - N{N}"), "C10")
	# util.showTreinamentoM([sac_am_C20_x, sac_am_C20_y, sac_am_C20_z], (f"SAC-AM: Arquivo C20 - N{int(N/4)}"), "C20")

	# # 							SAC-DM 
	# util.showTreinamentoM([sac_dm_C0_x, sac_dm_C0_y, sac_dm_C0_z], (f"SAC-DM: Arquivo C0 - N{N}"), "C0")
	# util.showTreinamentoM([sac_dm_C2_x, sac_dm_C2_y, sac_dm_C2_z], (f"SAC-DM: Arquivo C2 - N{N}"), "C2")
	# util.showTreinamentoM([sac_dm_C4_x, sac_dm_C4_y, sac_dm_C4_z], (f"SAC-DM: Arquivo C4 - N{N}"), "C4")
	# util.showTreinamentoM([sac_dm_C10_x, sac_dm_C10_y, sac_dm_C10_z], (f"SAC-DM: Arquivo C10 - N{N}"), "C10")
	# util.showTreinamentoM([sac_dm_C20_x, sac_dm_C20_y, sac_dm_C20_z], (f"SAC-DM: Arquivo C20 - N{int(N/4)}"), "C20")

	# # 								Matriz de confusao em arquivo txt e plot
	# util.cleanTxtMatrix(N)
	# util.confusionMatrixPlotAndTxt([sac_am_C0_x, sac_am_C2_x, sac_am_C4_x, sac_am_C10_x, sac_am_C20_x], ["C0", "C2", "C4", "C10", "C20"], "SAC-AM: Eixo X", N)
	# util.confusionMatrixPlotAndTxt([sac_am_C0_y, sac_am_C2_y, sac_am_C4_y, sac_am_C10_y, sac_am_C20_y], ["C0", "C2", "C4", "C10", "C20"], "SAC-AM: Eixo Y", N)
	# util.confusionMatrixPlotAndTxt([sac_am_C0_z, sac_am_C2_z, sac_am_C4_z, sac_am_C10_z, sac_am_C20_z], ["C0", "C2", "C4", "C10", "C20"], "SAC-AM: Eixo Z", N)

	# util.confusionMatrixPlotAndTxt([sac_dm_C0_x, sac_dm_C2_x, sac_dm_C4_x, sac_dm_C10_x, sac_dm_C20_x], ["C0", "C2", "C4", "C10", "C20"], "SAC-DM: Eixo X", N)
	# util.confusionMatrixPlotAndTxt([sac_dm_C0_y, sac_dm_C2_y, sac_dm_C4_y, sac_dm_C10_y, sac_dm_C20_y], ["C0", "C2", "C4", "C10", "C20"], "SAC-DM: Eixo Y", N)
	# util.confusionMatrixPlotAndTxt([sac_dm_C0_z, sac_dm_C2_z, sac_dm_C4_z, sac_dm_C10_z, sac_dm_C20_z], ["C0", "C2", "C4", "C10", "C20"], "SAC-DM: Eixo Z", N)

	# # 								Comparação de janelas Slinding vs Jumping
	# util.windowsPlot([sac_am_C0_x, sac_am_C2_x, sac_am_C4_x, sac_am_C10_x, sac_am_C20_x], ["C0", "C2", "C4", "C10", "C20"], "SAC-AM: Eixo X", int(sys.argv[2]), N)
	# util.windowsPlot([sac_am_C0_y, sac_am_C2_y, sac_am_C4_y, sac_am_C10_y, sac_am_C20_y], ["C0", "C2", "C4", "C10", "C20"], "SAC-AM: Eixo Y", int(sys.argv[2]), N)
	# util.windowsPlot([sac_am_C0_z, sac_am_C2_z, sac_am_C4_z, sac_am_C10_z, sac_am_C20_z], ["C0", "C2", "C4", "C10", "C20"], "SAC-AM: Eixo Z", int(sys.argv[2]), N)

	# util.windowsPlot([sac_dm_C0_x, sac_dm_C2_x, sac_dm_C4_x, sac_dm_C10_x, sac_dm_C20_x], ["C0", "C2", "C4", "C10", "C20"], "SAC-DM: Eixo X", int(sys.argv[2]), N)
	# util.windowsPlot([sac_dm_C0_y, sac_dm_C2_y, sac_dm_C4_y, sac_dm_C10_y, sac_dm_C20_y], ["C0", "C2", "C4", "C10", "C20"], "SAC-DM: Eixo Y", int(sys.argv[2]), N)
	# util.windowsPlot([sac_dm_C0_z, sac_dm_C2_z, sac_dm_C4_z, sac_dm_C10_z, sac_dm_C20_z], ["C0", "C2", "C4", "C10", "C20"], "SAC-DM: Eixo Z", int(sys.argv[2]), N)

	# #									Taxa de aquisição das amostras por segundo com plotagem
	# util.taxa_de_aquisicao(C0_t, "C0")
	# util.taxa_de_aquisicao(C2_t, "C2")
	# util.taxa_de_aquisicao(C4_t, "C4")
	# util.taxa_de_aquisicao(C10_t, "C10")
	# util.taxa_de_aquisicao(C20_t, "C20")

	plt.show()
	return 0

#********* Main ********

plot_SAC_AM_DM_drone_signals()
# plot_SAC_AM_DM_motor_signals()