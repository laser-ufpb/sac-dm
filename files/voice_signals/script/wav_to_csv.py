import wave
import csv
import struct

def wav_to_csv(input_wav_file, output_csv_file):
    # Abrir o arquivo WAV para leitura
    with wave.open(input_wav_file, 'rb') as wav_file:
        # Obter os parâmetros do arquivo WAV
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Ler os dados do arquivo WAV
        frames = wav_file.readframes(num_frames)



        # Converter os dados binários para uma lista de valores
        data = list(struct.unpack_from(f"{num_frames * num_channels}h", frames))

    # Escrever os valores no arquivo CSV
    with open(output_csv_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Escrever os dados
        for i in range(0, num_frames * num_channels, num_channels):
            row_data = data[i:i + num_channels]
            if any(row_data):  # Verifica se pelo menos um valor é diferente de zero
                csv_writer.writerow(row_data)




input_wav_file = '/Users/Raul/Documents/GitHub/sac-dm/files/voice_signals/sample/original/sf01.wav'
output_csv_file = '/Users/Raul/Documents/GitHub/sac-dm/files/voice_signals/sample/data/sf01.csv'
wav_to_csv(input_wav_file, output_csv_file)

