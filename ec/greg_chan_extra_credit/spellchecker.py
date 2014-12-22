from os import listdir
from os.path import isfile, join
import numpy as np
import subprocess

spam_directory = 'spam'
ham_directory = 'ham'
mail_directory = 'm'
spam = 's'
ham = 'h'

# get all unique words from an email
def get_words_in_email(file_path):
	file_reader = open(file_path, 'rb')
	lines = file_reader.read().split('\n')

	subject_index = 0

	# find the subject line
	for line in lines:
		if 'Subject' in line:
			subject_index = lines.index(line)

	# try to find the space after the first subject line
	try:
		# the start of the message is after the first line break from the subject line
		start_message = lines[subject_index:].index('') + 1
	except:
		# if the start of the message doesn't exist include all information 
		start_message = 0

	words = set()

	# get all the words from the start of the message and build a set of all words
	# sets are unique so it only returns on instance of any word in the list
	for i in range(start_message, len(lines)):
		for word in lines[i].split(' '):
			if word is not '':
				words.add(word.lstrip().rstrip())

	return words

# make the dictionary returns nothing
def makedictionary(spam_directory, ham_directory, dictionary_filename):
	dictionary = {}
	total_spam_emails = 1
	total_ham_emails = 1

	# for each email in the spam directory
	for f in listdir(spam_directory):
		if isfile(join(spam_directory, f)) and f != '.DS_Store':
			file_path = join(spam_directory,f)
			words = get_words_in_email(file_path)

			for word in words:
				if word in dictionary:
					dictionary[word]['spam_count'] += 1
				else:
					dictionary[word] = {}
					dictionary[word]['spam_count'] = 1
					dictionary[word]['ham_count'] = 0
			total_spam_emails += 1

	# for each email in the ham directory
	for f in listdir(ham_directory):
		if isfile(join(ham_directory, f)) and f != '.DS_Store':
			file_path = join(ham_directory,f)
			words = get_words_in_email(file_path)

			# for each word count that we've seen it
			for word in words:
				if word in dictionary:
					dictionary[word]['ham_count'] += 1
				else:
					dictionary[word] = {}
					dictionary[word]['spam_count'] = 0
					dictionary[word]['ham_count'] = 1
			total_ham_emails += 1

	words = sorted(dictionary.keys())

	dictionary_file = open(dictionary_filename, 'wb')

	# calculate the probability for each word and save it to a file.
	for word in words:
		# added pseudocount in so that the probability is not zeroo
		p_spam = (float(dictionary[word]['spam_count']) + 1) / total_spam_emails
		p_ham = (float(dictionary[word]['ham_count']) + 1) / total_ham_emails
		line = '%s %.9f %.9f\n' % (word, p_spam, p_ham)
		dictionary_file.write(line)

# sort spam in specified directories returns nothing
def spamsort(mail_directory, spam_directory, ham_directory, dictionary_filename, spam_prior_probability):
	ham_prior_probability = 1 - spam_prior_probability

	# read in the dictionary
	dictionary_file = open(dictionary_filename, 'rb')
	spam_dictionary = {}
	ham_dictionary = {}

	for line in dictionary_file:
		line_contents = line.split(' ')
		word = line_contents[0]
		spam = float(line_contents[1])
		ham = float(line_contents[2])
		
		# build a spam dictionary and a ham dictionary
		spam_dictionary[word] = spam
		ham_dictionary[word] = ham

	spam_count = 0
	ham_count = 0

	# correct_spam_classifications = 0
	# correct_ham_classifications = 0

	# go through all test emails
	for f in listdir(mail_directory):
		if isfile(join(mail_directory, f)) and f != '.DS_Store':
			file_path = join(mail_directory,f)
			words = get_words_in_email(file_path)

			# start with a base probability of the prior probability of spam/ham
			probability_spam = np.log(spam_prior_probability)
			probability_ham = np.log(ham_prior_probability)

			# compute the log probability for the message given a set of unique words
			for word in words:
				if word in ham_dictionary and word in spam_dictionary:
					probability_ham += np.log(ham_dictionary[word])
					probability_spam += np.log(spam_dictionary[word])

			# if the log probability of spam > ham then it is spam else it's ham
			if probability_spam > probability_ham:
				spam_count += 1

				# if f in listdir(spam_directory):
				# 	correct_spam_classifications += 1

				# move the files
				subprocess.call(["mv", file_path, join(spam_directory, f)])
			else:
				ham_count += 1

				# if f in listdir(ham_directory):
				# 	correct_ham_classifications += 1

				# move the files
				subprocess.call(["mv", file_path, join(ham_directory, f)])

	# print spam_count
	# print ham_count

# build dictionary
makedictionary(spam_directory, ham_directory, 'dictionary')
# sort spam
spamsort(mail_directory, spam, ham, 'dictionary', 0.1)

