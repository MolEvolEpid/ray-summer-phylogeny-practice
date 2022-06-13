#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
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

def log_likelihood(p, heads, tails):
	"""
	Calculate the log likelihood of a certain p (0 to 1, exclusive) based on observed
	numbers of heads and tails
	"""
	#print("p", p, "heads", heads, "tails", tails)
	return math.log(pow(p, heads)) + math.log(pow(1-p, tails))

def likelihood_curve(heads, tails):
	"""
	Given a number of heads and tails, construct a curve showing
	the log likelihood of p between 0 and 1.
	"""
	x = np.linspace(0, 1, 1000, endpoint=False)[1:] #TODO: fix this messy way to exclude both 0 and 1
	y = []
	for p in x:
		y.append(log_likelihood(p, heads, tails))
	return x, y

def important_points(x, y): #TODO: This doesn't actually return anything useful at the moment.
	"""
	Given a likelihood curve, find the maximum point on the curve, 
	as well as the positions that make up a 95% confidence interval.
	"""
	maximum = 1
	lower = 0.1
	upper = 0.9
	return maximum, lower, upper

if __name__ == "__main__":
	h, t = count_faces(sys.argv[1]) # TODO: add some sort of checking
	x, y = likelihood_curve(h, t)

	max_pos = y.index(max(y))

	print(x[max_pos], y[max_pos])

	plt.plot(x, y)
	plt.show()
