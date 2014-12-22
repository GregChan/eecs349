import numpy as np

DOWN = 0
UP = 1
SAME = 2

size = 3
observation_dictionary = {'c': 0, 'o': 1, 't': 2}

sequence = ['c', 'c', 'c', 't', 't']

starting_probability = [0.3, 0.3, 0.4]
transition_probability = [[0.5, 0.2, 0.3], [0.5, 0.2, 0.3], [0.5, 0.2, 0.3]]
observation_probability = [[0.1, 0.5, 0.4], [0.5, 0.3, 0.2], [0.2, 0.2, 0.6]]

initial_values = [starting_probability[i] * observation_probability[i][observation_dictionary[sequence[0]]] for i in range(size)]

P = [[x for x in initial_values]]
a = transition_probability
b = observation_probability

t = 2
P_t = [0]
for i in range(0, size):
	# print b[i][observation_dictionary[sequence[t]]]
	# print a[i][0]
	# print P[t - 2][i]
	P_t[0] += P[t - 2][i] * a[i][0] * b[i][observation_dictionary[sequence[t - 1]]]
	

print P_t[0]
