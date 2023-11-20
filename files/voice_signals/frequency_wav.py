#import numpy as np
#import matplotlib.pyplot as plt
#from scipy.io import wavfile
#from scipy.signal import spectrogram


#fs, data = wavfile.read('./data2/data/pac670/VGA670.wav')


#frequencies, times, spectrogram_data = spectrogram(data, fs)

# Plotando o espectrograma
#plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram_data), shading='auto')
#plt.ylabel('Frequência [Hz]')
#plt.xlabel('Tempo [s]')
#plt.title('Espectrograma')
#plt.colorbar(label='Intensidade [dB]')
#plt.show()

# Calculando o eixo de tempo
#time = np.arange(0, len(data)) / fs

# Plotando a forma de onda sonora
#plt.plot(time, data)
#plt.xlabel('Tempo (s)')
#plt.ylabel('Amplitude')
#plt.title('Forma de Onda Sonora')
#plt.show()



import librosa
import librosa.display
import numpy as np
import csv
import matplotlib.pyplot as plt

audio_file = './data2/data/pac670/VGA670.wav'
y, sr = librosa.load(audio_file)

# Extraindo características (por exemplo, energia média ao longo do tempo)
rms = librosa.feature.rms(y=y)

# Salvando as características em um arquivo CSV
csv_file = 'pac670t3.csv'
with open(csv_file, 'w', newline='') as file:
    #writer = csv.writer(file)

    for e in rms:
        file.write('\n'.join(map(str, e)))



