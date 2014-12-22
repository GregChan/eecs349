import sys, csv, scipy, numpy as np
from scipy.stats.stats import pearsonr
from scipy.stats import mode

# reads the specified csv and takes in and casts the arguments
def main():
	f = sys.argv[1]
	userID = int(sys.argv[2])
	movieID = int(sys.argv[3])
	distance = int(sys.argv[4])
	k = int(sys.argv[5])
	i = int(sys.argv[6])

	csvfile = open(f, 'rb')
	data = csv.reader(csvfile, delimiter='\t')

	movies = {}

	for row in data:
		user = int(row[0])
		movie = int(row[1])
		rating = int(row[2])
		
		if not movie in movies:
			movies[movie] = [0] * (943 + 1)

		movies[movie][user] = rating

	# print manhattanDistance(movies, 4, 1, 4)

	if distance == 0:
		nearestNeighbors = pearson(movies, userID, movieID, k, i)
	elif distance == 1:
		nearestNeighbors = manhattan(movies, userID, movieID, k, i)
	# print nearestNeighbors
	
	predictedRating = predictedRatingFromNearestNeighbors(movies, userID, nearestNeighbors)

	print 'userID %d	movieID: %d	trueRating: %d	predictedRating: %f	distance: %d	k: %d	i: %d' % (userID, movieID, movies[movieID][userID], predictedRating, distance, k, i)

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

def pearson(movies, userID, movieID, k, i):
	results = []

	for movie in movies.keys():
		if movie != movieID:
			if i == 0 and movies[movie][userID] == 0:
				continue

			results.append((movie, pearsonCorrelationDistance(movies, movieID, movie, userID)))

	results.sort(key=lambda x: x[1],reverse=True)
	return results[:k]

def pearsonCorrelationDistance(movies, movieIDA, movieIDB, userID):
	usersA = list(movies[movieIDA])
	usersB = list(movies[movieIDB])

	del usersA[userID]
	del usersB[userID]

	return pearsonr(usersA[1:], usersB[1:])[0]

if __name__ == "__main__":
    main()



