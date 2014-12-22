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

	users = {}

	for row in data:
		user = int(row[0])
		movie = int(row[1])
		rating = int(row[2])
		
		if not user in users:
			users[user] = [0] * (1682 + 1)

		users[user][movie] = rating

	if distance == 0:
		nearestNeighbors = pearson(users, userID, movieID, k, i)
	elif distance == 1:
		nearestNeighbors = manhattan(users, userID, movieID, k, i)

	predictedRating = predictedRatingFromNearestNeighbors(users, movieID, nearestNeighbors)

	print 'userID %d	movieID: %d	trueRating: %d	predictedRating: %f	distance: %d	k: %d	i: %d' % (userID, movieID, users[userID][movieID], predictedRating, distance, k, i)

# returns the mode of the nearest neighbor's ratings of the movie
def predictedRatingFromNearestNeighbors(users, movieID, nearestNeighbors):
	ratings = []
	for neighbor in nearestNeighbors:
		ratings.append(users[neighbor[0]][movieID])

	return mode(ratings)[0][0]

# returns the k nearest neighbors of userID as a list of tuples of userIDs and the manhattan distance
def manhattan(users, userID, movieID, k, i):
	results = []
	
	for user in users.keys():
		if user != userID:
			if i == 0 and users[user][movieID] == 0:
				continue
			
			results.append((user, manhattanDistance(users, userID, user, movieID)))

	results.sort(key=lambda x: x[1],reverse=False)

	return results[:k]

# returns the manhattan distance between two users, userIDA and userIDB this distance excludes the movieID
def manhattanDistance(users, userIDA, userIDB, movieID):
	moviesA = users[userIDA]
	moviesB = users[userIDB]

	distance = 0

	for i in range(1, len(moviesA)):
		if i != movieID:
			distance += abs(moviesA[i] - moviesB[i])

	return distance

# returns the k nearest neighbors of userID as a list of tuples of userIDs and the pearson distance
def pearson(users, userID, movieID, k, i):
	results = []

	for user in users.keys():
		if user != userID:
			if i == 0 and users[user][movieID] == 0:
				continue

			results.append((user, pearsonCorrelationDistance(users, userID, user, movieID)))

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



