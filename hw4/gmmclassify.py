import csv
import numpy as np
from matplotlib import pyplot as plt
from gmmest import *




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
	

