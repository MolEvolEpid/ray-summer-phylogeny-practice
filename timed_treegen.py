#!/usr/bin/env python3

import math
import random
import numpy as np
from plot_coalescence_time import probability_overlay

#
# Simulate the time until a coalescence event with each population model
#

def con_time_until_next(k, N):
    """
    The time until the next coalescence in a constant population model
    """
    t = 0
    while True:
        t += 1
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

def con_probability(k, N, z):
    """
    The proabaility of a coalescence at time z with constant population
    """
    lmd = k*(k - 1)/(2*N)
    return lmd * math.exp(-lmd*z)

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
    y = [con_probability(k, N, t) for t in x]
    labels = {"type": "Constant", "N": str(N), "k": str(k), "replicates": str(replicates)}

    plot_coalescence(times, x, y, labels)

def lin_histogram(k, N0, beta, replicates):
    """
    Histogram of next coalescence time with linear population
    """
    times = [lin_time_until_next(k, N0, beta) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [lin_probability(k, N0, beta, t) for t in x]
    labels = {"type": "Linear", "N": str(N0), "k": str(k), "replicates": str(replicates)}

    plot_coalescence(times, x, y, labels)

def exp_histogram(k, N0, r, replicates):
    """
    Histogram of next coalescence time with exponential population
    """
    times = [exp_time_until_next(k, N0, r) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [exp_probability(k, N0, r, t) for t in x]
    labels = {"type": "Exponential", "N": str(N0), "k": str(k), "replicates": str(replicates)}

    plot_coalescence(times, x, y, labels)

#
# Some simple scripts to test these things
#

def con_test():
    for k in np.arange(2, 32, 5):
        con_histogram(k, 1000, 1000)

def lin_test():
    for b in np.arange(1, 3, 1):
        for k in np.arange(2, 32, 5):
            lin_histogram(k, 100000, b, 1000)

def exp_test():
    for k in np.linspace(2, 32, 5):
        for r in np.linspace(0, 1, 15):
            exp_histogram(k, 1000, r, 1000)


if __name__ == "__main__":
    exp_histogram(5, 1000, 0.1, 1000)
