import numpy as np
import librosa
import csv


audios = ['VGA6-denoizado','VGA239-denoizado', 'VGA240-denoizado','VGA266-denoizado','VGA484-denoizado','original-denoizado','fundo-denoizado']

for i in range(len(audios)):
    caminho_audio = '../../files/voice_signals/vogal-sustentada/'+audios[i]+'.wav'


    sinal, taxa_amostragem = librosa.load(caminho_audio)

    # Excluir valores iguais a 0.0
    sinal_sem_zeros = [valor for valor in sinal if valor != 0.0]
    #caminho_saida_csv = 'audio_1.csv'
    caminho_saida_csv = audios[i]+'_.csv'

    # Salvar os dados em um arquivo CSV
    with open(caminho_saida_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[valor] for valor in sinal_sem_zeros])

