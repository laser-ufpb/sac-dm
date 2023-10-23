import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import matplotlib.colors as mcolors
import time

def average_sac(dataset, start, end):

	average = np.average(dataset[start:end])

	return average

def deviation_sac(dataset, start, end):

	standard_deviation = np.std(dataset[start:end])

	return standard_deviation

def sampling_sac(dataset, start, end):

	return dataset[start:end]

def cleanTxtSliding(N, window_size):
	filename = (f"SlidingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	file1.close()

def cleanTxtJumping(N, window_size):
	filename = (f"JumpingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	file1.close()

def cleanTxtMatrix(N):
	filename = (f"confusionMatrixHalfTrainingN{N}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	file1.close()

def get_change_t(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current)  / previous) * 100.0
    except ZeroDivisionError:
        return 0

def windowCompare( window, average, deviation, file_tags ):

	conclusion = np.full((len(window)), -1)

	#Axes
	for i in range(len(window)):
		#Files
		for j in range(len(file_tags)):

			result = np.logical_and(window[i] >= (average[i][j] - deviation[i][j]), window[i] <= (average[i][j] + deviation[i][j]))
			# print(f"Result: {result} Window: {window[i]} LimitS: {(average[i][j] - deviation[i][j])} LimitI: { (average[i][j] + deviation[i][j])}")
			auxConclusion = np.where(result == True)[0]

			#checks if the entire window is classified with the same tag
			if(len(auxConclusion) == len(file_tags)):
				conclusion[i] = j
				break
			
			#checks whether the majority of points contained in the window are classified with the same tag
			if(len(auxConclusion) >= (len(window[i])- len(auxConclusion))):
				conclusion[i] = j
				break
			
			#checks if only one of the points contained in the window is classified as failure
			if(len(auxConclusion) == 1 and auxConclusion[0] != 1):
				conclusion[i] = j
				break

			conclusion[i] = (len(file_tags))

	#modificar retorno da função: trocar majoritaria
	# identificação
	# 	- Sem falha = Se os 3 eixos estão na condiçao normal
	#	- Falha = Se pelo menos um eixo está fora da condição normal
	#Classificação -> Verificar em qual faixa do erro que a janela está
	#	- se eixos != de normal estão na mesma faixa:
	# 		- Erro dessa faixa
	# 	- se eixos != de normal estão em faixas de erros diferentes: 
	#		- Inconclusivo 

	#check if the 3 axes are in the same condition
	for i in range(len(file_tags)):
		auxConclusion = np.where(conclusion == i)[0]
		if(len(auxConclusion) == len(conclusion)):
			print(f"Eixos com mesma falha: conclusao: {conclusion}")
			return i
	
	auxConclusion = np.where(conclusion > 0)[0]

	#check if at least one axis is outside the normal condition
	#only one axis outside the normal condition
	if(len(auxConclusion) == 1):
		print(f"Apenas um eixo com falha:  conclusao: {conclusion}")
		return auxConclusion
	
	#more than one axis outside the normal condition but with the same fault condition
	if(len(auxConclusion) == 2 and conclusion[auxConclusion[0]] == conclusion[auxConclusion[1]]):
		print(f"Dois eixos com mesma falha e outro sem:  conclusao: {conclusion}")
		return conclusion[auxConclusion[0]]
	else:
		#different failure conditions
		print(f"Inconclusivo:  conclusao: {conclusion}")
		return len(file_tags)

def saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header):
	
	matrix_file = open(filename, 'a+')
	matrix_file.write(f"{title} - N{N}\n\n")
	
	for i in range(len(outputMatrix)):
		matrix_file.write((file_tags[i] + ":" + " Average - " + str(round(average[i], 4)) + "\n"))
		matrix_file.write((file_tags[i] + ":" + " Standard deviation - " + str(round(deviation[i], 4)) + "\n"))
		matrix_file.write((file_tags[i] + ":" + " Lower limit - " + str(round(average[i] - deviation[i], 4)) + " | " + "Upper limit - " + str(round(average[i] + deviation[i], 4)) +"\n\n"))

	matrix_file.write(header)
	matrix_file.write((f"{'File':<10}"))
	for i in range(len(file_tags)):
		matrix_file.write(f"{file_tags[i]:<10}")
	matrix_file.write(f"{'Inconclusive':<10}\n")

	for i in range(len(outputMatrix)):
		matrix_file.write(f"{file_tags[i]:<10}")
		for j in range(len(outputMatrix[i])):
			aux = (f"{outputMatrix[i][j]}%")
			matrix_file.write(f"{aux:<10}")
		matrix_file.write("\n\n")

	matrix_file.close()


def halfTraining(dataset, title, fig, ax, file_tag):
	
	plt.ylabel(title) 
	plt.xlabel('Time (ms)')
	
	half_dataset = sampling_sac(dataset, 0, round(len(dataset)/2) + 1)
	colors = list(mcolors.CSS4_COLORS) 

	average_dataset = average_sac(half_dataset, 0, len(half_dataset))
	deviation_dataset = deviation_sac(half_dataset, 0, len(half_dataset))

	aux_dev = np.zeros(len(half_dataset))
	aux_dev[round(len(half_dataset)/2)] = deviation_dataset

	x = np.arange(len(half_dataset))
	y = np.zeros(len(half_dataset))
	y = np.full_like(y, average_dataset)

	ax.plot(x,y,color=colors[10], label = (f"Average of the first half of the SAC {file_tag}"))

	for j in range(len(half_dataset)):

		if(aux_dev[j] != 0):			
			ax.errorbar(j,average_dataset,yerr = aux_dev[j], color = colors[20],marker='s', capsize=2, markersize=4, linewidth=1, linestyle='--')

	ax.fill_between(x, average_dataset - deviation_dataset, average_dataset + deviation_dataset, alpha = 0.2, label = (f"Standard Deviation of the first half of the File {file_tag}"))

def testing(dataset, title, fig, ax, color):

	colors = list(mcolors.CSS4_COLORS) 
	ax.plot(dataset,color=colors[color], label = title)
	ax.set_xlim(left= -1)
	
def plotTraining(dataset, title, file_tag):	
	
	fig, axs = plt.subplots(3)
	fig.suptitle(title)

	#Creating subgraph titles
	auxT = [("x-axis"), ("y-axis"), ("z-axis")]
	
	for i in range(len(dataset)):

		halfTraining(dataset[i], title, fig, axs[i],file_tag)
		testing_data = sampling_sac(dataset[i], round(len(dataset[i])/2), len(dataset[i]) )
		testing(testing_data, (f"Second half of the file {file_tag}"), fig, axs[i], (11+i))
		axs[i].set_xlim(left = -1)
		axs[i].set(ylabel = auxT[i])
		# axs[i].legend(loc = 'upper right')

def plotSACsInOneFigureWithTraining(dataset, title, file_tag):

	#Creating base graphics (Training)
	fig, (axs) = plt.subplots(3)

	fig.suptitle(title)
	aux = title.split(':',1)

	#Plot the axes on base graphs (Test)
	#Axes
	for i in range(len(dataset[0])):
		halfTraining(dataset[0][i], "", fig, axs[i], file_tag[0])
		
		#Files
		for j in range(0 ,len(dataset)):
			testing_data = sampling_sac(dataset[j][i], round(len(dataset[j][i])/2), len(dataset[j][i]) )
			testing(testing_data, (f"Second half of the file: {file_tag[j]}"), fig, axs[i], (11+j))
		
		axs[i].set_xlim(-1, round(len(dataset[0][i]) * 0.69))
		axs[i].legend(loc='lower right')
		
	axs[0].set(ylabel = (aux[0] + ": x-axis"))
	axs[1].set(ylabel = (aux[0] + ": y-axis"))
	axs[2].set(ylabel = (aux[0] + ": z-axis"))	

def plotSACsAxis(dataset, title, file_tag):

	#Creating base graphics (Training)
	fig, ax = plt.subplots()
	ax.set_title(title)

	#Plot the axes on base graphs (Test)
	for i in range(len(dataset)):
		testing(dataset[i], (f"File: {file_tag[i]}"), fig, ax, (10+i))
	
	ax.legend(loc='lower right')

def confusionMatrix(dataset, file_tags, title, N, save):

	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	outputMatrix = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))

	#Files with the same axis
	for i in range(len(dataset)):
		#Array of SACs
		for j in range(round(len(dataset[i])/2),len(dataset[i])): 
			testing_data = dataset[i][j]
			if (testing_data >= average[0] - deviation[0] and testing_data <= average[0] + deviation[0]):
				outputMatrix[i][0] += 1
				continue

			elif(testing_data >= average[1] - deviation[1] and testing_data <= average[1] + deviation[1]):
				outputMatrix[i][1] += 1
				continue

			elif(testing_data >= average[2] - deviation[2] and testing_data <= average[2] + deviation[2]):
				outputMatrix[i][2] += 1
				continue

			elif(testing_data >= average[3] - deviation[3] and testing_data <= average[3] + deviation[3]):
				outputMatrix[i][3] += 1
				continue
			
			else:
				outputMatrix[i][4] += 1

	for i in range(len(dataset)):
		#Converts matrix values to percentage values.
		outputMatrix[i] = np.round((outputMatrix[i] / (len(dataset[i])/2)) * 100, decimals=1)  

	print(f"\n\t\t{title}\n")

	print(f"{'File':<10}", end="")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<10}", end="")

	print(f"{'Inconclusive':<10}")

	for i in range(len(outputMatrix)):
		#Adds '%' to array values.
		values = [f"{outputMatrix[i][j]}%" for j in range(len(outputMatrix[i]))] 
		print(f"{file_tags[i]:<10}{values[0]:<10}{values[1]:<10}{values[2]:<10}{values[3]:<10}{values[4]:<10}")

	if(save == True):
		filename = (f"confusionMatrixHalfTrainingN{N}.txt")
		header = (f"Confusion matrix[%] \n\n")
		saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)

def slidingWindow(dataset, file_tags, title, window_size, N, save):


	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	count_window = np.zeros((len(dataset)))
	outputMatrix = np.zeros((len(dataset),len(dataset)+1))

	print((title + "\n\n"))
	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))
		

	#Files with the same axis
	for i in range(len(dataset)):
		#Array of SACs
		for j in range( round(len(dataset[i])/2), (len(dataset[i]) - window_size + 1) ):
			window = dataset[i][j:j+window_size]
			conclusion = np.zeros((len(file_tags) + 1))
			
			for k in range(len(window)):
				if (window[k] >= average[0] - deviation[0] and window[k] <= average[0] + deviation[0]):
					conclusion[0] += 1
					continue

				elif(window[k] >= average[1] - deviation[1] and window[k] <= average[1] + deviation[1]):
					conclusion[1] += 1
					continue

				elif(window[k] >= average[2] - deviation[2] and window[k] <= average[2] + deviation[2]):
					conclusion[2] += 1
					continue

				# elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
				# 	conclusion[3] += 1
				# 	continue
				
				else:
					conclusion[3] += 1
			
			if(j == (len(dataset[i]) - window_size)):
				outputMatrix[i][np.argmax(conclusion)] += 1 * window_size
				count_window[i] += 1 * window_size
			else:
				outputMatrix[i][np.argmax(conclusion)] += 1
				count_window[i] += 1

	print(f"Confusion matrix[%] - Sliding window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
	print((f"{'File':<10}"), end="")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<10}", end="")
	print(f"{'Inconclusive':<10}")

	for i in range(len(outputMatrix)):
		print(f"{file_tags[i]:<10}", end="")
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)
			aux = (f"{outputMatrix[i][j]}%")
			print(f"{aux:<10}", end="")
		print("\n")

	if(save == True):
		filename = (f"SlidingWindowN{N}Size{window_size}.txt")
		header = (f"Confusion matrix[%] - Sliding window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
		saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)

def jumpingWindow(dataset, file_tags, title, window_size, N, save):
	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	count_window = np.zeros((len(dataset)))
	outputMatrix = np.zeros((len(dataset),len(dataset)+1))

	print((title + "\n\n"))
	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))


	#Files with the same axis
	for i in range(len(dataset)):
		#Array of SACs
		for j in range( round(len(dataset[i])/2), (len(dataset[i])), window_size):
			conclusion = np.zeros((len(file_tags) + 1))
			count_window[i] += 1
			if (j + window_size <= len(dataset[i])):
				window = dataset[i][j:j+window_size]

				for k in range(len(window)):
					if (window[k] >= average[0] - deviation[0] and window[k] <= average[0] + deviation[0]):
						conclusion[0] += 1
						continue

					elif(window[k] >= average[1] - deviation[1] and window[k] <= average[1] + deviation[1]):
						conclusion[1] += 1
						continue

					elif(window[k] >= average[2] - deviation[2] and window[k] <= average[2] + deviation[2]):
						conclusion[2] += 1
						continue

					elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
						conclusion[3] += 1
						continue
					
					else:
						conclusion[4] += 1

			else:
				window = dataset[i][j:]

				for k in range(len(window)):
					if (window[k] >= average[0] - deviation[0] and window[k] <= average[0] + deviation[0]):
						conclusion[0] += 1
						continue

					elif(window[k] >= average[1] - deviation[1] and window[k] <= average[1] + deviation[1]):
						conclusion[1] += 1
						continue

					elif(window[k] >= average[2] - deviation[2] and window[k] <= average[2] + deviation[2]):
						conclusion[2] += 1
						continue

					elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
						conclusion[3] += 1
						continue
					
					else:
						conclusion[4] += 1
			
			outputMatrix[i][np.argmax(conclusion)] += 1
				
	print(f"Confusion matrix[%] - Jumping Window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
	print((f"{'File':<10}"), end="")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<10}", end="")
	print(f"{'Inconclusive':<10}")

	for i in range(len(outputMatrix)):
		print(f"{file_tags[i]:<10}", end="")
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)
			aux = (f"{outputMatrix[i][j]}%")
			print(f"{aux:<10}", end="")
		print("\n")

	if(save == True):
		filename = (f"JumpingWindowN{N}Size{window_size}.txt")
		header = (f"Confusion matrix[%] - Jumping Window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
		saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)

def plotWindowsComparation(dataset, file_tags, title, window_size, N):

	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	count_window_jumping = np.zeros((len(dataset)))
	count_window_sliding = np.zeros((len(dataset)))
	jumpingMatrixOutput = np.zeros((len(dataset),len(dataset)+1))
	slidingMatrixOutput = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))

	#Files with the same axis
	for i in range(len(dataset)):
		#Array of SACs
		for j in range( round(len(dataset[i])/2), (len(dataset[i]) - window_size + 1) ):
			window = dataset[i][j:j+window_size]
			conclusion = np.zeros((len(file_tags) + 1))
			
			for k in range(len(window)):
				if (window[k] >= average[0] - deviation[0] and window[k] <= average[0] + deviation[0]):
					conclusion[0] += 1
					continue

				elif(window[k] >= average[1] - deviation[1] and window[k] <= average[1] + deviation[1]):
					conclusion[1] += 1
					continue

				elif(window[k] >= average[2] - deviation[2] and window[k] <= average[2] + deviation[2]):
					conclusion[2] += 1
					continue

				# elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
				# 	conclusion[3] += 1
				# 	continue
				
				else:
					conclusion[3] += 1
			
			if(j == (len(dataset[i]) - window_size)):
				slidingMatrixOutput[i][np.argmax(conclusion)] += 1 * window_size
				count_window_sliding[i] += 1 * window_size
			else:
				slidingMatrixOutput[i][np.argmax(conclusion)] += 1
				count_window_sliding[i] += 1

	#Files with the same axis
	for i in range(len(dataset)):
		#Array of SACs
		for j in range( round(len(dataset[0])/2), (len(dataset[i])), window_size):
			conclusion = np.zeros((len(file_tags) + 1))
			count_window_jumping[i] += 1
			if (j + window_size <= len(dataset[i])):
				window = dataset[i][j:j+window_size]

				for k in range(len(window)):
					if (window[k] >= average[0] - deviation[0] and window[k] <= average[0] + deviation[0]):
						conclusion[0] += 1
						continue

					elif(window[k] >= average[1] - deviation[1] and window[k] <= average[1] + deviation[1]):
						conclusion[1] += 1
						continue

					elif(window[k] >= average[2] - deviation[2] and window[k] <= average[2] + deviation[2]):
						conclusion[2] += 1
						continue

					# elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
					# 	conclusion[3] += 1
					# 	continue
					
					else:
						conclusion[3] += 1

			else:
				window = dataset[i][j:]

				for k in range(len(window)):
					if (window[k] >= average[0] - deviation[0] and window[k] <= average[0] + deviation[0]):
						conclusion[0] += 1
						continue

					elif(window[k] >= average[1] - deviation[1] and window[k] <= average[1] + deviation[1]):
						conclusion[1] += 1
						continue

					elif(window[k] >= average[2] - deviation[2] and window[k] <= average[2] + deviation[2]):
						conclusion[2] += 1
						continue

					# elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
					# 	conclusion[3] += 1
					# 	continue
					
					else:
						conclusion[3] += 1
			
			jumpingMatrixOutput[i][np.argmax(conclusion)] += 1

	for i in range(len(jumpingMatrixOutput)):
		for j in range(len(jumpingMatrixOutput[i])):
			jumpingMatrixOutput[i][j] = round(get_change_t(jumpingMatrixOutput[i][j],(count_window_jumping[i])),2 )	

	for i in range(len(slidingMatrixOutput)):
		for j in range(len(slidingMatrixOutput[i])):
			slidingMatrixOutput[i][j] = round(get_change_t(slidingMatrixOutput[i][j],count_window_sliding[i]),2)

	fig, ax = plt.subplots(len(dataset), 2)
	fig.suptitle(f"{title} - N{N}WindowSize{window_size}")

	labels = file_tags + ["Inconclusive"]

	for j in range(len(dataset)):

		#Pie chart for slidingMatrixOutput
		non_zero_values_sliding = [value for value in slidingMatrixOutput[j] if value != 0]
		non_zero_labels_sliding = [label for value, label in zip(slidingMatrixOutput[j], labels) if value != 0]
		wedges, texts, autotexts = ax[j][0].pie(non_zero_values_sliding, labels=non_zero_labels_sliding[:len(non_zero_values_sliding)], autopct='%1.1f%%', shadow=True, startangle=90)
		ax[j][0].set_title(f"Sliding window - {file_tags[j]}")
		ax[j][0].legend(wedges, non_zero_labels_sliding[:len(non_zero_values_sliding)], loc = "lower left", bbox_to_anchor=(1, 0, 0.5, 1))

		#Pie chart for jumpingMatrixOutput
		non_zero_values_jumping = [value for value in jumpingMatrixOutput[j] if value != 0]
		non_zero_labels_jumping = [label for value, label in zip(jumpingMatrixOutput[j], labels) if value != 0]
		wedges, texts, autotexts = ax[j][1].pie(non_zero_values_jumping, labels=non_zero_labels_jumping[:len(non_zero_values_jumping)], autopct='%1.1f%%', shadow=True, startangle=90)
		ax[j][1].set_title(f"Jumping window - {file_tags[j]}")
		ax[j][1].legend(wedges, non_zero_labels_jumping[:len(non_zero_values_jumping)], loc = "lower left", bbox_to_anchor=(1, 0, 0.5, 1))

def jumpingWindowAllAxes(dataset, file_tags, title, window_size, N):
	average = []
	deviation = []
	count_window = np.zeros((len(file_tags)))
	outputMatrix = np.zeros((len(file_tags),len(file_tags)+1))

	for i in range(3):
		average_list = []
		deviation_list = []
		for j in range(len(file_tags)):
			average_aux = average_sac(dataset[j][i], 0, round(len(dataset[j][i])/2))
			deviation_aux = deviation_sac(dataset[j][i], 0, round(len(dataset[j][i])/2))
			average_list.append(average_aux)
			deviation_list.append(deviation_aux)
		average.append(average_list)
		deviation.append(deviation_list)

	window = []
	#Getting all windows
	#Files
	for i in range(len(dataset)):
		#Axes
		window_files = []
		auxSAC_x = dataset[i][0]
		auxSAC_y = dataset[i][1]
		auxSAC_z = dataset[i][2]
		#windows SAC'S
		for j in range( round(len(auxSAC_x)/2), (len(auxSAC_x)), window_size):
			if (j + window_size <= len(dataset[i])):
				window_aux_x = auxSAC_x[j:j+window_size]
				window_aux_y = auxSAC_y[j:j+window_size]
				window_aux_z = auxSAC_z[j:j+window_size]
			else:
				window_aux_x = auxSAC_x[j:]
				window_aux_y = auxSAC_y[j:]
				window_aux_z = auxSAC_z[j:]	
			window_files.append([window_aux_x,window_aux_y,window_aux_z])
		
		window.append(window_files)

	#files
	for i in range(len(window)):
		#windows
		for j in range(len(window[i])):
			conclusion = windowCompare(window[i][j], average, deviation, file_tags)
			count_window[i] += 1
			outputMatrix[i][conclusion] += 1

	print(f"Confusion matrix[%] - Jumping window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
	print((f"{'File':<10}"), end="")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<10}", end="")
	print(f"{'Inconclusive':<10}")

	for i in range(len(outputMatrix)):
		print(f"{file_tags[i]:<10}", end="")
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)
			aux = (f"{outputMatrix[i][j]}")
			print(f"{aux:<10}", end="")
		print("\n")

	# filename = (f"SlidingWindowN{N}Size{window_size}AllAxes.txt")
	# header = (f"Confusion matrix[%] - Sliding window[{window_size}] AllAxes - N{N} - Quantity of windows{count_window}\n\n")
	# saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)
	return outputMatrix

def slidingWindowAllAxes(dataset, file_tags, title, window_size, N):
	average = []
	deviation = []
	count_window = np.zeros((len(file_tags)))
	outputMatrix = np.zeros((len(file_tags),len(file_tags)+1))

	for i in range(3):
		average_list = []
		deviation_list = []
		for j in range(len(file_tags)):
			average_aux = average_sac(dataset[j][i], 0, round(len(dataset[j][i])/2))
			deviation_aux = deviation_sac(dataset[j][i], 0, round(len(dataset[j][i])/2))
			average_list.append(average_aux)
			deviation_list.append(deviation_aux)
		average.append(average_list)
		deviation.append(deviation_list)

	window = []
	#Getting all windows
	#Files
	for i in range(len(dataset)):
		#Axes
		window_files = []
		auxSAC_x = dataset[i][0]
		auxSAC_y = dataset[i][1]
		auxSAC_z = dataset[i][2]
		#windows SAC'S
		for j in range( round(len(auxSAC_x)/2), (len(auxSAC_x) - window_size + 1) ):
			window_aux_x = auxSAC_x[j:j+window_size]
			window_aux_y = auxSAC_y[j:j+window_size]
			window_aux_z = auxSAC_z[j:j+window_size]
			window_files.append([window_aux_x,window_aux_y,window_aux_z])
		
		window.append(window_files)

	print(f"Qtd de arquivos: {len(window)} Janelas: {len(window[0])} Qtd de janelas: {len(window[0][0])}")
	#files
	for i in range(len(window)):
		#windows
		for j in range(len(window[i])):
			conclusion = windowCompare(window[i][j], average, deviation, file_tags)
			if(j == (len(window[i]) - 1)):
				outputMatrix[i][conclusion] += 1 * window_size
				count_window[i] += 1 * window_size
			else:
				outputMatrix[i][conclusion] += 1
				count_window[i] += 1

	print(f"Confusion matrix[%] - Sliding window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
	print((f"{'File':<10}"), end="")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<10}", end="")
	print(f"{'Inconclusive':<10}")

	for i in range(len(outputMatrix)):
		print(f"{file_tags[i]:<10}", end="")
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)
			aux = (f"{outputMatrix[i][j]}")
			print(f"{aux:<10}", end="")
		print("\n")

	# filename = (f"SlidingWindowN{N}Size{window_size}AllAxes.txt")
	# header = (f"Confusion matrix[%] - Sliding window[{window_size}] AllAxes - N{N} - Quantity of windows{count_window}\n\n")
	# saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)

	return outputMatrix

def plot_heat_windows(dataset, file_tags, title, window_size, N):

	outputMatrixJumping = jumpingWindowAllAxes(dataset, file_tags, title, window_size, N)
	outputMatrixSliding = slidingWindowAllAxes(dataset, file_tags, title, window_size, N)
	labels = file_tags + ["Inconclusive"]

	outputMatrixJumpingN = (outputMatrixJumping - outputMatrixJumping.min()) / (outputMatrixJumping.max() - outputMatrixJumping.min())
	
	fig, ax = plt.subplots()
	

	im, cbar = heatmap(outputMatrixJumpingN, file_tags, labels, ax=ax, cmap="Blues", cbarlabel="")

	# Loop over data dimensions and create text annotations.
	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixJumpingN[i][j], 2)
			if(percentage > 0.2):
				ax.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax.text(j, i, percentage, ha="center", va="center", color="b")
	titleJump = title + (f"Jumping window[N:{N}, WindowSize:{window_size}]")
	ax.set_title(titleJump)
	ax.set(ylabel = "True label", xlabel =  "Predicted label")
	fig.tight_layout()

	outputMatrixSlidingN = (outputMatrixSliding - outputMatrixSliding.min()) / (outputMatrixSliding.max() - outputMatrixSliding.min())
	
	fig, ax = plt.subplots()
	im, cbar = heatmap(outputMatrixSlidingN, file_tags, labels, ax=ax, cmap="Blues", cbarlabel="")

	# Loop over data dimensions and create text annotations.
	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixSlidingN[i][j], 2)
			if(percentage > 0.2):
				ax.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax.text(j, i, percentage, ha="center", va="center", color="b")
	titleJump = title + (f"Sliding window[N:{N}, WindowSize:{window_size}]")
	ax.set_title(titleJump)
	ax.set(ylabel = "True label", xlabel =  "Predicted label")
	fig.tight_layout()




def acquisition_Rate(dataset, file_tag):
	timestamp_seconds = np.zeros(len(dataset))
	for i in range(len(dataset)):
		aux = time.localtime(dataset[i])
		seconds = (aux.tm_hour * 3600) + (aux.tm_min * 60) + aux.tm_sec
		timestamp_seconds[i] = seconds

	unique_values, counts = np.unique(timestamp_seconds, return_counts=True)
	samples = {}

	for value, counts in zip(unique_values, counts):
		samples[value] = np.full(counts, value)

	# for key, separated_array in samples.items():
	# 	print(f"{key}: {len(separated_array)}")

	keys = (list(samples.keys()))
	keys_int = [int(key) for key in keys]

	samples_plot = []
	samples_average = []
	for i in range(keys_int[0], keys_int[-1]):
		if(i in keys_int):
			samples_plot.append(len(samples[i]))
			if(len(samples[i]) > 250):
				samples_average.append(len(samples[i]))
		else:
			samples_plot.append(0)

	# print(f"Samples sizes: {len(samples_average)} Sum of samples: {sum(samples_average)}")
	acquisition_rate = ( sum(samples_average) / len(samples_average) )
	print(f"File acquisition rate {file_tag}: {round(acquisition_rate, 2)} samples per second")

	fig, ax = plt.subplots()

	ax.set_xlim(-5, len(samples_plot))
	ax.set_xticks(range(0, len(samples_plot), 30))
	ax.set(ylabel = "Samples", xlabel = "Seconds", title = (f"Acquisition rate: File {file_tag} "))
	ax.plot(samples_plot)

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)


    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar