#!/usr/bin/env python3


import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import sys # at the moment I use it for sys.argv but maybe I don't need that idk
import math


def count_faces(string):
	"""
	Given a string of space-separated letters, count 
	the number of times"H" and "T" occur
	"""
	heads = tails = 0
	for face in string.split():
		if face.lower() == "h":
			heads += 1
		elif face.lower() == "t":
			tails += 1
	return heads, tails


def binomial_coefficient(heads, tails):
	"""
	Calculate a binomial coefficient based on the number of heads and tails
	observed, representing the number of ways a certain number of heads could
	be rolled as described in Etz (2018).
		https://doi.org/10.1177/2515245917744314
	"""
	return math.factorial(heads + tails) / (math.factorial(heads) * math.factorial(tails))


def likelihood(p, heads, tails):
	"""
	Calculate the likelihood of a certain p (0 to 1, exclusive) 
	based on observed numbers of heads and tails. 
	"""
	bc = binomial_coefficient(heads, tails)
	return bc * pow(p, heads) * pow(1-p, tails)


def log_likelihood(p, heads, tails):
	"""
	Calculate the log likelihood of a certain p (0 to 1, exclusive)
	based on observednumbers of heads and tails.
	"""
	bc = binomial_coefficient(heads, tails) 
	return bc * (np.log(pow(p, heads)) + np.log(pow(1-p, tails)))


def high_low_ci(heads, tails):
	"""
	Use fisher information to find the high and low confidence intervals
	for the log likelihood, then convert these values back into likelihood.
	Statistical reference from Slavković (n.d.)
		http://personal.psu.edu/abs12/
	"""
	p_sample = heads / (heads + tails)
	fisher_info = (heads + tails) * p_sample * (1 - p_sample)
	
	phi_hat = np.log(p_sample / (1 - p_sample))
	confidence_interval = 1.96 * math.sqrt(1 / fisher_info)
	phi_low = phi_hat - confidence_interval
	phi_high = phi_hat + confidence_interval
	
	low_ci = math.pow(math.e, phi_low) / (1 + math.pow(math.e, phi_low))
	high_ci = math.pow(math.e, phi_high) / (1 + math.pow(math.e, phi_high))
	return low_ci, high_ci


def likelihood_curve(heads, tails):
	"""
	Given a number of heads and tails, construct a curve showing
	the log likelihood of p between 0 and 1.
	"""
	x = np.linspace(0, 1, 1000, endpoint=False)[1:] 
	y = []
	for p in x:
		y.append(likelihood(p, heads, tails)) 
	return x, y


if __name__ == "__main__":
	h, t = count_faces(sys.argv[1]) # TODO: add some sort of checking
	p_sample = h / (h + t)
	x, y = likelihood_curve(h, t)
	low_ci, high_ci = high_low_ci(h, t)
	#max_pos = y.index(max(y))

	fig, ax = plt.subplots(figsize=(12, 5))
	
	ax.plot(x, y, c="black")
	ax.set_xlabel("p value")
	ax.set_ylabel("likelihood")
	ax.set_title("95% Confidence Interval of p")
	ax.fill_between(x, 0, y, where=(np.array(x) > low_ci) & (np.array(x) < high_ci), facecolor="lightgreen")
	ax.axvline(x=p_sample, color="blue", linestyle="--")
	#ax.grid(False)

	plt.show()
