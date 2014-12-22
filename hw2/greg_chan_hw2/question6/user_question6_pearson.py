import sys, csv, scipy, numpy as np
from scipy.stats import mode
from scipy.stats.stats import pearsonr
import pickle

try:
	cache = pickle.load(open("pearson.p", "rb" ))
except:
	print 'no cache'
	cache = {}

def main():
	setSize = 1000
	f = sys.argv[1]

	csvfile = open(f, 'rb')
	data = csv.reader(csvfile, delimiter='\t')

	triples = []

	for row in data:
		user = int(row[0])
		movie = int(row[1])
		rating = int(row[2])

		triples.append((user, movie, rating))

	# start loop
	for i in range(0, 100):
		start = i * 1000
		testSet = triples[start:start+setSize]
		filterSet = triples[start+setSize:] + triples[0:start]

		users = {}

		for row in filterSet:
			user = int(row[0])
			movie = int(row[1])
			rating = int(row[2])

			if not user in users:
				users[user] = [0] * (1682 + 1)

			users[user][movie] = rating

		# print testSet[:10]
		k = 100
		errorSum = 0
		count = 0
		i = 0

		for triple in testSet:
			userID = triple[0]
			movieID = triple[1]
			rating = triple[2]
			nearestNeighbors = pearson(users, userID, movieID, k, i)
			predictedRating = predictedRatingFromNearestNeighbors(users, movieID, nearestNeighbors)
			percentError = (float(rating) - predictedRating) / float(rating)

			# print count, userID, predictedRating, percentError
			errorSum += percentError
			count = count + 1

		print errorSum / setSize

	pickle.dump(cache, open( "pearson.p", "wb" ))

# returns the mode of the nearest neighbor's ratings of the movie
def predictedRatingFromNearestNeighbors(users, movieID, nearestNeighbors):
	ratings = []
	for neighbor in nearestNeighbors:
		ratings.append(users[neighbor[0]][movieID])

	return mode(ratings)[0][0]

# returns the k nearest neighbors of userID as a list of tuples of userIDs and the pearson distance
def pearson(users, userID, movieID, k, i):
	results = []

	for user in users.keys():
		if user != userID:
			if i == 0 and users[user][movieID] == 0:
				continue

			# check cache if it doesn't exist then compute
			key = [userID, user, movieID]
			key.sort()
			key = tuple(key)
			if key in cache:
				results.append((user, cache[key]))
			else:
				distance = pearsonCorrelationDistance(users, userID, user, movieID)
				cache[key] = distance
				results.append((user, distance))

	results.sort(key=lambda x: x[1],reverse=True)

	# prune negatively or not correlated results
	prunedResults = []
	for r in results[:k]:
		if r[1] > 0:
			prunedResults.append(r)

	return prunedResults

# returns the pearson correlation distance between two users, userIDA, and userIDB this distance excludes movieID
def pearsonCorrelationDistance(users, userIDA, userIDB, movieID):
	moviesA = list(users[userIDA])
	moviesB = list(users[userIDB])

	del moviesA[movieID]
	del moviesB[movieID]

	return pearsonr(moviesA[1:], moviesB[1:])[0]

if __name__ == "__main__":
    main()