#!/usr/bin/env python3

import math
import random
import numpy as np
from plot_coalescence_time import probability_overlay, side_by_side

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

def lin_time_until_next(k, N0, b):
    """
    The time until the next coalescence in a linear population model
    """
    t = 0
    while True:
        t += 1
        N = round(N0 - (b * t))
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

    return times, x, y, labels

def lin_histogram(k, N0, b, replicates):
    """
    Histogram of next coalescence time with linear population
    """
    times = [lin_time_until_next(k, N0, b) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [lin_probability(k, N0, b, t) for t in x]
    labels = {"type": "Linear", "N": str(N0), "k": str(k), "b": str(b), "replicates": str(replicates)}
    
    return times, x, y, labels

def exp_histogram(k, N0, r, replicates):
    """
    Histogram of next coalescence time with exponential population
    """
    times = [exp_time_until_next(k, N0, r) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [exp_probability(k, N0, r, t) for t in x]
    labels = {"type": "Exponential", "N": str(N0), "k": str(k), "r": str(r), "replicates": str(replicates)}

    return times, x, y, labels

#
# Plot a 2x2 grid of a certain histogram. You could also find a way
# to mix the types, but I'm not gonna handle all that.
#

def con_multi_histogram(k_range, N_range, replicates):
    """
    Plot four different constant histograms as subplots so
    they can be compared easily
    """
    runs = []
    for (k, N) in zip(k_range, N_range):
        times, x, y, labels = con_histogram(k, N, replicates)
        runs.append({"times": times, "x": x, "y": y, "labels": labels})
    side_by_side(runs)

def lin_multi_histogram(k_range, N0_range, b_range, replicates):
    """
    Plot four different linear histograms as subplots so
    they can be compared easily
    """
    runs = []
    for (k, N0, b) in zip(k_range, N0_range, b_range):
        times, x, y, labels = lin_histogram(k, N0, b, replicates)
        runs.append({"times": times, "x": x, "y": y, "labels": labels})
    side_by_side(runs)

def exp_multi_histogram(k_range, N0_range, r_range, replicates):
    """
    Plot four different exponential histograms as subplots so
    they can be compared easily
    """
    runs = []
    for (k, N0, r) in zip(k_range, N0_range, r_range):
        times, x, y, labels = exp_histogram(k, N0, r, replicates)
        runs.append({"times": times, "x": x, "y": y, "labels": labels})
    side_by_side(runs)


if __name__ == "__main__":
    con_multi_histogram([6, 10, 14, 18],  [1000, 1000, 1000, 1000], 1000)
    lin_multi_histogram([6, 10, 14, 18],  [1000, 1000, 1000, 1000], [1, 1, 1, 1], 1000)
    lin_multi_histogram([10, 10, 10, 10], [1000, 1000, 1000, 1000], [0.5, 1, 1.5, 2], 1000)
    exp_multi_histogram([6, 10, 14, 18],  [1000, 1000, 1000, 1000], [0.1, 0.1, 0.1, 0.1], 1000)
    exp_multi_histogram([10, 10, 10, 10], [1000, 1000, 1000, 1000], [0.1, 0.2, 0.3, 0.4], 1000)
