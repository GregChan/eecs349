#	Starter code for linear regression problem
#	Below are all the modules that you'll need to have working to complete this problem
#	Some helpful functions: np.polyfit, scipy.polyval, zip, np.random.shuffle, np.argmin, np.sum, plt.boxplot, plt.subplot, plt.figure, plt.title
import sys
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt

def nfoldpolyfit(X, Y, maxK, n, verbose):
#	NFOLDPOLYFIT Fit polynomial of the best degree to data.
#   NFOLDPOLYFIT(X,Y,maxDegree, nFold, verbose) finds and returns the coefficients 
#   of a polynomial P(X) of a degree between 1 and N that fits the data Y 
#   best in a least-squares sense, averaged over nFold trials of cross validation.
#
#   P is a vector (in numpy) of length N+1 containing the polynomial coefficients in
#   descending powers, P(1)*X^N + P(2)*X^(N-1) +...+ P(N)*X + P(N+1). use
#   numpy.polyval(P,Z) for some vector of input Z to see the output.
#
#   X and Y are vectors of datapoints specifying  input (X) and output (Y)
#   of the function to be learned. Class support for inputs X,Y: 
#   float, double, single
#
#   maxDegree is the highest degree polynomial to be tried. For example, if
#   maxDegree = 3, then polynomials of degree 0, 1, 2, 3 would be tried.
#
#   nFold sets the number of folds in nfold cross validation when finding
#   the best polynomial. Data is split into n parts and the polynomial is run n
#   times for each degree: testing on 1/n data points and training on the
#   rest.
#
#   verbose, if set to 1 shows mean squared error as a function of the 
#   degrees of the polynomial on one plot, and displays the fit of the best
#   polynomial to the data in a second plot.
#   
#
#   AUTHOR: Greg Chan
#
	length = len(X)
	validationSetSize = len(X) / n

	scatterPlotX = []
	scatterPlotY = []

	lowestMSE = sys.maxint
	coefficients = []
	kValue = 0
	meanMSEK = {}
	medianMSEK = {}
	stdMSEK = {}

	for k in range(0, maxK + 1):
		MSEK = []
		for i in range(n):
			validationSetX = X[i*validationSetSize:i*validationSetSize+validationSetSize]
			validationSetY = Y[i*validationSetSize:i*validationSetSize+validationSetSize]

			trainingSetX = [X[0:i*validationSetSize], X[i*validationSetSize+validationSetSize:]]
			trainingSetX = [item for sublist in trainingSetX for item in sublist]

			trainingSetY = [Y[0:i*validationSetSize], Y[i*validationSetSize+validationSetSize:]]
			trainingSetY = [item for sublist in trainingSetY for item in sublist]

			P = np.polyfit(trainingSetX, trainingSetY, k)
			Z = np.polyval(P, validationSetX)
			
			MSE = np.subtract(Z, validationSetY)
			MSE = np.multiply(MSE, MSE)
			MSE = np.average(MSE)

			MSEK.append(MSE)

			scatterPlotX.append(k)
			scatterPlotY.append(MSE)

			if MSE < lowestMSE:
				lowestMSE = MSE
				coefficients = P
				kValue = k

		stdMSEK[k] = np.std(MSEK)
		medianMSEK[k] = np.median(MSEK)
		meanMSEK[k] = np.average(MSEK)

	if verbose == 1:
		plt.xlim([-1, 10])
		plt.ylim([-1, 3])
		plt.plot(scatterPlotX, scatterPlotY, '.', meanMSEK.keys(), meanMSEK.values(), 'x')
		plt.xlabel('k')
		plt.ylabel('MSE')
		plt.savefig('question1a1.png')
		plt.show()

		print stdMSEK
		print 'Lowest MSE: %d' % lowestMSE
		print 'Coefficients of the polynomial with the lowest MSE: ' + str(coefficients)
		print 'Degree of the polynomial with the lowest MSE: %d' % kValue

		p = np.poly1d(coefficients)
		xp = np.linspace(-1, 1)
		plt.plot(X, Y, '.', xp, p(xp), '-')
		plt.xlabel('x (input)')
		plt.ylabel('y (response)')
		plt.savefig('question1a2.png')
		plt.show()

	return coefficients

def main():
	# read in system arguments, first the csv file, max degree fit, number of folds, verbose
	rfile = sys.argv[1]
	maxK = int(sys.argv[2])
	nFolds = int(sys.argv[3])
	verbose = int(sys.argv[4])
	
	csvfile = open(rfile, 'rb')
	dat = csv.reader(csvfile, delimiter=',')
	X = []
	Y = []
	# put the x coordinates in the list X, the y coordinates in the list Y
	for i, row in enumerate(dat):
		if i > 0:
			X.append(float(row[0]))
			Y.append(float(row[1]))
	X = np.array(X)
	Y = np.array(Y)
	print nfoldpolyfit(X, Y, maxK, nFolds, verbose)

if __name__ == "__main__":
	main()
