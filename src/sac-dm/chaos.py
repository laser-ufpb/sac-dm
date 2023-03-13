import nolds
import autocorrelation as auto
#import sacdm as s
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import util


'''
λ > 0, {xn} shows chaotic behavior;
λ < 0, {xn} shows periodic behavior;
λ = 0, a bifurcation occurs.
'''

def lyapunov_e(data, N):
	i = 0
	j = N
	coef = []
	while j < len(data):
		coef.append(nolds.lyap_e(data[i:j]))
		print('Coeficientes ja calculados: ', i, len(coef))
		i = j
		j = j+N

	coef = np.reshape(coef, (-1))
	coef.flatten()
	return coef


def lyapunov_r(data, N):
	i = 0
	j = N
	coef = []
	while j < len(data):
		coef.append(nolds.lyap_r(data[i:j]))
		i = j
		j = j+N

	coef = np.reshape(coef, (-1))
	coef.flatten()
	return coef

def test():
	lm = nolds.logistic_map(0.1, 1000000, r=4)
	data = np.fromiter(lm, dtype="float32")

	print('Logistic map: ', data.shape)



	N = 100
	sac = s.sac_dm(data, N)
	am = s.sac_am(data, N)
	pm = s.sac_pm(data)
	wm = s.sac_wm(data)

	util.show(sac, am, 'SAC')

	corr = auto.autocorrelation(data, N)

	util.show(corr, corr, 'autocorrelation')



	#le = lyapunov_e(data[0:10000], 1000)
	lr = lyapunov_r(data[0:10000], N)

	#print (le.shape)
	print (lr.shape)

	util.show(lr, lr, 'lyapunov coef')

	l = max(le)

	print ('lyapunov max coef: ', l)

	return 1

#test()