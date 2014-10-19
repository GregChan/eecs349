import sys
import csv
import numpy as np
import scipy

def perceptrona(w_init, X, Y):
	#figure out (w, k) and return them here. w is the vector of weights, k is how many iterations it took to converge.
	b = 0
	e = 0
	k = 0
	m = len(X)
	w = 0
	mistake = True

	while mistake:
		mistake = False
		for i in range(len(X)):
			if Y[i] != classify(X[i], w, b):
				w = w + Y[i] * X[i]
				b = b + Y[i]
				k = k + 1
				mistake = True
		e = e + 1
	print w, b, e
	# check_weight_vector(X, w, b)
	return (w, e)

def classify(x, w, b):
	test_value = w * x + b
	if test_value > 0:
		return 1
	else:
		return -1

def check_weight_vector(X, w, b):
	for i in range(len(X)):
		print X[i], classify(X[i], w, b)

def main():
	rfile = sys.argv[1]
	
	#read in csv file into np.arrays X1, X2, Y1, Y2
	csvfile = open(rfile, 'rb')
	dat = csv.reader(csvfile, delimiter=',')
	X1 = []
	Y1 = []
	X2 = []
	Y2 = []
	for i, row in enumerate(dat):
		if i > 0:
			X1.append(float(row[0]))
			X2.append(float(row[1]))
			Y1.append(float(row[2]))
			Y2.append(float(row[3]))
	X1 = np.array(X1)
	X2 = np.array(X2)
	Y1 = np.array(Y1)
	Y2 = np.array(Y2)
	w_init = [0, 0]# INTIALIZE W_INIT
	print perceptrona(w_init, X1, Y1)
	print perceptrona(w_init, X2, Y2)

if __name__ == "__main__":
	main()
