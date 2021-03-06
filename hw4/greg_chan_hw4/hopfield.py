import csv
import numpy as np
from matplotlib import pyplot as plt
import random

def train_hopfield(X):
	# Creates a set of weights between nodes in a Hopfield network whose
	# size is based on the length of the rows in the input data X.

	# X is a numpy.array of shape (R, C). Values in X are drawn from
	# {+1,-1}. Each row is a single training example. So X(3,:) would be
	# the 3rd training example. %
	# W is a C by C numpy array of weights, where W(a,b) is the connection
	# weight between nodes a and b in the Hopfield net after training.
	# Here, C = number of nodes in the net = number of columns in X
	# return W
	C = len(X[0])
	R = len(X)
	W = [[0 for z in range(C)] for z in range(C)]

	for i in range(C):
		for j in range(C):
			if i == j:
				W[i][j] = 0
			else:
				W[i][j] = 0
				for r in range(R):
					W[i][j] += X[r][i] * X[r][j]

	return np.array(W)

def classify(x, w):
	if np.dot(x, w) >= 0:
		return 1
	else:
		return -1

def display_vector_as_image(image):
	plt.imshow(np.reshape(image, (16, 16)), interpolation="nearest")
	plt.show()

def use_hopfield(W,x):
	# Takes a Hopfield net W and an input vector x and runs the
	# Hopfield network until it converges.
	# x, the input vector, is a numpy vector of length C (where
	# the number of nodes in the net). This is a set of
	# activation values drawn from the set {+1, -1}
	# W is a C by C numpy array of weights, where W(a,b) is the
	# weight between nodes a and b in the Hopfield net.
	# Here, C = number of nodes in the net.
	# s is a numpy vector of length C (number of nodes in the net)
	# containing the final activation of the net. It is the result of
	# giving x to the net as input and then running until convergence.
	# return s

	update_order_indices = range(len(x))
	np.random.shuffle(update_order_indices)

	s = np.copy(x)
	e = 0
	mistake = True

	while mistake or e > 10:
		mistake = 0

		display_vector_as_image(s)

		for i in update_order_indices:
			update_value = classify(s, W[i])
			if update_value != s[i]:
				s[i] = update_value
				mistake += 1

		print 'mistakes: ' + str(mistake)

		e = e + 1

	return s

def fix_data(x):
	x = int(float(x))
	if x == 0:
		return -1
	else:
		return 1

def read_data(file_name):
	csvfile = open(file_name, 'rb')
	data = csv.reader(csvfile, delimiter=' ')

	X = []

	for row in data:
		row = map(fix_data, row[:-1])
		label = row[-10:].index(1)
		X.append((row[:-10], label))

	return X

def question1C(X):
	training_examples = []
	testing_examples = []
	used_indices = []

	# get training examples
	label = 0
	for i in range(len(X)):
		if label == X[i][1] and label < 5:
			training_examples.append(X[i][0])
			label += 1
			used_indices.append(i)

	# get test examples
	label = 0
	for i in range(len(X)):
		if label == X[i][1] and label < 5 and i not in used_indices:
			testing_examples.append(X[i][0])
			label += 1
	
	# train hopfield net
	training_examples = np.array(training_examples)
	W = train_hopfield(training_examples)

	# use hopfield net
	testing_examples = np.array(testing_examples)
	s = use_hopfield(W, testing_examples[2])

def question1D(X):
	training_examples = []
	testing_examples = []
	used_indices = []

	# get training examples
	label = 0
	for i in range(len(X)):
		if label == X[i][1] and label < 10:
			training_examples.append(X[i][0])
			label += 1
			used_indices.append(i)

	# get test examples
	# label = 0
	# for i in range(len(X)):
	# 	if label == X[i][1] and label < 5 and i not in used_indices:
	# 		testing_examples.append(X[i][0])
	# 		label += 1
	digit_index_offset = 3

	for i in used_indices:
		testing_examples.append(X[i + digit_index_offset][0])
	
	# train hopfield net
	training_examples = np.array([testing_examples[5], testing_examples[6]])
	W = train_hopfield(training_examples)

	# use hopfield net
	testing_examples = np.array(testing_examples)
	display_vector_as_image(training_examples[0])
	s = use_hopfield(W, add_noise(training_examples[0], 0.2))

def add_noise(testing_example, percent):
	noise_indices = []
	while len(noise_indices) < (len(testing_example) * percent):
		index = random.randint(0, len(testing_example) - 1)
		if index not in noise_indices:
			testing_example[index] *= -1
			noise_indices.append(index)

	return testing_example

def main():
	X = read_data("semeion.data")
	# question1C(X)
	question1D(X)
	
if __name__ == "__main__":
	main()