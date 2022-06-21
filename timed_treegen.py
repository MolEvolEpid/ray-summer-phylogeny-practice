#!/usr/bin/env python3

import math
import random
import numpy as np
from coalescence_time import coalescence_probability, \
        plot_coalescence_probability_overlay as plot_coalescence

#
# Simulate the time until a coalescence event with each population model
#

def con_time_until_next(k, N):
    """
    The time until the next coalescence in a constant population model
    """
    t = 0
    while True:
        parents = set()
        for i in range(k):
            p = random.randint(0, N-1)
            if p in parents:
                return t
            else:
                parents.add(p)

def lin_time_until_next(k, N0, beta):
    """
    The time until the next coalescence in a linear population model
    """
    t = 0
    while True:
        t += 1
        N = round(N0 - (beta * t))
        parents = set()
        for i in range(k):
            p = random.randint(0, N-1)
            if p in parents:
                return t
            else:
                parents.add(p)

def exp_time_until_next(k, N0, r):
    """
    The time until the next coalescence in an exponential population model
    """
    t = 0
    while True:
        t += 1
        N = round(N0 * math.exp(-r * t))
        parents = set()
        for i in range(k):
            p = random.randint(0, N-1)
            if p in parents:
                return t
            else:
                parents.add(p)

#
# Functions for the probability of coalescence by time t
# for each population model
#

# TODO: Should I move the constant one in here? Right now it lives in coalescent_probability

def con_probability(k, N, z):
    """
    The proabaility of a coalescence at time z with constant population
    """
    return coalescence_probability(N, k, z)

def lin_probability(k, N0, b, z):
    """
    The probability of a coalescence at time z with linear population
    """
    return (k*(k-1)/2) / (N0-b*z) * (N0 / (N0-b*z))**(-k*(k-1)/(2*b))

def exp_probability(k, N0, r, z):
    """
    The probability of a coalescence at time z with exponential population
    """
    return k*(k-1)/2 * math.exp(r*z) / N0 * math.exp(-(k*(k-1)/2) * (math.exp(r*z) -1) / (r*N0))

#
# Return data for a histogram of the probability of coalescence at over time
# for each population model
#

def con_histogram(k, N, replicates):
    """
    Histogram of next coalescence time with constant population
    """
    times = [con_time_until_next(k, N) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [con_probability(k, N0, t) for t in x]
    labels = {"N": str(N), "k": str(k), "replicates": str(replicates)}

    plot_coalescence(times, x, y, labels)

def lin_histogram(k, N0, beta, replicates):
    """
    Histogram of next coalescence time with linear population
    """
    times = [lin_time_until_next(k, N0, beta) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [lin_probability(k, N0, beta, t) for t in x]
    labels = {"N": str(N0), "k": str(k), "replicates": str(replicates)}

    plot_coalescence(times, x, y, labels)

def exp_histogram(k, N0, r, replicates):
    """
    Histogram of next coalescence time with exponential population
    """
    times = [exp_time_until_next(k, N0, r) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [exp_probability(k, N0, r, t) for t in x]
    labels = {"N": str(N0), "k": str(k), "replicates": str(replicates)}

    plot_coalescence(times, x, y, labels)

if __name__ == "__main__":
    exp_histogram(5, 1000, 0.1, 1000)
