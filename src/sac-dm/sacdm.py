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

def plot_SAC_AM_DM(file_paths, file_columns, file_tags):

	N = int(sys.argv[1])
	files = []
	file_axes = []
	sac_am_by_files = []
	sac_dm_by_files = []
	sac_am_by_axes = []
	sac_dm_by_axes = []
	auxAxes = ["Eixo X", "Eixo Y", "Eixo Z"]
	
	for i in range(len(file_paths)): # Abrindo arquivos
		files_aux = np.genfromtxt( file_paths[i], delimiter=';',names= file_columns)
		files.append(files_aux)

	for i in range(len(file_paths)):
		file_list = []
		sac_am_list = []
		sac_dm_list = []
		for j in range(5):	# Extraindo eixos
			file_axes_aux = files[i][file_columns[j]].reshape(-1)
			file_list.append(file_axes_aux)

			if( j < 3): # Obtendo SACs
				sac_am_aux = sac_am(file_axes_aux, N)
				sac_dm_aux = sac_dm(file_axes_aux, N)
				sac_am_aux.pop()
				sac_dm_aux.pop()
				sac_am_list.append(sac_am_aux)
				sac_dm_list.append(sac_dm_aux)
		
		file_axes.append(file_list)
		sac_am_by_files.append(sac_am_list)
		sac_dm_by_files.append(sac_dm_list)

	for i in range(3): # Qtd de eixos
		sac_am_aux = []
		sac_dm_aux = []
		for j in range(len(file_paths)): # Qtd de arquivos
			sac_am_aux.append(sac_am_by_files[j][i])
			sac_dm_aux.append(sac_dm_by_files[j][i])

		sac_am_by_axes.append(sac_am_aux)
		sac_dm_by_axes.append(sac_dm_aux)

	
	# #					Plotando teste e treino do mesmo arquivo

	# util.showTreinamentoM(sac_am_by_files[0], (f"SAC-AM: {file_tags[0]}"), file_tags[0])
	# util.showTreinamentoM(sac_dm_by_files[0], (f"SAC-DM: {file_tags[0]}"), file_tags[0])

	# # Plotando na mesma figura 3 graficos( 1 para cada eixo ), contendo o treinamento e o teste feitos em arquivos diferentes
	
	# #								SAC-AM
	# util.showSAC_figUnicaComTreinoM( sac_am_by_files, (f"SAC-AM: Treinamento Metade - N{N}"), file_tags)

	# #								SAC-DM
	# util.showSAC_figUnicaComTreinoM( sac_dm_by_files, (f"SAC-AM: Treinamento Metade - N{N}"), file_tags)
	
	# # Plotando graficos de forma individual

	# for i in range(3):
	# 	util.showSacUnicoEixo(sac_am_by_axes[i], (f"SAC-AM: {auxAxes[i]}"), file_tags)
	# 	util.showSacUnicoEixo(sac_dm_by_axes[i], (f"SAC-DM: {auxAxes[i]}"), file_tags)

	# # 								Matriz de confusao em um arquivo txt e Plot

	# util.cleanTxtMatrix(N)
	# for i in range(3):
	# 	util.confusionMatrixPlotAndTxt(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), N)
	# 	util.confusionMatrixPlotAndTxt(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), N)

	# # 								Janela Deslizante em um arquivo txt
	
	# util.cleanTxtSliding(N, int(sys.argv[2]))
	# for i in range(3):
	# 	util.slidingWindowInTxt(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N)
	# 	util.slidingWindowInTxt(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N)

	# # 								Janela Pulante em um arquivo txt
	# util.cleanTxtJumping(N, int(sys.argv[2]))
	# for i in range(3):
	# 	util.jumpingWindowInTxt(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N)
	# 	util.jumpingWindowInTxt(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N)
	
	# # 								Comparação de janelas Slinding vs Jumping
	
	# for i in range(3):
		# util.windowsPlot(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N)
		# util.windowsPlot(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N)
	
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

file_paths = [  "../../files/drone_signals/accel_80_F0.csv",
				"../../files/drone_signals/accel_80_F6.csv",
				"../../files/drone_signals/accel_80_F14.csv",
				"../../files/drone_signals/accel_80_F22.csv" ]

file_columns = ['x','y','z','s','t']

file_tags = [ "F0", "F6", "F14", "F22"]

plot_SAC_AM_DM(file_paths, file_columns, file_tags)

# plot_SAC_AM_DM_motor_signals()