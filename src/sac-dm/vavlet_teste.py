
from scipy.io import wavfile
import numpy as np
from pywt import wavedec, waverec
import soundfile as sf


def soft_thresholding(x, threshold):
    return np.sign(x) * np.maximum(np.abs(x) - threshold, 0.0)

def wavelet_denoise(signal, wavelet='db6', level=1, threshold=0.2):
    # Aplica a transformada discreta de wavelet
    coeffs = wavedec(signal, wavelet, level=level)

    # Aplica soft thresholding nos coeficientes de detalhes
    denoised_coeffs = [soft_thresholding(detail, threshold) for detail in coeffs[1:]]

    # Reconstroi o sinal denoised a partir dos coeficientes denoised e do coeficiente de aproximação original
    denoised_signal = waverec([coeffs[0]] + denoised_coeffs, wavelet)
    return denoised_signal
   

audios = ['VGA6','VGA239', 'VGA240','VGA266','VGA484','original','fundo']

for i in range(len(audios)):

    original_signal, sr = sf.read('../../files/voice_signals/vogal-sustentada/'+audios[i]+'.wav')

    denoised_signal = wavelet_denoise(original_signal, wavelet='db6', level=11, threshold=0.2)
    output_file_path = audios[i]+'-denoizado.wav'
    sf.write(output_file_path, denoised_signal, sr)


    print(f'Sinal denoizado salvo')

    

