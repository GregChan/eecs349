import sys, csv, random

class Node:
	def __init__(self):
		self.right = None
		self.left = None

class Items:
	def __init__(self, items):
		self.items = items
	
	def calculateEntropyGainFromAttribute(attribute):
		originalGood = 0
		originalBad = 0

		goodCountsByAttributeValue = {}
		badCountsByAttributeValue = {}
		totalItemsByAttributeValue = {}

	def get_best_classifier(attributes):
		attributesToCheck = attributes.keys()

		if len(attributesToCheck) == 1:
			return attributesToCheck[0]

		maxGain = 0
		bestAttribute = None

		for attribute in attributesToCheck:
			gain = calculateEntropyGainFromAttribute(attribute)

			if gain > maxGain:
				maxGain = gain
				bestAttribute = attribute
		return bestAttribute

def ID3(examples, target_attribute, attributes):
	print 'ID3'
	root = Node()

	# if examples are positive

	# if examples are negative

	# if attributes is empty
	if not attributes:
		return root
	
	# A <-- the attribute from Attributes that best classifies examples
	
	

if len(sys.argv) < 5:
	print "Not enough arguments were provided."
	exit(1)

inputFileName = sys.argv[1]
trainingSetSize = sys.argv[2]
numberOfTrials = sys.argv[3]
verbose = sys.argv[4]

# read in the specified text file containing th examples
with open(inputFileName, 'rb') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t', quotechar='\'')
	rows = []
	for row in reader:
		rows.append(row)
	# randomly select the number of examples for the training set
	trainingSet = random.sample(rows, int(trainingSetSize))

	# estimate probability using the training set
	trainingSetProbabilityMap = {}
	for row in trainingSet:
		for key, value in row.iteritems():
			if not key in trainingSetProbabilityMap:
				trainingSetProbabilityMap[key] = 0
			if 'true' in value:
				trainingSetProbabilityMap[key] += 1
	for key, value in trainingSetProbabilityMap.iteritems():
		trainingSetProbabilityMap[key] = value / float(trainingSetSize)

	# construct a decision tree, based on the training set
	ID3(trainingSet, 1, ['',''])	

	print trainingSetProbabilityMap

