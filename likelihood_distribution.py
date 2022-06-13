#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import sys # at the moment I use it for sys.argv but maybe I don't need that idk
import math

def count_faces(string):
	"""
	Given a string of space-separated letters, count the number of times 
	"H" and "T" occur
	"""
	heads = tails = 0
	for face in string.split():
		if face.lower() == "h":
			heads += 1
		elif face.lower() == "t":
			tails += 1
	return heads, tails

def binomial_coeff(n, x):
	"""
	Calculate a binomial coefficient based on the number of heads (x) in 
	n flips of the coin, as described by Etz (2018).
		https://doi.org/10.1177/2515245917744314
	"""
	return math.factorial(n) / (math.factorial(x) * math.factorial(n - x))

def likelihood(p, heads, tails):
	"""
	Calculate the likelihood of a certain p (0 to 1, exclusice) based on observed
	numbers of heads and tails
	"""
	return pow(p, heads) * pow(1-p, tails)

def log_likelihood(p, heads, tails):
	"""
	Calculate the log likelihood of a certain p (0 to 1, exclusive) based on observed
	numbers of heads and tails
	"""
	return math.log(pow(p, heads)) + math.log(pow(1-p, tails))

def likelihood_curve(heads, tails):
	"""
	Given a number of heads and tails, construct a curve showing
	the log likelihood of p between 0 and 1.
	"""
	x = np.linspace(0, 1, 1000, endpoint=False)[1:] #TODO: Can I make this less ugly? 
	y = []
	bc = binomial_coeff(heads + tails, heads)
	for p in x:
		y.append(bc * likelihood(p, heads, tails)) 
	return x, y

def important_points(x, y): 
	"""
	Given a likelihood curve, find the maximum point on the curve, 
	as well as the positions that make up a 95% confidence interval.
	"""
	maximum = y.index(max(y))
	lower = 0.1 # TODO: Find the right way to calculate these figures. Do not assume binomial dist!
	upper = 0.9
	return maximum, lower, upper

if __name__ == "__main__":
	h, t = count_faces(sys.argv[1]) # TODO: add some sort of checking
	x, y = likelihood_curve(h, t)

	max_pos = y.index(max(y))
	print("max of", y[max_pos], "at x =", x[max_pos])

	plt.plot(x, y)
	plt.show()
