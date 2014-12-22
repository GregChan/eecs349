import csv
import scipy
import numpy as np
import matplotlib.pyplot as plt

def main():
	csvfile = open('ml-100k/u.data', 'rb')
	data = csv.reader(csvfile, delimiter='\t')

	users = {}
	movies = {}

	for row in data:
		user = int(row[0])
		movie = int(row[1])
		rating = int(row[2])
		if not user in users:
			users[user] = {}

		if not movie in movies:
			movies[movie] = {}

		users[user][movie] = rating
		movies[movie][user] = rating

	question3a(users)
	question3b(movies)

def question3a(users):
	usersWithCommonRatingsAndMovies = []
	usersWithCommonMovies = []

	for i in range(1, len(users) + 1):
		movieIDs = users[i].keys()
		userAMovies = users[i]
		for j in range(i + 1, len(users) + 1):
			# movies both users have in common
			usersWithCommonMovies.append(len(set(users[i].keys()).intersection(set(users[j].keys()))))

			# movies both users have in common and the ratings are the same
			usersWithCommonRatingsAndMovies.append(0)
			userBMovies = users[j]
			for movie in movieIDs:
				try:
					if userAMovies[movie] == userBMovies[movie]:
						usersWithCommonRatingsAndMovies[-1] += 1
				except KeyError:
					pass

	print 'Mean number of movies watched in common: %f' % np.mean(usersWithCommonMovies)
	print 'Median number of movies watched in common: %d' % np.median(usersWithCommonMovies)

	print 'Mean number of movies watched in common and rated the same: %f' % np.mean(usersWithCommonRatingsAndMovies)
	print 'Median number of movies watched in common and rated the same: %d' % np.median(usersWithCommonRatingsAndMovies)

	plt.hist(usersWithCommonRatingsAndMovies,bins=np.arange(0,15,1))
	plt.xlabel('Number of movies in common')
	plt.ylabel('Number of users')
	plt.savefig('question3a.png')
	plt.show()

def question3b(movies):
	results = []
	for movie, users in movies.iteritems():
		results.append((movie, len(users)))

	results.sort(key=lambda x: x[1],reverse=True)

	print 'Movie with most reviews is %d with %d reviews.' % (results[0][0], results[0][1])
	print 'Movie with least reviews is %d with %d reviews.' % (results[-1][0], results[-1][1])

	plt.scatter(range(0,len(results)),[x[1] for x in results])
	plt.xlabel('Movie Rank')
	plt.ylabel('Number of Reviews')
	plt.savefig('question3b.png')
	plt.show()


if __name__ == "__main__":
    main()
