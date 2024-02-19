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
		# s = sum(v)
		s = np.mean(v)
		sacdm[k] = 1.0*s/N
		inicio = fim
		fim = fim + N

		
	
	return sacdm

def plot_trainning_test(sac_am_by_files, sac_dm_by_files, file_tags, file=0):
	#Plotting test and training from the same file
	util.plotTraining(sac_am_by_files[file], (f"SAC-AM: {file_tags[file]}"), file_tags[file])
	util.plotTraining(sac_dm_by_files[file], (f"SAC-DM: {file_tags[file]}"), file_tags[file])

def plot_sacs_one_figure(sac_am_by_files, sac_dm_by_files, file_tags, N):
	#Plotting 3 graphs on the same figure (1 for each axis), including training and testing done on different files.
	#SAC-AM
	util.plotSACsInOneFigureWithTraining( sac_am_by_files, (f"SAC-AM: N{N}"), file_tags)
	#SAC-DM
	util.plotSACsInOneFigureWithTraining( sac_dm_by_files, (f"SAC-DM: Half training/testing - N{N}"), file_tags)

def plot_sacs_by_axes(sac_am_by_files, sac_dm_by_files, file_tags):
	#Plotting graphs individually
	auxAxes = ["x-axis", "y-axis", "z-axis"]
	for i in range(3):
		util.plotSACsAxis(sac_am_by_axes[i], (f"SAC-AM: {auxAxes[i]}"), file_tags)
	for i in range(3):
		util.plotSACsAxis(sac_dm_by_axes[i], (f"SAC-DM: {auxAxes[i]}"), file_tags)

def plot_confusion_matrix_save_txt(sac_am_by_axes, sac_dm_by_axes, file_tags, N, save):
	#Confusion matrix in a txt file
	auxAxes = ["x-axis", "y-axis", "z-axis"]
	if(save == True):
		util.cleanTxtMatrix(N)
		for i in range(3):
			util.confusionMatrix(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), N, save)
		for i in range(3):
			util.confusionMatrix(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), N, save)
	else:
		for i in range(3):
			util.confusionMatrix(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), N, save)
		for i in range(3):
			util.confusionMatrix(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), N, save)


def slinding_window_in_txt(sac_am_by_axes, sac_dm_by_axes, file_tags, N, save=False):
	#Sliding window in a txt file
	auxAxes = ["x-axis", "y-axis", "z-axis"]
	if( save == True):
		util.cleanTxtSliding(N, int(sys.argv[2]))
		for i in range(3):
			util.slidingWindow(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N, save)
		for i in range(3):
			util.slidingWindow(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N, save)
	else:
		for i in range(3):
			util.slidingWindow(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N, save)
		for i in range(3):
			util.slidingWindow(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N, save)

def jumping_window_in_txt(sac_am_by_axes, sac_dm_by_axes, file_tags, N, save=False):
	#Jumping window in a txt file
	auxAxes = ["x-axis", "y-axis", "z-axis"]
	if(save == True):
		util.cleanTxtJumping(N, int(sys.argv[2]))
		for i in range(3):
			util.jumpingWindow(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N, save)
		for i in range(3):
			util.jumpingWindow(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N, save)
	else:
		for i in range(3):
			util.jumpingWindow(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N, save)
		for i in range(3):
			util.jumpingWindow(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N, save)

def plot_compare_windows(sac_am_by_axes, sac_dm_by_axes, file_tags, N):
	#Comparison of Windows: Sliding vs Jumping
	auxAxes = ["x-axis", "y-axis", "z-axis"]
	for i in range(3):
		util.plotWindowsComparation(sac_am_by_axes[i], file_tags, (f"SAC-AM: {auxAxes[i]}"), int(sys.argv[2]), N)
	for i in range(3):
		util.plotWindowsComparation(sac_dm_by_axes[i], file_tags, (f"SAC-DM: {auxAxes[i]}"), int(sys.argv[2]), N)
	
def plot_heat_all_axes_windows(sac_am_by_files, sac_dm_by_files, file_tags, N, accelerometer):
	#Heatmap of all axes window
	util.plot_heat_jumpingWindowAllAxes(sac_am_by_files, file_tags, (f"Accelerometer {accelerometer}: "), int(sys.argv[2]), N)
	util.plot_heat_slidingWindowAllAxes(sac_am_by_files, file_tags, (f"Accelerometer {accelerometer}: "), int(sys.argv[2]), N)

def plot_heat_axis_window(sac_am_by_axes, sac_dm_by_axes, file_tags, N, accelerometer):
	#Heatmaps of one axis window
	util.plot_heat_jumpingWindowAxis(sac_am_by_axes, file_tags, (f"Accelerometer {accelerometer}: "), int(sys.argv[2]), N)
	util.plot_heat_slidingWindowAxis(sac_am_by_axes, file_tags, (f"Accelerometer {accelerometer}: "), int(sys.argv[2]), N)


def relocateN(files, file_columns, file_paths, N):

	sac_am_by_files = []
	sac_dm_by_files = []
	sac_am_by_axes = []
	sac_dm_by_axes = []

	for i in range(len(file_paths)):
		file_list = []
		sac_am_list = []
		sac_dm_list = []
		#Extracting axes
		for j in range(len(file_columns)):
			file_axes_aux = files[i][file_columns[j]].reshape(-1)
			file_list.append(file_axes_aux)

			#Getting SACs
			if( j < 3):
				sac_am_aux = sac_am(file_axes_aux, N)
				sac_am_aux.pop()
				sac_am_list.append(sac_am_aux)

		sac_am_by_files.append(sac_am_list)

	#Number of axes
	for i in range(3): 
		sac_am_aux = []

		#Number of files
		for j in range(len(file_paths)): 
			sac_am_aux.append(sac_am_by_files[j][i])

		sac_am_by_axes.append(sac_am_aux)

	return sac_am_by_files

def search_optimal(files, file_columns, file_paths, file_tags):

	jumping_list_result_c = []
	sliding_list_result_c = []
	jumping_list_result_nc = []
	sliding_list_result_nc = []
	title = ""
	stop = 0
	for k in range(500,6000,100):
		window_range = [3,5]
		for j in range(len(window_range)):
			print(f"Jumping: Calculating N:{k} ws:{window_range[j]}")
			dataset = relocateN(files, file_columns,file_paths, k)
			outputMatrixJumping = util.jumpingWindowAllAxes(dataset, file_tags, title, window_range[j], k)
			outputMatrixJumping = outputMatrixJumping / 100
			jumping_result = np.zeros(len(file_tags) + 3)


			jump_axes_percent = 0
			for i in range(len(file_tags)):
				jumping_result[i] = round(outputMatrixJumping[i][i],2)
				jump_axes_percent += jumping_result[i]

			jumping_result[len(file_tags)] = k
			jumping_result[len(file_tags) + 1] = window_range[j]
			jumping_result[len(file_tags) + 2] = jump_axes_percent

			if(jump_axes_percent >= 4):
				jumping_list_result_c.append(jumping_result)
			else:
				jumping_list_result_nc.append(jumping_result)

			if(jump_axes_percent == 4):
				stop += 1
			
		if(stop == 2):
			break

	jumping_list_result_nc.sort(key=lambda x: x[6])

	stop = 0
	for k in range(500,6000,100):
		window_range = [3,5]
		for j in range(len(window_range)):
			print(f"Sliding: Calculating N:{k} ws:{window_range[j]}")
			dataset = relocateN(files, file_columns,file_paths, k)
			outputMatrixSliding = util.slidingWindowAllAxes(dataset, file_tags, title, window_range[j], k)
			outputMatrixSliding = outputMatrixSliding / 100
			sliding_result = np.zeros(len(file_tags) + 3)

			sli_axes_percent = 0
			for i in range(len(file_tags)):

				sliding_result[i] = round(outputMatrixSliding[i][i],2)
				sli_axes_percent += sliding_result[i]

			sliding_result[len(file_tags)] = k
			sliding_result[len(file_tags) + 1] = window_range[j]
			sliding_result[len(file_tags) + 2] = sli_axes_percent
			
			if(sli_axes_percent >= 4):
				sliding_list_result_c.append(sliding_result)
			else:
				sliding_list_result_nc.append(sliding_result)

			if(sli_axes_percent == 4):
				stop += 1
			
		if(stop == 2):
			break
	
	sliding_list_result_nc.sort(key=lambda x: x[6])

	print("\n\nJumping window \n")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<12}", end="")
	print(f"{'N':<10}", end="")
	print(f"{'window_size':<12}",end="")
	print(f"{'soma diagonal':<12}",)
	
	if(len(jumping_list_result_c) > 0):
		for i in range(len(jumping_list_result_c)):
			for j in range(len(jumping_list_result_c[i])):
				result = jumping_list_result_c[i]
				print(f"{result[j]:<12}", end="")
			print("")
	else:
		for i in range((len(jumping_list_result_nc) - 1), ((len(jumping_list_result_nc) - 1)) - 2 , -1):
			for j in range(len(jumping_list_result_nc[i])):
				result = jumping_list_result_nc[i]
				print(f"{result[j]:<12}", end="")
			print("")

	print("\n\nSliding window \n")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<12}", end="")
	print(f"{'N':<10}", end="")
	print(f"{'window_size':<12}",end="")
	print(f"{'soma diagonal':<12}",)

	if(len(sliding_list_result_c) > 0):
		for i in range(len(sliding_list_result_c)):
			for j in range(len(sliding_list_result_c[i])):
				result = sliding_list_result_c[i]
				print(f"{result[j]:<12}", end="")
			print("")
	else:
		for i in range((len(sliding_list_result_nc) - 1), ((len(sliding_list_result_nc) - 1)) - 2 , -1):
			for j in range(len(sliding_list_result_nc[i])):
				result = sliding_list_result_nc[i]
				print(f"{result[j]:<12}", end="")
			print("")

def plot_SAC_AM_DM(sac_am_by_axes, sac_am_by_files, sac_dm_by_axes, sac_dm_by_files, file_tags, N):

	# plot_trainning_test(sac_am_by_files, sac_am_by_files, file_tags, file = 0)

	plot_sacs_one_figure(sac_am_by_files, sac_dm_by_files, file_tags, N)

	# plot_sacs_by_axes(sac_am_by_files, sac_dm_by_files, file_tags)

	# plot_confusion_matrix_save_txt(sac_am_by_axes, sac_dm_by_axes, file_tags, N, save=True)

	# slinding_window_in_txt(sac_am_by_axes, sac_dm_by_axes, file_tags, N, save=True)

	# jumping_window_in_txt(sac_am_by_axes, sac_dm_by_axes, file_tags, N, save=True)

	# plot_compare_windows(sac_am_by_axes, sac_dm_by_axes, file_tags, N)

	# plot_heat_all_axes_windows(sac_am_by_files, sac_dm_by_files, file_tags, N, accelerometer=1)

	# plot_heat_axis_window(sac_am_by_axes, sac_dm_by_axes, file_tags, N, accelerometer=1)
	
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

file_paths = [     "../../files/hexacopter_signals/nominal_flight/NFlt01n1.csv",
			"../../files/hexacopter_signals/failure_condition_1/FC1Flt01n1.csv",
			"../../files/hexacopter_signals/failure_condition_2/FC2Flt01n1.csv",
			"../../files/hexacopter_signals/failure_condition_3/FC3Flt01n1.csv" ]

# file_paths = [     "../../files/hexacopter_signals/nominal_flight/NFlt01n2.csv",
# 			"../../files/hexacopter_signals/failure_condition_1/FC1Flt01n2.csv",
# 			"../../files/hexacopter_signals/failure_condition_2/FC2Flt01n2.csv",
# 			"../../files/hexacopter_signals/failure_condition_3/FC3Flt01n2.csv" ]

# file_paths = [     "../../files/hexacopter_signals/nominal_flight/NFlt01n3.csv",
# 			"../../files/hexacopter_signals/failure_condition_1/FC1Flt01n3.csv",
# 			"../../files/hexacopter_signals/failure_condition_2/FC2Flt01n3.csv",
# 			"../../files/hexacopter_signals/failure_condition_3/FC3Flt01n3.csv" ]


file_tags = [ "Nflt","FC1", "FC2", "FC3"]

file_columns = ['x','y','z','t']

N = int(sys.argv[1])
files = []
file_axes = []
sac_am_by_files = []
sac_dm_by_files = []
sac_am_by_axes = []
sac_dm_by_axes = []

#Opening files
for i in range(len(file_paths)):
	files_aux = np.genfromtxt( file_paths[i], delimiter=';',names= file_columns)
	files.append(files_aux)

for i in range(len(file_paths)):
	file_list = []
	sac_am_list = []
	sac_dm_list = []
	#Extracting axes
	for j in range(len(file_columns)):
		file_axes_aux = files[i][file_columns[j]].reshape(-1)
		file_list.append(file_axes_aux)

		#Getting SACs
		if( j < 3):
			sac_am_aux = sac_am(file_axes_aux, N)
			sac_dm_aux = sac_dm(file_axes_aux, N)
			sac_am_aux.pop()
			sac_dm_aux.pop()
			sac_am_list.append(sac_am_aux)
			sac_dm_list.append(sac_dm_aux)
	
	file_axes.append(file_list)
	sac_am_by_files.append(sac_am_list)
	sac_dm_by_files.append(sac_dm_list)

#Number of axes
for i in range(3): 
	sac_am_aux = []
	sac_dm_aux = []
	#Number of files
	for j in range(len(file_paths)): 
		sac_am_aux.append(sac_am_by_files[j][i])
		sac_dm_aux.append(sac_dm_by_files[j][i])

	sac_am_by_axes.append(sac_am_aux)
	sac_dm_by_axes.append(sac_dm_aux)


plot_SAC_AM_DM(sac_am_by_axes, sac_am_by_files, sac_dm_by_axes, sac_dm_by_files, file_tags, N)

# search_optimal(files,file_columns, file_paths, file_tags)
# plot_SAC_AM_DM_motor_signals()