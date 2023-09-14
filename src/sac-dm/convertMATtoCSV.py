import scipy.io
import numpy as np

file_path = "../../files/hexacopter_signals/mat/nominal_flight/NFlt05.mat"

file_name = "../../files/hexacopter_signals/csv/nominal_flight/NFlt05"
file = scipy.io.loadmat(file_path)


print(f"Tamanhos[n1] - Eixo X: {len(file['n1'][0][0][1][0])} Eixo Y: {len(file['n1'][0][0][2][0])} Eixo Z: {len(file['n1'][0][0][3][0]  )} Time: {len(file['n1'][0][0][0] )}")

file_csv = open( (file_name + "n1.csv"), "w")

for i in range(len(file['n1'][0][0][0])):
    file_csv.write(f"{file['n1'][0][0][1][0][i]} ; {file['n1'][0][0][2][0][i]} ; {file['n1'][0][0][3][0][i]} ; {file['n1'][0][0][0][i][0]}")
    if(i < (len(file['n1'][0][0][0]) - 1)):
        file_csv.write("\n")

file_csv.close()

print(f"Tamanhos[n2] - Eixo X: {len(file['n2'][0][0][1][0])} Eixo Y: {len(file['n2'][0][0][2][0])} Eixo Z: {len(file['n2'][0][0][3][0]  )} Time: {len(file['n2'][0][0][0] )}")

file_csv = open((file_name + "n2.csv"), "w")

for i in range(len(file['n2'][0][0][0])):
    file_csv.write(f"{file['n2'][0][0][1][0][i]} ; {file['n2'][0][0][2][0][i]} ; {file['n2'][0][0][3][0][i]} ; {file['n2'][0][0][0][i][0]}")
    if(i < (len(file['n2'][0][0][0]) - 1)):
        file_csv.write("\n")

file_csv.close()

print(f"Tamanhos[n3] - Eixo X: {len(file['n3'][0][0][4][0])} Eixo Y: {len(file['n3'][0][0][5][0])} Eixo Z: {len(file['n3'][0][0][6][0])} Time: {len(file['n3'][0][0][2])}")

file_csv = open((file_name + "n3.csv"), "w")

for i in range(len(file['n3'][0][0][4][0])):
    file_csv.write(f"{file['n3'][0][0][4][0][i]} ; {file['n3'][0][0][5][0][i]} ; {file['n3'][0][0][6][0][i]} ; {file['n3'][0][0][2][i]}")
    if(i < (len(file['n3'][0][0][0]) - 1)):
        file_csv.write("\n")

file_csv.close()
