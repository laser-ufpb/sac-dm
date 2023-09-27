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

	conclusion = np.zeros((len(file_tags) + 1))
	for i in range(len(window)):
		wasFailure = False
		for j in range(len(file_tags)):
			if (window[i] >= average[j] - deviation[j] and window[i] <= average[j] + deviation[j]):
				wasFailure = True
				conclusion[j] += 1
				break
		if(wasFailure == False):
			conclusion[len(file_tags)] += 1

	return conclusion	

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

				elif(window[k] >= average[3] - deviation[3] and window[k] <= average[3] + deviation[3]):
					conclusion[3] += 1
					continue
				
				else:
					conclusion[4] += 1
			
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

def plotWindowsComparationAllAxes(dataset, file_tags, title, window_size, N):
	average = np.zeros(round(len(dataset[0])/2))
	deviation = np.zeros((round(len(dataset[0])/2)))
	count_window_jumping = np.zeros((len(dataset)))
	count_window_sliding = np.zeros((len(dataset)))
	jumpingMatrixOutput = np.zeros((len(dataset),len(dataset)+1))
	slidingMatrixOutput = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		average[i] = average_sac(dataset[i], 0, round(len(dataset[i])/2))
		deviation[i] = deviation_sac(dataset[i], 0, round(len(dataset[i])/2))

	#Array of SACs
	for j in range( round(len(dataset[0])/2), (len(dataset[0]) - window_size + 1) ):
		window = dataset[i][j:j+window_size]
		conclusion = np.zeros((len(file_tags) + 1))
		
		
		if(j == (len(dataset[i]) - window_size)):
			slidingMatrixOutput[i][np.argmax(conclusion)] += 1 * window_size
			count_window_sliding[i] += 1 * window_size
		else:
			slidingMatrixOutput[i][np.argmax(conclusion)] += 1
			count_window_sliding[i] += 1

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

