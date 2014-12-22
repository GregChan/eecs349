import sys
import csv
import numpy as np
import scipy
# http://www.stat.cmu.edu/~cshalizi/350/lectures/25/lecture-25.pdf
def perceptrona(w_init, X, Y):
	#figure out (w, e) and return them here. w is the vector of weights, e is how many iterations it took to converge.
	w = np.array(w_init)
	e = 0
	mistake = True

	while mistake:
		mistake = False

		for k in range(len(X)):
			x = np.array(X[k])
			x = np.append(x, 1.0)

			if classify(x, w) != Y[k]:
				w = np.add(w, np.multiply(x, Y[k]))
				mistake = True

		e = e + 1
	return (w, e)

def classify(x, w):
	if np.dot(x, w) > 0:
		return 1
	else:
		return -1

def square(X):
	result = []
	for value in X:
		result.append([value, value * value])
	result = np.array(result)
	X = result
	return result

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
	w_init = [0, 0, 0]# INTIALIZE W_INIT
	X2 = square(X2)
	
	print perceptrona(w_init, X2, Y2)

if __name__ == "__main__":
	main()
