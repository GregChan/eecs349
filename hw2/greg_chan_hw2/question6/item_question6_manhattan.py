import sys, csv, scipy, numpy as np
from scipy.stats.stats import pearsonr
from scipy.stats import mode

try:
	cache = pickle.load(open("item_manhattan.p", "rb" ))
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

		movies = {}

		for row in filterSet:
			user = int(row[0])
			movie = int(row[1])
			rating = int(row[2])

			if not movie in movies:
				movies[movie] = [0] * (943 + 1)

			movies[movie][user] = rating

		k = 1
		errorSum = 0
		count = 0
		i = 0

		for triple in testSet:
			userID = triple[0]
			movieID = triple[1]
			rating = triple[2]
			nearestNeighbors = manhattan(movies, userID, movieID, k, i)
			predictedRating = predictedRatingFromNearestNeighbors(movies, userID, nearestNeighbors)
			percentError = (float(rating) - predictedRating) / float(rating)

			# print count, userID, predictedRating, percentError
			errorSum += percentError
			count = count + 1

		print errorSum / setSize

	pickle.dump(cache, open( "item_manhattan.p", "wb" ))

# returns the mode of the nearest neighbor's ratings of the movie
def predictedRatingFromNearestNeighbors(movies, userID, nearestNeighbors):
	ratings = []
	for neighbor in nearestNeighbors:
		ratings.append(movies[neighbor[0]][userID])

	return mode(ratings)[0][0]

def manhattan(movies, userID, movieID, k, i):
	results = []
	
	for movie in movies.keys():
		if movie != movieID:
			if i == 0 and movies[movie][userID] == 0:
				continue

			results.append((movie, manhattanDistance(movies, movieID, movie, movieID)))

	results.sort(key=lambda x: x[1],reverse=False)

	return results[:k]

def manhattanDistance(movies, movieIDA, movieIDB, movieID):
	usersA = movies[movieIDA]
	usersB = movies[movieIDB]

	distance = 0

	for i in range(1, len(usersA)):
		if i != movieID:
			distance += abs(usersA[i] - usersB[i])

	return distance

if __name__ == "__main__":
    main()



