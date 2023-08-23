import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import matplotlib.colors as mcolors
import time

def treinamentoMetade(dataset, title, fig, ax, file_tag):
	
	plt.ylabel(title) 
	plt.xlabel('Time (ms)')
	
	half_dataset = amostragem_sac(dataset, 0, round(len(dataset)/2))
	colors = list(mcolors.CSS4_COLORS) 

	media_dataset = media_sac(half_dataset, 0, len(half_dataset))
	desv_dataset = desvio_sac(half_dataset, 0, len(half_dataset))

	aux_desv = np.zeros(len(half_dataset))
	aux_desv[round(len(half_dataset)/2)] = desv_dataset

	x = np.arange(len(half_dataset))
	y = np.zeros(len(half_dataset))
	y = np.full_like(y, media_dataset)

	ax.plot(x,y,color=colors[10], label = (f"Média da primeira metade do SAC {file_tag}"))

	for j in range(len(half_dataset)):

		if(aux_desv[j] != 0):			
			ax.errorbar(j,media_dataset,yerr = aux_desv[j], color = colors[20],marker='s', capsize=2, markersize=4, linewidth=1, linestyle='--')

	ax.fill_between(x, media_dataset - desv_dataset, media_dataset + desv_dataset, alpha = 0.2, label = (f"Desvio Padrão da primeira metade do Arquivo {file_tag}"))

def treinamentoCompleto(dataset, title, fig, ax, file_tag):
	
	aux = title.split(':',1)
	plt.ylabel(aux[0]) 
	plt.xlabel('Time (ms)')

	ax.set_title(title)  
	colors = list(mcolors.CSS4_COLORS) 

	media_dataset = media_sac(dataset, 0, round(len(dataset)))
	desv_dataset = desvio_sac(dataset, 0, round(len(dataset)))

	aux_desv = np.zeros(len(dataset))
	aux_desv[round((len(dataset))/2)] = desv_dataset

	x = np.arange(len(dataset))
	y = np.zeros(len(dataset))
	y = np.full_like(y, media_dataset)

	ax.plot(x,y,color=colors[10], label = (f"Média do Arquivo {file_tag}"))


	plt.xlim(right = (len(dataset)))

	for j in range(len(dataset)):

		if(aux_desv[j] != 0):			
			ax.errorbar(j,media_dataset,yerr = aux_desv[j], color = colors[20],marker='s', capsize=2, markersize=4, linewidth=1, linestyle='--')

	ax.fill_between(x, media_dataset - desv_dataset, media_dataset + desv_dataset, alpha = 0.2, label = (f"Desvio Padrão do Arquivo {file_tag}"))

def testagem(dataset, title, fig, ax, color):

	colors = list(mcolors.CSS4_COLORS) 
	ax.plot(dataset,color=colors[color], label = title)
	
def showTreinamentoM(dataset, title, file_tag):	
	
	fig, axs = plt.subplots(3)
	fig.suptitle(title)

	#				Criando os titulos dos subgrafos
	auxT = [("Eixo X"), ("Eixo Y"), ("Eixo Z")]
	
	for i in range(len(dataset)):
		# axs[i].set_title(auxT[i])
		treinamentoMetade(dataset[i], title, fig, axs[i],file_tag)
		dataset_teste = amostragem_sac(dataset[i], round(len(dataset[i])/2), len(dataset[i]) )
		testagem(dataset_teste, (f"Segunda metade do arquivo {file_tag}"), fig, axs[i], (11+i))
		axs[i].set(ylabel = auxT[i])
		# axs[i].legend(loc = 'upper right')

def showTreinamentoC(dataset, title, file_tag):	
	
	fig, axs = plt.subplots(3)
	fig.suptitle(title)

	#				Criando os titulos dos subgrafos
	auxT = [("Eixo X"), ("Eixo Y"), ("Eixo Z")]
	
	for i in range(len(dataset)):
		# axs[i].set_title(auxT[i])
		treinamentoCompleto(dataset[i], "", fig, axs[i],file_tag)
		testagem(dataset[i], (f"Segunda metade do arquivo {file_tag}"), fig, axs[i], (11+i))
		axs[i].set(ylabel = auxT[i])
		# axs[i].legend(loc = 'upper right')



def showSAC_figUnicaComTreinoC(dataset, title, file_tag):
 
	# # Criando graficos base ( Treinamento )
	fig, axs = plt.subplots(3)

	fig.suptitle(title)
	aux = title.split(':',1)

	# # Plotar os eixos nos gráficos base ( Teste )
	for i in range(len(dataset[0])):#	eixos 
		treinamentoCompleto(dataset[0][i], "", fig, axs[i], file_tag[0])

		for j in range(len(dataset)):# arquivos
			testagem(dataset[j][i], (f"Arquivo: {file_tag[j]}"), fig, axs[i], (11+j))

		axs[i].set_xlim(-1, round(len(dataset[0][i])))
		axs[i].legend(loc='lower right')

	axs[0].set(ylabel = (aux[0] + ": Eixo X"))
	axs[1].set(ylabel = (aux[0] + ": Eixo Y"))
	axs[2].set(ylabel = (aux[0] + ": Eixo Z"))

def showSAC_figUnicaComTreinoM(dataset, title, file_tag):

	# # Criando graficos base ( Treinamento )
	fig, (axs) = plt.subplots(3)

	fig.suptitle(title)
	aux = title.split(':',1)

	# # Plotar os eixos nos gráficos base ( Teste )
	for i in range(len(dataset[0])):#	eixos 
		treinamentoMetade(dataset[0][i], "", fig, axs[i], file_tag[0])
		
		for j in range(0 ,len(dataset)):# arquivos
			dataset_teste = amostragem_sac(dataset[j][i], round(len(dataset[j][i])/2), len(dataset[j][i]) )
			testagem(dataset_teste, (f"Segunda metade do Arquivo: {file_tag[j]}"), fig, axs[i], (11+j))
		
		axs[i].set_xlim(-1, round(len(dataset[0][i])))
		axs[i].legend(loc='lower right')
		
	axs[0].set(ylabel = (aux[0] + ": Eixo X"))
	axs[1].set(ylabel = (aux[0] + ": Eixo Y"))
	axs[2].set(ylabel = (aux[0] + ": Eixo Z"))
	

def showSacUnicoEixo(dataset, title, file_tag):

	# # Criando graficos base ( Treinamento )
	fig, ax = plt.subplots()
	ax.set_title(title)

	# # Plotar os eixos nos gráficos base ( Teste )
	for i in range(len(dataset)):
		testagem(dataset[i], (f"Arquivo: {file_tag[i]}"), fig, ax, (10+i))
	ax.legend(loc='lower right')


def media_sac(dataset,inicio,fim):

	media = np.average(dataset[inicio:fim])

	return media

def variancia_sac(dataset,inicio,fim):

	variancia = np.var(dataset[inicio:fim])

	return variancia

def desvio_sac(dataset, inicio, fim):

	desvio_padrao = np.std(dataset[inicio:fim])

	return desvio_padrao

def amostragem_sac(dataset, inicio, fim):

	return dataset[inicio:fim]

def confusionMatrix(dataset, arquivos, title):

	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	matrix = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range(len(dataset[i])): # array com n pontos
			
			if (dataset[i][j] >= media[0] - desvio[0] and dataset[i][j] <= media[0] + desvio[0]):
				matrix[i][0] += 1
				continue

			elif(dataset[i][j] >= media[1] - desvio[1] and dataset[i][j] <= media[1] + desvio[1]):
				matrix[i][1] += 1
				continue

			elif(dataset[i][j] >= media[2] - desvio[2] and dataset[i][j] <= media[2] + desvio[2]):
				matrix[i][2] += 1
				continue

			elif(dataset[i][j] >= media[3] - desvio[3] and dataset[i][j] <= media[3] + desvio[3]):
				matrix[i][3] += 1
				continue
			
			else:
				matrix[i][4] += 1

	for i in range(len(dataset)): 
		matrix[i] = np.round((matrix[i] / len(dataset[i])) * 100, decimals=1)  #converte os valores da matriz para valores percentuais.

	print(f"\n\t\t{title}\n")

	print(f"{'Arquivo':<10}", end="")
	for i in range(len(arquivos)):
		print(f"{arquivos[i]:<10}", end="")

	print(f"{'Inconclusivo':<10}")

	for i in range(len(matrix)):
		values = [f"{matrix[i][j]}%" for j in range(len(matrix[i]))] #adiciona '%' nos valores da matriz.
		print(f"{arquivos[1]:<10}{values[0]:<10}{values[1]:<10}{values[2]:<10}{values[3]:<10}{values[4]:<10}")

def confusionMatrixInTxt(dataset, arquivos, title):

	file1 = open('confusionMatrix.txt', 'a+')
	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	matrix = np.zeros((len(dataset),len(dataset)+1))
	pontos_inconclusivos = np.zeros((len(dataset),len(dataset[0])))
	pontos_inconclusivos_ordenados = np.zeros((len(dataset),len(dataset[0])))

	file1.write((title + "\n\n"))
	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))
		file1.write((arquivos[i] + ":" + " Média - " + str(round(media[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Desvio padrao - " + str(round(desvio[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Limite inferior - " + str(round(media[i] - desvio[i], 4)) + " | " + "Limite superior - " + str(round(media[i] + desvio[i], 4)) +"\n\n"))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range(len(dataset[i])): # array com n pontos
			
			if (dataset[i][j] >= media[0] - desvio[0] and dataset[i][j] <= media[0] + desvio[0]):
				matrix[i][0] += 1
				continue

			elif(dataset[i][j] >= media[1] - desvio[1] and dataset[i][j] <= media[1] + desvio[1]):
				matrix[i][1] += 1
				continue

			elif(dataset[i][j] >= media[2] - desvio[2] and dataset[i][j] <= media[2] + desvio[2]):
				matrix[i][2] += 1
				continue

			elif(dataset[i][j] >= media[3] - desvio[3] and dataset[i][j] <= media[3] + desvio[3]):
				matrix[i][3] += 1
				continue
			
			else:
				pontos_inconclusivos[i][j] = dataset[i][j] 
				matrix[i][4] += 1

	qtd_max_pontos = 0
	for i in range(len(dataset)):
		pontos_inconclusivos_ordenados[i] = np.sort(pontos_inconclusivos[i])
		if(matrix[i][4] > qtd_max_pontos):
			qtd_max_pontos = int(matrix[i][4])

	pontos_inconclusivos_porcent_Menor = np.zeros((len(dataset),qtd_max_pontos))
	pontos_inconclusivos_porcent_Maior = np.zeros((len(dataset),qtd_max_pontos))

	file1.write("Matriz de confusao\n\n")
	file1.write((f"{'Arquivo':<10}"))
	for i in range(len(arquivos)):
		file1.write(f"{arquivos[i]:<10}")
	file1.write(f"{'Inconclusivo':<10}\n")

	for i in range(len(matrix)):
		file1.write(f"{arquivos[i]:<10}{matrix[i][0]:<10}{matrix[i][1]:<10}{matrix[i][2]:<10}{matrix[i][3]:<10}{matrix[i][4]:<10}\n\n")

	pontos_str = ""
	pontos_str += ("Pontos inconclusivos ordenados com porcentagens: \n\n")
	for i in range(len(pontos_inconclusivos_ordenados)):
		aux = 0
		aux_porcent = 0
		for j in range(len(pontos_inconclusivos_ordenados[i])):

			if(pontos_inconclusivos_ordenados[i][j] != 0):

				if(pontos_inconclusivos_ordenados[i][j] < (media[i] - desvio[i])):
					indice = np.where(pontos_inconclusivos[i] == pontos_inconclusivos_ordenados[i][j])
					percentagem = get_change_t(pontos_inconclusivos_ordenados[i][j], (media[i] - desvio[i]))
					pontos_inconclusivos_porcent_Menor[i][aux_porcent] = percentagem
					pontos_str += (f"{arquivos[i]}-{indice[0]}:[Menor: {round(percentagem,2)}%] {round(pontos_inconclusivos_ordenados[i][j], 3)}  ")
					aux_porcent = aux_porcent + 1
					aux = aux + 1

				elif(pontos_inconclusivos_ordenados[i][j] > (media[i] + desvio[i])):
					indice = np.where(pontos_inconclusivos[i] == pontos_inconclusivos_ordenados[i][j])
					percentagem = get_change_t(pontos_inconclusivos_ordenados[i][j], (media[i] + desvio[i]))
					pontos_inconclusivos_porcent_Maior[i][aux_porcent] = percentagem
					pontos_str += (f"{arquivos[i]}-{indice[0]}:[Maior: {round(percentagem,2)}%] {round(pontos_inconclusivos_ordenados[i][j], 3)}  ")
					aux_porcent = aux_porcent + 1
					aux = aux + 1

			if(aux % 5 == 0.0 and aux != 0):
				pontos_str += ("\n")
				aux = 0
	
		pontos_str += ("\n\n")
	
	
	tabela_porcentagem_menor = np.zeros((len(dataset),11))
	tabela_porcentagem_maior = np.zeros((len(dataset),11))


	faixas_porcentagem = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
	for i in range(len(pontos_inconclusivos_porcent_Menor)):
		for j in range(len(pontos_inconclusivos_porcent_Menor[i])):
			valor = pontos_inconclusivos_porcent_Menor[i][j]
			for k in range(len(faixas_porcentagem)-1):
				if (valor != 0 and valor > faixas_porcentagem[k] and valor <= faixas_porcentagem[k+1]):
					tabela_porcentagem_menor[i][k] += 1
				if (valor != 0 and valor > faixas_porcentagem[10]):
					tabela_porcentagem_menor[i][10] += 1

	for i in range(len(pontos_inconclusivos_porcent_Maior)):
		for j in range(len(pontos_inconclusivos_porcent_Maior[i])):
			valor = pontos_inconclusivos_porcent_Maior[i][j]
			for k in range(len(faixas_porcentagem)-1):
				if (valor != 0 and valor > faixas_porcentagem[k] and valor <= faixas_porcentagem[k+1]):
					tabela_porcentagem_maior[i][k] += 1
				if (valor != 0 and valor > faixas_porcentagem[10]):
					tabela_porcentagem_maior[i][10] += 1

	file1.write("\nTabela das porcentagens menores que o limite inferior: \n\n")
	file1.write((f"{'':<10}"))
	file1.write((f"{'0-10%':<10}") + (f"{'10-20%':<10}") + (f"{'20-30%':<10}") + (f"{'30-40%':<10}") + (f"{'40-50%':<10}") + (f"{'50-60%':<10}") + (f"{'60-70%':<10}") + (f"{'70-80%':<10}") + (f"{'80-90%':<10}") + (f"{'90-100%':<10}") + (f"{'>100%':<10}\n"))
	for i in range(len(tabela_porcentagem_menor)):
		file1.write((f"{arquivos[i]:<10}"))
		for j in range(len(tabela_porcentagem_menor[i])):
			file1.write(f"{tabela_porcentagem_menor[i][j]:<10}")
		file1.write("\n")
	file1.write("\n\n")	
	
	file1.write("Tabela das porcentagem maiores que o limite superior: \n\n")
	file1.write((f"{'':<10}"))
	file1.write((f"{'0-10%':<10}") + (f"{'10-20%':<10}") + (f"{'20-30%':<10}") + (f"{'30-40%':<10}") + (f"{'40-50%':<10}") + (f"{'50-60%':<10}") + (f"{'60-70%':<10}") + (f"{'70-80%':<10}") + (f"{'80-90%':<10}") + (f"{'90-100%':<10}") + (f"{'>100%':<10}\n"))
	for i in range(len(tabela_porcentagem_maior)):
		file1.write((f"{arquivos[i]:<10}"))
		for j in range(len(tabela_porcentagem_maior[i])):
			file1.write(f"{tabela_porcentagem_maior[i][j]:<10}")
		file1.write("\n")
	
	file1.write("\n\nPontos inconclusivos: \n\n")
	for i in range(len(pontos_inconclusivos_ordenados)):
		aux = 0
		for j in range(len(pontos_inconclusivos[i])):

			if(pontos_inconclusivos[i][j] != 0):

				file1.write(f"{arquivos[i]}-{j}: {round(pontos_inconclusivos[i][j], 3)}  ")
				aux = aux + 1

			if(aux % 8 == 0.0 and aux != 0):
				file1.write("\n")
				aux = 0

		file1.write("\n\n")

	file1.write(pontos_str)
	file1.write("\n\n\n")	
	file1.close()

def cleanTxtSliding(N, window_size):
	filename = (f"LiteSlidingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	file1.close()

def cleanTxtMatrix(N):
	filename = (f"confusionMatrixHalfTrainingN{N}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	filename = (f"confusionMatrixCompleteTrainingN{N}.txt")
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

def slidingWindowDetailedInTxt(dataset, arquivos, title, window_size, N):

	filename = (f"LiteSlidingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	count_window = np.zeros((len(dataset)))
	matrixSaida = np.zeros((len(dataset),len(dataset)+1))
	matrix = np.zeros((len(dataset),len(dataset)+1))

	file1.write((title + "\n\n"))
	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))
		file1.write((arquivos[i] + ":" + " Média - " + str(round(media[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Desvio padrao - " + str(round(desvio[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Limite inferior - " + str(round(media[i] - desvio[i], 4)) + " | " + "Limite superior - " + str(round(media[i] + desvio[i], 4)) +"\n\n"))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos

		for j in range( (len(dataset[i]) - window_size + 1) ): # array com n pontos
			janela = dataset[i][j:j+window_size]
			conclusion = np.zeros((len(arquivos) + 1))
			
			for k in range(len(janela)):
				if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
					conclusion[0] += 1
					continue

				elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
					conclusion[1] += 1
					continue

				elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
					conclusion[2] += 1
					continue

				elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
					conclusion[3] += 1
					continue
				
				else:
					conclusion[4] += 1
			
			if(j == (len(dataset[i]) - window_size)):
				matrix[i][np.argmax(conclusion)] += 1 * window_size
				count_window[i] += 1 * window_size
			else:
				matrix[i][np.argmax(conclusion)] += 1
				count_window[i] += 1

				

	file1.write(f"Matriz de confusao - Janela Deslizante[{window_size}] - N{N} - Qtd de janelas{count_window}\n\n")
	file1.write((f"{'Arquivo':<10}"))
	for i in range(len(arquivos)):
		file1.write(f"{arquivos[i]:<10}")
	file1.write(f"{'Inconclusivo':<10}\n")

	for i in range(len(matrix)):
		file1.write(f"{arquivos[i]:<10}")
		for j in range(len(matrix[i])):
			# matrixSaida[i][j] = round(get_change_t(matrix[i][j],count_window[i]),2)
			matrixSaida[i][j] = round(matrix[i][j],2)
			file1.write(f"{matrixSaida[i][j]:<10}")
		file1.write("\n\n")


	file1.close()

def jumpingWindowDetailedInTxt(dataset, arquivos, title, window_size, N):

	filename = (f"LiteJumpingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	count_points = np.zeros((len(dataset)))
	matrixSaida = np.zeros((len(dataset),len(dataset)+1))
	matrix = np.zeros((len(dataset),len(dataset)+1))
	pontos_inconclusivos_int = np.zeros((len(dataset),len(dataset[0])))


	file1.write((title + "\n\n"))
	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))
		file1.write((arquivos[i] + ":" + " Média - " + str(round(media[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Desvio padrao - " + str(round(desvio[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Limite inferior - " + str(round(media[i] - desvio[i], 4)) + " | " + "Limite superior - " + str(round(media[i] + desvio[i], 4)) +"\n\n"))


	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range( 0, (len(dataset[i])), window_size): # array com n pontos
			conclusion = np.zeros((len(arquivos) + 1))
			count_points[i] += 1
			if (j + window_size <= len(dataset[i])):
				janela = dataset[i][j:j+window_size]

				for k in range(len(janela)):
					if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
						conclusion[0] += 1
						continue

					elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
						conclusion[1] += 1
						continue

					elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
						conclusion[2] += 1
						continue

					elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
						conclusion[3] += 1
						continue
					
					else:
						conclusion[4] += 1

			else:
				janela = dataset[i][j:]

				for k in range(len(janela)):
					if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
						conclusion[0] += 1
						continue

					elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
						conclusion[1] += 1
						continue

					elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
						conclusion[2] += 1
						continue

					elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
						conclusion[3] += 1
						continue
					
					else:
						conclusion[4] += 1
			
			matrix[i][np.argmax(conclusion)] += 1
			if( np.argmax(conclusion) == 4):
				pontos_inconclusivos_int[i][j] = dataset[i][j]
				

	file1.write(f"Matriz de confusao - Janela Pulante[{window_size}] - N{N} - Qtd de janelas{count_points}\n\n")
	file1.write((f"{'Arquivo':<10}"))
	for i in range(len(arquivos)):
		file1.write(f"{arquivos[i]:<10}")
	file1.write(f"{'Inconclusivo':<10}\n")

	for i in range(len(matrix)):
		file1.write(f"{arquivos[i]:<10}")
		for j in range(len(matrix[i])):
			# matrixSaida[i][j] = round(get_change_t(matrix[i][j],(count_points[i])),2 )		
			matrixSaida[i][j] = round(matrix[i][j],2 )
			file1.write(f"{matrixSaida[i][j]:<10}")
		file1.write("\n\n")


	file1.close()

def windowsPlot(dataset, arquivos, title, window_size, N):

	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	count_window_jumping = np.zeros((len(dataset)))
	count_window_sliding = np.zeros((len(dataset)))
	matrixJumping = np.zeros((len(dataset),len(dataset)+1))
	matrixSliding = np.zeros((len(dataset),len(dataset)+1))
	matrixJumpingSaida = np.zeros((len(dataset),len(dataset)+1))
	matrixSlidingSaida = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range( (len(dataset[i]) - window_size + 1) ): # array com n pontos
			janela = dataset[i][j:j+window_size]
			conclusion = np.zeros((len(arquivos) + 1))
			
			for k in range(len(janela)):
				if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
					conclusion[0] += 1
					continue

				elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
					conclusion[1] += 1
					continue

				elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
					conclusion[2] += 1
					continue

				elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
					conclusion[3] += 1
					continue
				
				else:
					conclusion[4] += 1
			
			if(j == (len(dataset[i]) - window_size)):
				matrixSliding[i][np.argmax(conclusion)] += 1 * window_size
				count_window_sliding[i] += 1 * window_size
			else:
				matrixSliding[i][np.argmax(conclusion)] += 1
				count_window_sliding[i] += 1

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range( 0, (len(dataset[i])), window_size): # array com n pontos
			conclusion = np.zeros((len(arquivos) + 1))
			count_window_jumping[i] += 1
			if (j + window_size <= len(dataset[i])):
				janela = dataset[i][j:j+window_size]

				for k in range(len(janela)):
					if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
						conclusion[0] += 1
						continue

					elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
						conclusion[1] += 1
						continue

					elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
						conclusion[2] += 1
						continue

					elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
						conclusion[3] += 1
						continue
					
					else:
						conclusion[4] += 1

			else:
				janela = dataset[i][j:]

				for k in range(len(janela)):
					if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
						conclusion[0] += 1
						continue

					elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
						conclusion[1] += 1
						continue

					elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
						conclusion[2] += 1
						continue

					elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
						conclusion[3] += 1
						continue
					
					else:
						conclusion[4] += 1
			
			matrixJumping[i][np.argmax(conclusion)] += 1

	for i in range(len(matrixJumping)):
		for j in range(len(matrixJumping[i])):
			matrixJumpingSaida[i][j] = round(get_change_t(matrixJumping[i][j],(count_window_jumping[i])),2 )	

	for i in range(len(matrixSliding)):
		for j in range(len(matrixSliding[i])):
			matrixSlidingSaida[i][j] = round(get_change_t(matrixSliding[i][j],count_window_sliding[i]),2)

	fig, ax = plt.subplots(len(dataset), 2)
	fig.suptitle(f"{title} - N{N}WindowSize{window_size}")

	labels = arquivos + ["Inconclusivo"]

	for j in range(len(dataset)):

		# # Gráfico de pizza para matrixSlidingSaida
		non_zero_values_sliding = [value for value in matrixSlidingSaida[j] if value != 0]
		non_zero_labels_sliding = [label for value, label in zip(matrixSlidingSaida[j], labels) if value != 0]
		wedges, texts, autotexts = ax[j][0].pie(non_zero_values_sliding, labels=non_zero_labels_sliding[:len(non_zero_values_sliding)], autopct='%1.1f%%', shadow=True, startangle=90)
		ax[j][0].set_title(f"Sliding window - {arquivos[j]}")
		ax[j][0].legend(wedges, non_zero_labels_sliding[:len(non_zero_values_sliding)], loc = "lower left", bbox_to_anchor=(1, 0, 0.5, 1))

		# Gráfico de pizza para matrixJumpingSaida
		non_zero_values_jumping = [value for value in matrixJumpingSaida[j] if value != 0]
		non_zero_labels_jumping = [label for value, label in zip(matrixJumpingSaida[j], labels) if value != 0]
		wedges, texts, autotexts = ax[j][1].pie(non_zero_values_jumping, labels=non_zero_labels_jumping[:len(non_zero_values_jumping)], autopct='%1.1f%%', shadow=True, startangle=90)
		ax[j][1].set_title(f"Jumping window - {arquivos[j]}")
		ax[j][1].legend(wedges, non_zero_labels_jumping[:len(non_zero_values_jumping)], loc = "lower left", bbox_to_anchor=(1, 0, 0.5, 1))


def confusionMatrixComparation(dataset, arquivos, title, N):

	media_metade = np.zeros((len(dataset)))
	desvio_metade = np.zeros((len(dataset)))
	matrix_metade = np.zeros((len(dataset),len(dataset)+1))
	media_completo = np.zeros((len(dataset)))
	desvio_completo = np.zeros((len(dataset)))
	matrix_completo = np.zeros((len(dataset),len(dataset)+1))

	filename = (f"confusionMatrixHalfTrainingN{N}.txt")
	half_file = open(filename, 'a+')
	filename = (f"confusionMatrixCompleteTrainingN{N}.txt")
	complete_file = open(filename, 'a+')

	half_file.write(f"{title} - N{N}\n\n")
	complete_file.write(f"{title} - N{N}\n\n")

	for i in range(len(dataset)):
		media_metade[i] = media_sac(dataset[i], 0, round(len(dataset[i])/2) )
		desvio_metade[i] = desvio_sac(dataset[i], 0, round(len(dataset[i])/2) )
		half_file.write((arquivos[i] + ":" + " Média - " + str(round(media_metade[i], 4)) + "\n"))
		half_file.write((arquivos[i] + ":" + " Desvio padrao - " + str(round(desvio_metade[i], 4)) + "\n"))
		half_file.write((arquivos[i] + ":" + " Limite inferior - " + str(round(media_metade[i] - desvio_metade[i], 4)) + " | " + "Limite superior - " + str(round(media_metade[i] + desvio_metade[i], 4)) +"\n\n"))

	for i in range(len(dataset)):
		media_completo[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio_completo[i] = desvio_sac(dataset[i], 0, len(dataset[i]))
		complete_file.write((arquivos[i] + ":" + " Média - " + str(round(media_completo[i], 4)) + "\n"))
		complete_file.write((arquivos[i] + ":" + " Desvio padrao - " + str(round(desvio_completo[i], 4)) + "\n"))
		complete_file.write((arquivos[i] + ":" + " Limite inferior - " + str(round(media_completo[i] - desvio_completo[i], 4)) + " | " + "Limite superior - " + str(round(media_completo[i] + desvio_completo[i], 4)) +"\n\n"))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		teste_dataset = amostragem_sac(dataset[i], (round((len(dataset[i])/2))), (len(dataset[i])))
		for j in range(round((len(dataset[i])/2))): # array com n pontos
			
			if (teste_dataset[j] >= media_metade[0] - desvio_metade[0] and teste_dataset[j] <= media_metade[0] + desvio_metade[0]):
				matrix_metade[i][0] += 1
				continue

			elif(teste_dataset[j] >= media_metade[1] - desvio_metade[1] and teste_dataset[j] <= media_metade[1] + desvio_metade[1]):
				matrix_metade[i][1] += 1
				continue

			elif(teste_dataset[j] >= media_metade[2] - desvio_metade[2] and teste_dataset[j] <= media_metade[2] + desvio_metade[2]):
				matrix_metade[i][2] += 1
				continue

			elif(teste_dataset[j] >= media_metade[3] - desvio_metade[3] and teste_dataset[j] <= media_metade[3] + desvio_metade[3]):
				matrix_metade[i][3] += 1
				continue
			
			else:
				matrix_metade[i][4] += 1

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range(len(dataset[i])): # array com n pontos
			
			if (dataset[i][j] >= media_completo[0] - desvio_completo[0] and dataset[i][j] <= media_completo[0] + desvio_completo[0]):
				matrix_completo[i][0] += 1
				continue

			elif(dataset[i][j] >= media_completo[1] - desvio_completo[1] and dataset[i][j] <= media_completo[1] + desvio_completo[1]):
				matrix_completo[i][1] += 1
				continue

			elif(dataset[i][j] >= media_completo[2] - desvio_completo[2] and dataset[i][j] <= media_completo[2] + desvio_completo[2]):
				matrix_completo[i][2] += 1
				continue

			elif(dataset[i][j] >= media_completo[3] - desvio_completo[3] and dataset[i][j] <= media_completo[3] + desvio_completo[3]):
				matrix_completo[i][3] += 1
				continue
			
			else:
				matrix_completo[i][4] += 1

	matrix_completo_saida = np.zeros((len(dataset),len(dataset)+1))
	matrix_metade_saida = np.zeros((len(dataset),len(dataset)+1))

	half_file.write(f"Matriz de confusao \n\n")
	half_file.write((f"{'Arquivo':<10}"))
	for i in range(len(arquivos)):
		half_file.write(f"{arquivos[i]:<10}")
	half_file.write(f"{'Inconclusivo':<10}\n")

	for i in range(len(matrix_metade)):
		half_file.write(f"{arquivos[i]:<10}")
		for j in range(len(matrix_metade[i])):
			matrix_metade[i][j] = round(matrix_metade[i][j],2)
			half_file.write(f"{matrix_metade[i][j]:<10}")
		half_file.write("\n\n")

	half_file.close()

	complete_file.write(f"Matriz de confusao \n\n")
	complete_file.write((f"{'Arquivo':<10}"))
	for i in range(len(arquivos)):
		complete_file.write(f"{arquivos[i]:<10}")
	complete_file.write(f"{'Inconclusivo':<10}\n")

	for i in range(len(matrix_completo)):
		complete_file.write(f"{arquivos[i]:<10}")
		for j in range(len(matrix_completo[i])):
			matrix_completo[i][j] = round(matrix_completo[i][j],2)
			complete_file.write(f"{matrix_completo[i][j]:<10}")
		complete_file.write("\n\n")

	complete_file.close()

	for i in range(len(dataset)):
		for j in range(len(matrix_completo[0])):
			matrix_completo_saida[i][j] = get_change_t(matrix_completo[i][j], len(dataset[i]))
			matrix_metade_saida[i][j] = get_change_t(matrix_metade[i][j], len(dataset[i]))
	
	fig, ax = plt.subplots(len(dataset), 2)
	fig.suptitle(f"{title} - N{N}")

	labels = arquivos + ["Inconclusivo"]

	for j in range(len(dataset)):

		# # Gráfico de pizza para matriz de confusão metade
		non_zero_values_half = [value for value in matrix_metade_saida[j] if value != 0]
		non_zero_labels_half = [label for value, label in zip(matrix_metade_saida[j], labels) if value != 0]
		wedges, texts, autotexts = ax[j][0].pie(non_zero_values_half, labels=non_zero_labels_half[:len(non_zero_values_half)], autopct='%1.1f%%', shadow=True, startangle=90)
		ax[j][0].set_title(f"Confusion matrix Half Training - {arquivos[j]}")
		ax[j][0].legend(wedges, non_zero_labels_half[:len(non_zero_values_half)], loc = "lower left", bbox_to_anchor=(1, 0, 0.5, 1))

		# Gráfico de pizza para matriz de confusão completo
		non_zero_values_full = [value for value in matrix_completo_saida[j] if value != 0]
		non_zero_labels_full = [label for value, label in zip(matrix_completo_saida[j], labels) if value != 0]
		wedges, texts, autotexts = ax[j][1].pie(non_zero_values_full, labels=non_zero_labels_full[:len(non_zero_values_full)], autopct='%1.1f%%', shadow=True, startangle=90)
		ax[j][1].set_title(f"Confusion matrix Full Training - {arquivos[j]}")
		ax[j][1].legend(wedges, non_zero_labels_full[:len(non_zero_values_full)], loc = "lower left", bbox_to_anchor=(1, 0, 0.5, 1))


def taxa_de_aquisicao(dataset, arquivo):
	timestamp_seg = np.zeros(len(dataset))
	for i in range(len(dataset)):
		aux = time.localtime(dataset[i])
		seg = (aux.tm_hour * 3600) + (aux.tm_min * 60) + aux.tm_sec
		timestamp_seg[i] = seg

	valores_unicos, contagens = np.unique(timestamp_seg, return_counts=True)

	amostras = {}

	for valor, contagem in zip(valores_unicos, contagens):
		amostras[valor] = np.full(contagem, valor)

	# for chave, array_separado in amostras.items():
	# 	print(f"{chave}: {len(array_separado)}")

	chaves = (list(amostras.keys()))
	chaves_int = [int(chave) for chave in chaves]

	amostras_plot = []
	amostras_media = []
	for i in range(chaves_int[0], chaves_int[-1]):
		if(i in chaves_int):
			amostras_plot.append(len(amostras[i]))
			if(len(amostras[i]) > 100):
				amostras_media.append(len(amostras[i]))
		else:
			amostras_plot.append(0)

	# print(f"Tamanho das amostras: {len(amostras_media)} Somatorio das amostras: {sum(amostras_media)}")
	taxa_aquisicao = ( sum(amostras_media) / len(amostras_media) )
	print(f"Taxa de aquisição do arquivo {arquivo}: {round(taxa_aquisicao, 2)} amostras por segundo")

	fig, ax = plt.subplots()

	ax.set_xlim(-5, len(amostras_plot))
	ax.set_xticks(range(0, len(amostras_plot), 30))
	ax.set(ylabel = "Amostras", xlabel = "Segundos", title = (f"Taxa de aquisição: Arquivo {arquivo} "))
	ax.plot(amostras_plot)