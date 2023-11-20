import librosa
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import csv

caminho_arquivo = './data2/data/pac670/VGA670.wav'
sinal, taxa_amostragem = librosa.load(caminho_arquivo)

# Função para projetar um filtro passa-baixa
def butter_lowpass_filter(data, cutoff_frequency, sample_rate, order=4):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Definir a frequência de corte para o filtro passa-baixa
frequencia_corte = 1000  # em Hz

# Aplicar o filtro passa-baixa ao sinal de áudio
sinal_filtrado = butter_lowpass_filter(sinal, frequencia_corte, taxa_amostragem)


dados_csv = np.column_stack((sinal_filtrado))
caminho_saida_csv = 'saida_audio_filtrado.csv'


with open(caminho_saida_csv, 'w', newline='') as file:
    for e in dados_csv:
        file.write('\n'.join(map(str, e)))


# Exibir os sinais original e filtrado
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(np.arange(len(sinal)) / taxa_amostragem, sinal, label='Sinal Original')
plt.title('Sinal de Áudio Original')
plt.xlabel('Tempo (s)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(np.arange(len(sinal_filtrado)) / taxa_amostragem, sinal_filtrado, label='Sinal Filtrado')
plt.title(f'Sinal de Áudio Filtrado (Frequência de Corte: {frequencia_corte} Hz)')
plt.xlabel('Tempo (s)')
plt.legend()

plt.tight_layout()
plt.show()