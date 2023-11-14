import csv
from scipy.io import wavfile

samplerate, data = wavfile.read('pac002__tarefa1.wav')
dados = []
dado = ''
nome_arquivo = "teste.csv"

# Selecionar os dados da voz até a primeira pausa
for i in range(len(data)-1):
    if (data[i] == 0 and data[i+1] == 0):
        break
    else:
        dado = str(data[i]) + ";"
        dado = dado.replace(",","")
        
        dados.append(dado)


print(dados)
# Abrir o arquivo CSV para escrita
with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    # Escrever os dados no arquivo CSV
    escritor_csv.writerow(dados)
print(f'Os dados foram salvos em {nome_arquivo}')
