#pip install pywavelets

import wave
import numpy as np
import pywt
import matplotlib.pyplot as pltcd
from scipy import signal


# Wavelet
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)
    return audio_data, params

def write_wav(file_path, audio_data, params):
    with wave.open(file_path, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(audio_data.tobytes())

def wavelet_denoise(input_wav_file, output_wav_file, wavelet='db1', level=1):
    # Ler o arquivo WAV
    audio_data, params = read_wav(input_wav_file)

    # Aplicar a transformada discreta de wavelet (DWT)
    coeffs = pywt.wavedec(audio_data, wavelet, level=level)

    # Aplicar a denoização
    threshold = 20  # Ajuste o valor do limiar conforme necessário
    coeffs_thresholded = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]

    # Reconstruir o sinal após a denoização
    audio_denoised = pywt.waverec(coeffs_thresholded, wavelet)

    # Converter os valores para int16 antes de salvar o arquivo
    audio_denoised = audio_denoised.astype(np.int16)

    # Salvar o sinal denoizado como um novo arquivo WAV
    write_wav(output_wav_file, audio_denoised, params)


input_wav_file = '/Users/Raul/Documents/GitHub/sac-dm/files/voice_signals/sample/original/f01.wav'
output_wav_file = '/Users/Raul/Documents/GitHub/sac-dm/files/voice_signals/sample/denoised/f01_denoised.wav'
wavelet_denoise(input_wav_file, output_wav_file)



# Filtro passa-baixa
def apply_lowpass_filter(input_wav_file, output_wav_file, cutoff_frequency=1000, sampling_rate=44100):
    # Ler o arquivo WAV
    with wave.open(input_wav_file, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)

    # Definir os parâmetros do filtro passa-baixa
    nyquist_frequency = 0.5 * sampling_rate
    normalized_cutoff_frequency = cutoff_frequency / nyquist_frequency
    b, a = signal.butter(4, normalized_cutoff_frequency, btype='low', analog=False)

    # Aplicar o filtro ao sinal de áudio
    filtered_audio = signal.lfilter(b, a, audio_data)

    # Converter os valores para int16 antes de salvar o arquivo
    filtered_audio = filtered_audio.astype(np.int16)

    # Salvar o sinal filtrado como um novo arquivo WAV
    with wave.open(output_wav_file, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(filtered_audio.tobytes())

# Exemplo de uso
#input_wav_file = '/home/pesquisador/Documentos/sac-dm/files/voice_signals/sample/original/galvao_ia.wav'
#output_wav_file = '/home/pesquisador/Documentos/sac-dm/files/voice_signals/sample/high-pass/galvao_ia_hp.wav'
#apply_lowpass_filter(input_wav_file, output_wav_file, cutoff_frequency=2000)

