import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import matplotlib.colors as mcolors
import time

from scipy.signal import find_peaks, peak_prominences

def testingInstants( instants, average, deviation, file_tags=np.zeros(1)):
	"""
	This function receives 4 parameters with the objective of classifying instants coming from <function sac_am>, 
	using the average and standard deviation of the corresponding axis.

	:param instants: List that contains instant, which are composed of 3 floating values coming from <function sac_am>
	:param average: List containing the averages that will be used in the test
	:param deviation: List containing the standard deviations that will be used in the test
	:param file_tags: List that has the size of the labels for classification, not necessarily being filled with the labels themselves.
	
	:return: Returns a list of tuples that contain the classification of each instant contained in <param instants>.
		Note: To understand the values contained in the tuples, see the return of <function instantCompare>
	"""

	average = np.array(average)
	deviation = np.array(deviation)
	metrics_shape = average.shape

	if( len(metrics_shape) > 1 and len(file_tags) == 1):
		#If the metrics has more than 1 dimension, then the test has more than 1 reference
		file_tags = np.zeros(metrics_shape[0])

	#If the metrics has more than 1 dimension, then the metrics is organized by axis | average[ quantity of axis ][ quantity of references ][ value ]
	average = np.transpose(average)
	deviation = np.transpose(deviation)

	instants_tuple = []

	for i in range(len(instants)):
		aux_conclusion = []

		#classification of singular points - Axis by Axis
		for j in range(len(instants[0])):
			aux = instantCompare(instants[i][j], average[j], deviation[j], file_tags)

			#saves only classifications where there are no interpolations
			if(aux != (len(file_tags) + 1)):
				aux_conclusion.append(aux)
			
		#classification of all axes points
		if(len(aux_conclusion) > 0):
				instants_tuple.append(tuple(aux_conclusion[instant] for instant in range(len(aux_conclusion))))

	return (instants_tuple)
	

def instantCompare( instant, average, deviation, file_tags):
	"""
	This function receives 4 parameters with the objective of classifying the point X, Y or Z, 
	using the average and standard deviation of the corresponding axis.

	:param instant: Floating point value
	:param average: List containing the averages that will be used in the test
	:param deviation: List containing the standard deviations that will be used in the test
	:param file_tags: List that has the size of the labels for classification, not necessarily being filled with the labels themselves.
	
	:return: Returns an integer value that represents the classification of the tested point, which can take the following values:
		from 0 to the size of <param file_tags> - 1, represents that the point was classified with the corresponding label.
		Size of <param file_tags>, represents that the point is not in the test metrics range.
		Size of <param file_tags> + 1, represents that the point is in the range of more than one test metric.
	"""
	conclusion = -1
	interpolation = 0

	try:
		for i in range(len(average)):
			if(instant >= (average[i] - deviation[i]) and instant <= (average[i] + deviation[i])):
				conclusion = i
				interpolation += 1

	except:
		if(instant >= (average - deviation) and instant <= (average + deviation)):
			conclusion = 0
		
	if(interpolation > 1):
		conclusion = (len(file_tags) + 1)

	if(conclusion == -1):
		conclusion = len(file_tags)

	return conclusion

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def instantsClassification(instant, file_tags):
    instant = np.array(instant)

    # Caso binário (só "NF"): NF somente se TODOS forem NF
    if len(file_tags) == 1:
        return 0 if np.all(instant == 0) else len(file_tags)

    # --- abaixo mantém sua lógica original para múltiplos rótulos (NF, FC1, FC2, ...) ---

    for i in range(len(file_tags)):
        auxConclusion = np.where(instant == i)[0]
        if len(auxConclusion) == len(instant):
            return i
        if len(auxConclusion) == 2:
            if instant[auxConclusion[0]] == 0:
                for j in range(len(instant)):
                    if instant[j] > 0:
                        if instant[j] == len(file_tags):
                            return 0
                        return instant[j]
            return i

    if len(instant) == 2:
        healthy = np.where(instant == 0)[0]
        failure = np.where(instant > 0)[0]
        if len(failure) == 2:
            if (instant[failure[0]] >= 1 and instant[failure[0]] < len(file_tags) and
                instant[failure[1]] >= 1 and instant[failure[1]] < len(file_tags)):
                return len(file_tags)
            if instant[failure[0]] < len(file_tags):
                return instant[failure[0]]
            else:
                return instant[failure[1]]
        if len(failure) == 1 and instant[failure[0]] == len(file_tags):
            return instant[healthy[0]]
        if len(failure) == 1:
            return instant[failure[0]]

    return len(file_tags)


import numpy as np

INCONCLUSIVE = "inconclusivo"

def windowing_classification(axes_classification, window_size, hop=1):
    """
    axes_classification: lista de rótulos por instante (strings: "NF" ou "inconclusivo")
    window_size: tamanho da janela
    hop: passo do deslizamento (1 = máxima sobreposição)
    """
    out = []
    N = len(axes_classification)
    if N == 0 or window_size <= 0 or hop <= 0:
        return out

    # garante ao menos 1 iteração quando N < window_size
    last_start = 0 if N < window_size else (N - window_size)
    for start in range(0, last_start + 1, hop):
        end = min(start + window_size, N)
        window = axes_classification[start:end]

        # ignora votos inconclusivos na contagem
        valid = [w for w in window if w != INCONCLUSIVE]
        if not valid:
            out.append(INCONCLUSIVE)
            continue

        values, counts = np.unique(valid, return_counts=True)
        top = counts.max()
        winners = values[counts == top]

        out.append(INCONCLUSIVE if len(winners) > 1 else str(winners[0]))
    return out


def classification(sac_instants, means, deviations, window_size=5, hop=1, file_tags=("NF",)):
    """
    Retorna "NF" ou "inconclusivo".
    - testingInstants(...) deve classificar por eixo/instante usando média±desvio.
    - instantsClassification(...) deve combinar X/Y/Z por instante aplicando
      as regras do artigo; como você usa só "NF" como rótulo válido, qualquer
      coisa que não seja unanimidade/maioria para "NF" vira "inconclusivo".
    """
    sac_classification = testingInstants(sac_instants, means, deviations, file_tags)

    # rótulo COMBINADO por instante (string): "NF" ou "inconclusivo"
    axes_classification = [instantsClassification(sac_classification[i], file_tags)
                           for i in range(len(sac_classification))]

    # janelamento deslizante
    window_cls = windowing_classification(axes_classification, window_size, hop)
    if not window_cls:
        return INCONCLUSIVE

    # decisão final por maioria sobre as janelas (ignora inconclusivo)
    valid = [c for c in window_cls if c != INCONCLUSIVE]
    if not valid:
        return INCONCLUSIVE

    values, counts = np.unique(valid, return_counts=True)
    top = counts.max()
    winners = values[counts == top]
    return INCONCLUSIVE if len(winners) > 1 else str(winners[0])




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def plotEditingHalfTraining(dataset, title, fig, ax, file_tag):
	
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

	# ax.plot(x,y,color=colors[10], label = (f"Average of the first half of the SAC {file_tag}"))
	ax.plot(x,y,color=colors[10])

	for j in range(len(half_dataset)):

		if(aux_dev[j] != 0):			
			ax.errorbar(j,average_dataset,yerr = aux_dev[j], color = colors[20],marker='s', capsize=2, markersize=4, linewidth=1, linestyle='--')

	# ax.fill_between(x, average_dataset - deviation_dataset, average_dataset + deviation_dataset, alpha = 0.2, label = (f"Standard Deviation of the first half of the File {file_tag}"))
	ax.fill_between(x, average_dataset - deviation_dataset, average_dataset + deviation_dataset, alpha = 0.2)

def plotTesting(dataset, title, fig, ax, color):

	colors = list(mcolors.CSS4_COLORS) 
	ax.plot(dataset,color=colors[color], label = title)
	ax.set_xlim(left= -1)
	
def plotTraining(dataset, title, file_tag):	
	
	fig, axs = plt.subplots(3)
	fig.suptitle(title)

	#Creating subgraph titles
	auxT = [("x-axis"), ("y-axis"), ("z-axis")]
	
	for i in range(len(dataset)):

		plotEditingHalfTraining(dataset[i], title, fig, axs[i],file_tag)
		testing_data = sampling_sac(dataset[i], round(len(dataset[i])/2), len(dataset[i]) )
		plotTesting(testing_data, (f"Second half of the file {file_tag}"), fig, axs[i], (11+i))
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
		plotEditingHalfTraining(dataset[0][i], "", fig, axs[i], file_tag[0])
		
		#Files
		for j in range(0 ,len(dataset)):
			testing_data = sampling_sac(dataset[j][i], round(len(dataset[j][i])/2), len(dataset[j][i]) )
			k = j
			if(j == 1):
				k = -10
			plotTesting(testing_data, (f"{file_tag[j]}"), fig, axs[i], (32+k))
		
		axs[i].set_xlim(-1, round(len(dataset[0][i]) * 0.575))
		axs[i].legend(loc='upper right')

	axs[0].set(ylabel = ("x-axis"))
	axs[1].set(ylabel = ("y-axis"))
	axs[2].set(ylabel = ("z-axis"))	

def plotSACsAxis(dataset, title, file_tag):

	#Creating base graphics (Training)
	fig, ax = plt.subplots()
	ax.set_title(title)

	#Plot the axes on base graphs (Test)
	for i in range(len(dataset)):
		plotTesting(dataset[i], (f"File: {file_tag[i]}"), fig, ax, (10+i))
	
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
		filename = (f"confusionMatrixplotHalfTrainingN{N}.txt")
		header = (f"Confusion matrix[%] \n\n")
		saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)

def slidingWindow(dataset, file_tags, title, window_size, N, save=False):

	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	count_window = np.zeros((len(dataset)))
	outputMatrix = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))
	
	instants_classification = []

	#File
	for i in range(len(dataset)):
		aux_instantes = []
		#Axes
		for j in range(round(len(dataset[i])/2), len(dataset[i])):
			#Instants
				
			aux = instantCompare(dataset[i][j], average, deviation, file_tags)
			if(aux != (len(file_tags) + 1)):
				aux_instantes.append(aux)
			# print(f"instant: {dataset[i][j]} file: {i} classification: {aux}")
		instants_classification.append(np.array(aux_instantes))

	for i in range(len(instants_classification)):
		for j in range((len(instants_classification[i]) - window_size + 1)):
			window = np.zeros(window_size)
			window = instants_classification[i][j:j+window_size]
			counts = np.bincount(window)

			if(j == (len(window) - 1)):
				outputMatrix[i][np.argmax(counts)] += 1 * window_size
				count_window[i] += 1 * window_size
			else:
				outputMatrix[i][np.argmax(counts)] += 1
				count_window[i] += 1
			# print(f"window: {(window)} file: {i} classification: {np.argmax(counts)}")

	for i in range(len(outputMatrix)):
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)

	if(save == True):
		filename = (f"SlidingWindowN{N}Size{window_size}.txt")
		header = (f"Confusion matrix[%] - Sliding window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
		saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)
	
	return outputMatrix, count_window

def jumpingWindow(dataset, file_tags, title, window_size, N, save=False):
	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	count_window = np.zeros((len(dataset)))
	outputMatrix = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))

	instants_classification = []

	#File
	for i in range(len(dataset)):
		aux_instantes = []
		#Axes
		for j in range(round(len(dataset[i])/2), len(dataset[i])):
			#Instants
				
			aux = instantCompare(dataset[i][j], average, deviation, file_tags)
			if(aux != (len(file_tags) + 1)):
				aux_instantes.append(aux)
			# print(f"instant: {dataset[i][j]} file: {i} classification: {aux}")
		instants_classification.append(np.array(aux_instantes))

	for i in range(len(instants_classification)):
		for j in range(0,(len(instants_classification[i])), window_size):
			count_window[i] += 1
			window = np.zeros(window_size)
			if (j + window_size <= len(instants_classification[i])):
				window = instants_classification[i][j:j+window_size]

			else:
				window = instants_classification[i][j:]
			
			counts = np.bincount(window)
			outputMatrix[i][np.argmax(counts)] += 1
			# print(f"window: {(window)} file: {i} classification: {np.argmax(counts)}")

	for i in range(len(outputMatrix)):
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)

	if(save == True):
		filename = (f"JumpingWindowN{N}Size{window_size}.txt")
		header = (f"Confusion matrix[%] - Jumping Window[{window_size}] - N{N} - Quantity of windows{count_window}\n\n")
		saveMatrixInTxt(outputMatrix, average, deviation, title, N, filename, file_tags, header)
	
	return outputMatrix, count_window

def printAnalysisMatrix(outputMatrix, window_quantity, window_size, analysis_type,file_tags, average, deviation, title, N, save=False):

	print(f"Confusion matrix[%] - {analysis_type}[{window_size}] - N{N} - Quantity of windows{window_quantity}\n\n")
	print((f"{'File':<10}"), end="")
	for i in range(len(file_tags)):
		print(f"{file_tags[i]:<10}", end="")
	print(f"{'Inconclusive':<10}")

	for i in range(len(outputMatrix)):
		print(f"{file_tags[i]:<10}", end="")
		for j in range(len(outputMatrix[i])):
			aux = (f"{outputMatrix[i][j]}%")
			print(f"{aux:<10}", end="")
		print("\n")

	if(save == True):
		filename = (f"{analysis_type}N{N}Size{window_size}.txt")
		header = (f"Confusion matrix[%] - {analysis_type}[{window_size}] - N{N} - Quantity of windows{window_quantity}\n\n")
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

	instants_gathered = []
	instants_classification = []

	#Files
	for i in range(len(dataset)):
		instants_files = []

		#SAC'S instants classification
		for j in range( round(len(dataset[i][0])/2), (len(dataset[i][0]))):
			conclusion = []
			#Axes
			for k in range(3):
				aux = instantCompare(dataset[i][k][j], average[k], deviation[k], file_tags)
				if(aux != (len(file_tags) + 1)):
					conclusion.append(aux)
			
			if(len(conclusion) > 0):
				instants_files.append(conclusion)
		
		instants_gathered.append(instants_files)

	for i in range(len(instants_gathered)):
		aux_instantes = []
		for j in range(len(instants_gathered[i])):
			aux = instantsClassification(instants_gathered[i][j], file_tags)
			if(aux != (len(file_tags) + 1)):
				aux_instantes.append(instantsClassification(instants_gathered[i][j], file_tags))
			# print(f"instant-sac: {instants_gathered[i][j]} file: {i} classification: {aux}")
		if(len(aux_instantes) > 0):
			instants_classification.append(np.array(aux_instantes))


	for i in range(len(instants_classification)):
		for j in range(0,(len(instants_classification[i])), window_size):
			count_window[i] += 1
			window = np.zeros(window_size)
			if (j + window_size <= len(instants_classification[i])):
				window = instants_classification[i][j:j+window_size]

			else:
				window = instants_classification[i][j:]
				
			values, counts = np.unique(window, return_counts=True)

			#	checks if there is more than one value with the same and greater repetition
			if(np.count_nonzero(counts == counts[np.argmax(counts)]) > 1):
				outputMatrix[i][len(file_tags)] += 1
				# print(f"window: {(window)} file: {i} classification: {len(file_tags)}")
			else:
				outputMatrix[i][values[np.argmax(counts)]] += 1
				# print(f"window: {(window)} file: {i} classification: {values[np.argmax(counts)]}")

	for i in range(len(outputMatrix)):
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)

	return outputMatrix, count_window

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

	instants_gathered = []
	instants_classification = []

	#Files
	for i in range(len(dataset)):
		instants_files = []

		#SAC'S instants classification
		for j in range( round(len(dataset[i][0])/2), (len(dataset[i][0]))):
			conclusion = []
			#Axes
			for k in range(3):
				aux = instantCompare(dataset[i][k][j], average[k], deviation[k], file_tags)
				if(aux != (len(file_tags) + 1)):
					conclusion.append(aux)
			
			if(len(conclusion) > 0):
				instants_files.append(conclusion)
		
		instants_gathered.append(instants_files)

	for i in range(len(instants_gathered)):
		aux_instantes = []
		for j in range(len(instants_gathered[i])):
			aux = instantsClassification(instants_gathered[i][j], file_tags)
			if(aux != (len(file_tags) + 1)):
				aux_instantes.append(instantsClassification(instants_gathered[i][j], file_tags))
			# print(f"instant-sac: {instants_gathered[i][j]} file: {i} classification: {aux}")
		if(len(aux_instantes) > 0):
			instants_classification.append(np.array(aux_instantes))

	for i in range(len(instants_classification)):
		for j in range((len(instants_classification[i]) - window_size + 1)):
			window = np.zeros(window_size)
			window = instants_classification[i][j:j+window_size]
			counts = np.bincount(window)

			if(j == (len(window) - 1)):
				outputMatrix[i][np.argmax(counts)] += 1 * window_size
				count_window[i] += 1 * window_size
			else:
				outputMatrix[i][np.argmax(counts)] += 1
				count_window[i] += 1
			# print(f"window: {(window)} file: {i} classification: {np.argmax(counts)}")

	for i in range(len(instants_classification)):
		for j in range((len(instants_classification[i]) - window_size + 1)):
			window = np.zeros(window_size)
			window = instants_classification[i][j:j+window_size]

			if(j == (len(window) - 1)):
				count_window[i] += 1 * window_size
			else:
				count_window[i] += 1
				
			values, counts = np.unique(window, return_counts=True)

			#	checks if there is more than one value with the same and greater repetition
			if(np.count_nonzero(counts == counts[np.argmax(counts)]) > 1):
				outputMatrix[i][len(file_tags)] += 1
				# print(f"window: {(window)} file: {i} classification: {len(file_tags)}")
			else:
				outputMatrix[i][values[np.argmax(counts)]] += 1
				# print(f"window: {(window)} file: {i} classification: {values[np.argmax(counts)]}")

	for i in range(len(outputMatrix)):
		for j in range(len(outputMatrix[i])):
			outputMatrix[i][j] = round(get_change_t(outputMatrix[i][j],count_window[i]),2)

	return outputMatrix, count_window

def plot_heat_jumpingWindowAllAxes(dataset, file_tags, title, window_size, N):

	outputMatrix, _ = jumpingWindowAllAxes(dataset, file_tags, title, window_size, N)
	labels = file_tags + ["Inconclusive"]

	# Min = 0% Max = 100%
	# outputMatrixN = (outputMatrix - outputMatrix.min()) / (outputMatrix.max() - outputMatrix.min())
	outputMatrixN = outputMatrix / 100

	fig, ax = plt.subplots()
	im, cbar = heatmap(outputMatrixN, file_tags, labels, ax=ax, cmap="Blues", cbarlabel="")

	# Loop over data dimensions and create text annotations.
	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN[i][j], 2)
			if(percentage > 0.45):
				ax.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax.text(j, i, percentage, ha="center", va="center", color="b")

	titleJump = title + (f"Jumping window[N:{N}, WindowSize:{window_size}]")
	ax.set_title(titleJump)
	ax.set(ylabel = "True label", xlabel =  "Predicted label")
	fig.tight_layout()

def plot_heat_slidingWindowAllAxes(dataset, file_tags, title, window_size, N):

	outputMatrix, _ = slidingWindowAllAxes(dataset, file_tags, title, window_size, N)
	labels = file_tags + ["Inconclusive"]

	# Min = 0% Max = 100%
	# outputMatrixN = (outputMatrix - outputMatrix.min()) / (outputMatrix.max() - outputMatrix.min())
	outputMatrixN = outputMatrix / 100
	
	fig, ax = plt.subplots()
	im, cbar = heatmap(outputMatrixN, file_tags, labels, ax=ax, cmap="Blues", cbarlabel="")

	# Loop over data dimensions and create text annotations.
	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN[i][j], 2)
			if(percentage > 0.2):
				ax.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax.text(j, i, percentage, ha="center", va="center", color="b")

	titleJump = title + (f"Sliding window[N:{N}, WindowSize:{window_size}]")
	ax.set_title(titleJump)
	ax.set(ylabel = "True label", xlabel =  "Predicted label")
	fig.tight_layout()

def plot_heat_jumpingWindowAxis(dataset, file_tags, title, window_size, N):

	outputMatrix_x, _ = jumpingWindow(dataset[0], file_tags, title, window_size, N,save=False)
	outputMatrix_y, _ = jumpingWindow(dataset[1], file_tags, title, window_size, N,save=False)
	outputMatrix_z, _ = jumpingWindow(dataset[2], file_tags, title, window_size, N,save=False)
	labels = file_tags + ["   Inconclusive"]

	# Min = 0% Max = 100%
	# outputMatrixN = (outputMatrix - outputMatrix.min()) / (outputMatrix.max() - outputMatrix.min())
	outputMatrixN_x = outputMatrix_x / 100
	outputMatrixN_y = outputMatrix_y / 100
	outputMatrixN_z = outputMatrix_z / 100

	fig, (ax_x, ax_y, ax_z) = plt.subplots(3)
	plt.subplots_adjust(left=0.06, right=0.70, bottom=0.06, top=0.93)

	im, cbar = heatmap(outputMatrixN_x, file_tags, labels, ax=ax_x, cmap="Blues", cbarlabel="")
	im, cbar = heatmap(outputMatrixN_y, file_tags, labels, ax=ax_y, cmap="Blues", cbarlabel="")
	im, cbar = heatmap(outputMatrixN_z, file_tags, labels, ax=ax_z, cmap="Blues", cbarlabel="")

	# Loop over data dimensions and create text annotations.
	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN_x[i][j], 2)
			if(percentage > 0.45):
				ax_x.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax_x.text(j, i, percentage, ha="center", va="center", color="b")

	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN_y[i][j], 2)
			if(percentage > 0.45):
				ax_y.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax_y.text(j, i, percentage, ha="center", va="center", color="b")

	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN_z[i][j], 2)
			if(percentage > 0.2):
				ax_z.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax_z.text(j, i, percentage, ha="center", va="center", color="b")

	titleJump = title + (f"Jumping window[N:{N}, WindowSize:{window_size}]")
	fig.suptitle(titleJump)
	ax_x.set(ylabel = "True label")
	ax_x.set_title("x-axis")
	ax_y.set(ylabel = "True label")
	ax_y.set_title("y-axis")
	ax_z.set(ylabel = "True label", xlabel =  "Predicted label")
	ax_z.set_title("z-axis")

def plot_heat_slidingWindowAxis(dataset, file_tags, title, window_size, N):

	outputMatrix_x, _ = slidingWindow(dataset[0], file_tags, title, window_size, N,save=False)
	outputMatrix_y, _ = slidingWindow(dataset[1], file_tags, title, window_size, N,save=False)
	outputMatrix_z, _ = slidingWindow(dataset[2], file_tags, title, window_size, N,save=False)
	labels = file_tags + ["   Inconclusive"]

	# Min = 0% Max = 100%
	# outputMatrixN = (outputMatrix - outputMatrix.min()) / (outputMatrix.max() - outputMatrix.min())
	outputMatrixN_x = outputMatrix_x / 100
	outputMatrixN_y = outputMatrix_y / 100
	outputMatrixN_z = outputMatrix_z / 100

	fig, (ax_x, ax_y, ax_z) = plt.subplots(3)
	plt.subplots_adjust(left=0.06, right=0.70, bottom=0.06, top=0.93)

	im, cbar = heatmap(outputMatrixN_x, file_tags, labels, ax=ax_x, cmap="Blues", cbarlabel="")
	im, cbar = heatmap(outputMatrixN_y, file_tags, labels, ax=ax_y, cmap="Blues", cbarlabel="")
	im, cbar = heatmap(outputMatrixN_z, file_tags, labels, ax=ax_z, cmap="Blues", cbarlabel="")

	# Loop over data dimensions and create text annotations.
	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN_x[i][j], 2)
			if(percentage > 0.45):
				ax_x.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax_x.text(j, i, percentage, ha="center", va="center", color="b")

	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN_y[i][j], 2)
			if(percentage > 0.45):
				ax_y.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax_y.text(j, i, percentage, ha="center", va="center", color="b")

	for i in range(len(file_tags)):
		for j in range(len(labels)):
			percentage = round(outputMatrixN_z[i][j], 2)
			if(percentage > 0.45):
				ax_z.text(j, i, percentage, ha="center", va="center", color="w")
			else:
				ax_z.text(j, i, percentage, ha="center", va="center", color="b")

	titleJump = title + (f"Sliding window[N:{N}, WindowSize:{window_size}]")
	fig.suptitle(titleJump)
	ax_x.set(ylabel = "True label")
	ax_x.set_title("x-axis")
	ax_y.set(ylabel = "True label")
	ax_y.set_title("y-axis")
	ax_z.set(ylabel = "True label", xlabel =  "Predicted label")
	ax_z.set_title("z-axis")

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
	filename = (f"confusionMatrixplotHalfTrainingN{N}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	file1.close()

def get_change_t(current, previous):
	if( current == 0 and previous == 0):
		return 0
    
	if current == previous:
		return 100.0
	try:
		return (abs(current)  / previous) * 100.0
	except ZeroDivisionError:
		return 0

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

def show():

	plt.show()
