import csv
import numpy as np
from matplotlib import pyplot as plt
import scipy.stats

def gmmest(X,mu_init,sigmasq_init,wt_init,its):
	L = []

	for it in range(its):
		for j in range(len(mu_init)):
			little_gamma = []
			big_gamma = 0

			for x_n in X:
				N = gaussian(x_n, mu_init[j], sigmasq_init[j])

				denominator = 0

				for k in range(len(mu_init)):
					
					denominator += wt_init[k] * gaussian(x_n, mu_init[k], sigmasq_init[k])
				if denominator == 0:
					little_gamma.append(0)
				else:
					little_gamma.append(wt_init[j] * N / denominator)

			big_gamma = np.sum(little_gamma)

			wt_init[j] = big_gamma / len(X)
			mu_init[j] = np.dot(little_gamma, X) / big_gamma

			sigNumerator = np.dot(little_gamma, [(x - mu_init[j])**2 for x in X])
			sigmasq_init[j] = sigNumerator/big_gamma

		l = 0

		for x in X:
			temp = 0
			for k in range(len(mu_init)):
				# temp += wt_init[k] * gaussian(x, mu_init[k], sigmasq_init[k])
				temp += wt_init[k] * scipy.stats.norm(mu_init[k], np.sqrt(sigmasq_init[k])).pdf(x)

			l += np.log(temp)

		L.append(l)

	return mu_init, sigmasq_init, wt_init, L

def gmmclassify(X, mu1, sigmasq1, wt1, mu2, sigmasq2, wt2, p1):
	classification = []
	for x in X:
		maxProbability1 = float('-inf')
		maxProbability2 = float('-inf')

		for i in range(len(mu1)):
			maxProbability1 = max(wt1[i] * gaussian(x, mu1[i], sigmasq1[i]), maxProbability1)

		for i in range(len(mu2)):
			maxProbability2 = max(wt2[i] * gaussian(x, mu2[i], sigmasq2[i]), maxProbability2)

		if maxProbability1 > maxProbability2:
			classification.append(1)
		else:
			classification.append(2)

	return classification

def gaussian(x, mu, sigmasq):
	# return np.exp(-((x-mu)**2)/(2*sigmasq))/(np.sqrt(2*np.pi)*np.sqrt(sigmasq))
	return scipy.stats.norm(mu, np.sqrt(sigmasq)).pdf(x)

def read_data(file_name):
	csvfile = open(file_name, 'rb')
	data = csv.reader(csvfile, delimiter=',')

	X = []
	Y = []

	for row in data:
		try:
			X.append(float(row[0]))
			Y.append(int(row[1]))
		except:
			pass

	return np.array(X), np.array(Y)

def main():
	X_test, Y_test = read_data('gmm_test.csv')
	X_train, Y_train = read_data('gmm_train.csv')

	class1 = X_train[np.nonzero(Y_train == 1)[0]]
	class2 = X_train[np.nonzero(Y_train == 2)[0]] 
	bins = 50

	# visualize class 1 and class 2 separately 
	plt.hist(class1, bins, alpha=0.5, label='Class 1', normed=True)
	plt.hist(class2, bins, alpha=0.5, label='Class 2', normed=True)
	plt.show()

	# get trained gaussians
	mu_init = [10,30]
	sigmasq_init = [1,1]
	wt_init = [.5,.5]
	its = 20

	mu1, sigmasq1, wt1, L1 = gmmest(class1, mu_init, sigmasq_init, wt_init, its)

	print 'means of model 1: ' + str(mu1)
	print 'variance of model 1: ' + str(sigmasq1)
	print 'weights of model 1: ' + str(wt1)

	plt.plot(L1)
	plt.show()

	# get trained gaussians
	mu_init = [-25,-6,50]
	sigmasq_init = [1,1,1]
	wt_init = [.33,.33,.33]
	its = 20

	mu2, sigmasq2, wt2, L2 = gmmest(class2, mu_init, sigmasq_init, wt_init, its)

	print 'means of model 2: ' + str(mu2)
	print 'variance of model 2: ' + str(sigmasq2)
	print 'weights of model 2: ' + str(wt2)

	plt.plot(L2)
	plt.show()

	p1 = len(class1/len(X_train))

	print 'prior probability: ' + str(p1)

	classification = gmmclassify(X_test, mu1, sigmasq1, wt1, mu2, sigmasq2, wt2, p1)

	class1 = X_test[np.nonzero(Y_test == 1)[0]]
	class2 = X_test[np.nonzero(Y_test == 2)[0]] 
	
	plt.scatter(X_test,[0.06] * len(X_test),c=classification,alpha=0.3)
	plt.hist(class1, bins, alpha=0.5, label='Class 1', normed=True)
	plt.hist(class2, bins, alpha=0.5, label='Class 2', normed=True)
	plt.show()

	correct = 0

	for i in range(len(classification)):
		if classification[i] == Y_test[i]:
			correct += 1

	print float(correct) / len(Y_test)
	
if __name__ == "__main__":
	main()