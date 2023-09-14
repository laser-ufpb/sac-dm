import scipy.io
import numpy as np

file_path = "../../files/hexacopter_signals/mat/nominal_flight/NFlt01.mat"

file = scipy.io.loadmat(file_path)

# file['n1'][0][0][0] - lista time vector
# file['n1'][0][0][1][0] - lista eixo x
# file['n1'][0][0][2][0] - lista eixo y
# file['n1'][0][0][3][0] - lista eixo z
# print(len(file['n1'][0][0][0] ))
# print(len(file['n1'][0][0][1][0]  ))
# print(len(file['n1'][0][0][2][0]  ))
# print(len(file['n1'][0][0][3][0]  ))


# file_csv = open("../../files/hexacopter_signals/nominal_flight/NFlt01-n1.csv", "w")

# for i in range(len(file['n1'][0][0][0])):
#     file_csv.write(f"{file['n1'][0][0][1][0][i]} ; {file['n1'][0][0][2][0][i]} ; {file['n1'][0][0][3][0][i]} ; {file['n1'][0][0][0][i][0]}")
#     if(i < (len(file['n1'][0][0][0]) - 1)):
#         file_csv.write("\n")

# file_csv.close()

# print(len(file['n2'][0][0][0] ))
# print(len(file['n2'][0][0][1][0]  ))
# print(len(file['n2'][0][0][2][0]  ))
# print(len(file['n2'][0][0][3][0]  ))

# file_csv = open("../../files/hexacopter_signals/nominal_flight/NFlt01-n2.csv", "w")

# for i in range(len(file['n2'][0][0][0])):
#     file_csv.write(f"{file['n2'][0][0][1][0][i]} ; {file['n2'][0][0][2][0][i]} ; {file['n2'][0][0][3][0][i]} ; {file['n2'][0][0][0][i][0]}")
#     if(i < (len(file['n2'][0][0][0]) - 1)):
#         file_csv.write("\n")

# file_csv.close()

print(len(file['n3'][0][0][0][0] ))
print((file['n3'][0][0][1] ))
# print(len(file['n3'][0][0][2][0]  ))
# print(len(file['n3'][0][0][3][0]  ))

# file_csv = open("../../files/hexacopter_signals/nominal_flight/NFlt01-n3.csv", "w")

# for i in range(len(file['n3'][0][0][0])):
#     file_csv.write(f"{file['n3'][0][0][1][0][i]} ; {file['n3'][0][0][2][0][i]} ; {file['n3'][0][0][3][0][i]} ; {file['n3'][0][0][0][i][0]}")
#     if(i < (len(file['n3'][0][0][0]) - 1)):
#         file_csv.write("\n")

# file_csv.close()
