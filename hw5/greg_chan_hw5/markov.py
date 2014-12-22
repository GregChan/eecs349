import numpy as np

class HMM:
    def __init__(self, transition, observation, initial_probability):
        self.transition = transition
        self.observation = observation
        self.initial_probability = initial_probability
        np.set_printoptions(precision=10)

    def inner_prod(self, x, y, z):
        return sum(a*b*c for a,b,c in zip(x,y,z))

    def get_probability_initial(self, state):
        return [initial_probability*b for initial_probability,b in zip(self.initial_probability, self.observation[state])]

    def get_probability(self, state, old_probability):
        probability = []
        size = len(old_probability)
        for i in range(size):
            node_probability = self.inner_prod(old_probability, np.array(self.transition)[:, i], [self.observation[state][i]]*size)
            probability.append(node_probability)
        return probability

    def run(self, seq):
        probability = self.get_probability_initial(seq[0])
        print "T=0, probability: %s" % str(np.array(self.initial_probability))
        print "T=1, probability: %s" % str(np.array(probability))
        for t, state in enumerate(seq[1:]):
            probability = self.get_probability(state, probability)
            print "T=%d, probability: %s" % (t+2, np.array(probability))
        return sum(probability)

transition_1 = [[.5, .2, .3],
     [.5, .2, .3],
     [.5, .2, .3]]

observation_1 = [[.1, .5, .2],
     [.5, .3, .2],
     [.4, .2, .6]]

initial_probability_1 = [.3, .3, .4]

transition_2 = [[.2, .3, .5],
     [.6, .2, .2],
     [.6, .3, .1]]

observation_2 = [[.1, .6, .2],
     [.6, .3, .1],
     [.3, .1, .7]]

initial_probability_2 = [.5, .3, .2]

sequence_1 = [0,0,0,2,2]
sequence_2 = [1,0,2,0,0]

hmm_1 = HMM(transition_1, observation_1, initial_probability_1)
hmm_2 = HMM(transition_2, observation_2, initial_probability_2)

print "\nModel 1, Sequence 1"
print "Probability of observing sequence, given the model: %.6f" % hmm_1.run(sequence_1)
print "\nModel 1, Sequence 2"
print "Probability of observing sequence, given the model: %.6f" % hmm_1.run(sequence_2)

print "\nModel 2, Sequence 1"
print "Probability of observing sequence, given the model: %.6f" % hmm_2.run(sequence_1)
print "\nModel 2, Sequence 2"
print "Probability of observing sequence, given the model: %.6f" % hmm_2.run(sequence_2)
