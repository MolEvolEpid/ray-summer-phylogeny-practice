#!/usr/bin/env python3

import math
import random
import numpy as np
from plot_coalescence_time import probability_overlay, side_by_side

#
# Simulate the time until a coalescence event with each population model
#

def con_population(params, t):
    """
    Return a constant population at time t.

    Required parameters:
      N0 : population size
    """
    return params["N0"]

def lin_population(params, t):
    """
    Return the value of a linear population at time t.

    Required parameters:
      N0 : population size at time 0
      b : slope (> 0)
    """
    N0 = params["N0"]
    b = params["b"]
    return N0 - b*t

def exp_population(params, t):
    """
    Return the value of an exponential population at time t.

    Required parameters:
      N0 : population at time 0
      r : rate of change (> 0)
    """
    N0 = params["N0"]
    r = params["r"]
    return N0 * np.exp(-r*t)

def time_until_next(population, params):
    """
    Return the time until a coalescence occurs in a given population model.

    Required parameters:
      Any parameters required by the population model
      k : sample size
    """
    t = 0
    while True:
        t += 1
        N = population(params, t)
        parents = set()
        for i in range(params["k"]):
            p = random.randint(0, N-1)
            if p in parents:
                return t
            else:
                parents.add(p)

#
# Functions for the probability of coalescence by time t
# for each population model
#

def con_probability(params, z):
    """
    The proabaility of a coalescence at time z with constant population

    Parameters:
      params : dictionary
        k : sample size
        N0 : population
      z : time of occurence

    Returns:
      probability (float): The probability of a coalescence occuring
    """
    k = params["k"]
    N0 = params["N0"]
    if N0 <= 0:
        return 0
    lmd = k*(k - 1)/(2*N0)
    return lmd * math.exp(-lmd*z)

def lin_probability(params, z):
    """
    The probability of a coalescence at time z with linear population

    Parameters:
      params : dictionary
        k : sample size
        N0 : population
        b : slope (> 0)
      z : time of occurence

    Returns:
      probability (float): The probability of a coalescence occuring
    """
    k = params["k"]
    N0 = params["N0"]
    b = params["b"]
    if N0 - b*z <= 0: # would result in /0 errors, so we return 0 instead
        return 0
    return (k*(k-1)/2) / (N0-b*z) * (N0 / (N0-b*z))**(-k*(k-1)/(2*b))

def exp_probability(params, z):
    """
    The probability of a coalescence at time z with exponential population

    Parameters:
      params : dictionary
        k : sample size
        N0 : population
        r : rate of change (> 0)
      z : time of occurence

    Returns:
      probability (float): The probability of a coalescence occuring
    """
    k = params["k"]
    N0 = params["N0"]
    r = params["r"]
    if N0 <= 0:
        return 0
    return k*(k-1)/2 * math.exp(r*z) / N0 * math.exp(-(k*(k-1)/2) * (math.exp(r*z) -1) / (r*N0))

#
# Return data for a histogram of the probability of coalescence at over time
# for each population model
#

def histogram(population, probability, params, replicates):
    """
    Return the necessary data to plot a histogram of the probability of
    coalescence over time.

    population : function con_- lin_- or exp_population
    probability : function con_- lin_- or exp_probability
    params : dictionary of required parameters for population and probability
    replicates : integer (> 0)
    """
    times = [time_until_next(population, params) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [probability(params, z) for z in x]

    labels = {"k": str(params["k"])}
    if "r" in params:
        labels["type"] = "Exponential"
        labels["N"] = str(params["N0"])
        labels["r"] = str(params["r"])
    elif "b" in params:
        labels["type"] = "Linear"
        labels["N"] = str(params["N0"])
        labels["b"] = str(params["b"])
    elif "N" in params:
        labels["type"] = "Constant"
        labels["N"] = str(params["N"])
    else:
        raise Exception("We shouldn't have gotten to here. Check parameters.")

    return times, x, y, labels

#
# Plot a 2x2 grid of a certain histogram. You could also find a way
# to mix the types, but I'm not gonna handle all that.
#
# I'm gonna keep the duplication here because the only thing I can think of doing
# (a dictionary of lists) is atrocious
#

def con_multi_histogram(k_range, N_range, replicates):
    """
    Plot four different constant histograms as subplots so
    they can be compared easily
    """
    runs = []
    for (k, N) in zip(k_range, N_range):
        times, x, y, labels = histogram(con_population, con_probability, \
                                        {"k": k, "N": N}, replicates)
        runs.append({"times": times, "x": x, "y": y, "labels": labels})
    side_by_side(runs)

def lin_multi_histogram(k_range, N0_range, b_range, replicates):
    """
    Plot four different linear histograms as subplots so
    they can be compared easily
    """
    runs = []
    for (k, N0, b) in zip(k_range, N0_range, b_range):
        times, x, y, labels = histogram(lin_population, lin_probability, \
                                        {"k": k, "N0": N0, "b": b}, replicates)
        runs.append({"times": times, "x": x, "y": y, "labels": labels})
    side_by_side(runs)

def exp_multi_histogram(k_range, N0_range, r_range, replicates):
    """
    Plot four different exponential histograms as subplots so
    they can be compared easily
    """
    runs = []
    for (k, N0, r) in zip(k_range, N0_range, r_range):
        times, x, y, labels = histogram(exp_population, exp_probability, \
                                        {"k": k, "N0": N0, "r": r}, replicates)
        runs.append({"times": times, "x": x, "y": y, "labels": labels})
    side_by_side(runs)


if __name__ == "__main__":
    times, x, y, labels = histogram(con_population, con_probability, {"N": 10000, "k": 50}, 1000)
    probability_overlay(times, x, y, labels)
    #con_multi_histogram([6, 10, 14, 18],  [1000, 1000, 1000, 1000], 1000)
    #lin_multi_histogram([6, 10, 14, 18],  [1000, 1000, 1000, 1000], [1, 1, 1, 1], 1000)
    #lin_multi_histogram([10, 10, 10, 10], [1000, 1000, 1000, 1000], [0.5, 1, 1.5, 2], 1000)
    #exp_multi_histogram([6, 10, 14, 18],  [1000, 1000, 1000, 1000], [0.1, 0.1, 0.1, 0.1], 1000)
    #exp_multi_histogram([10, 10, 10, 10], [1000, 1000, 1000, 1000], [0.1, 0.2, 0.3, 0.4], 1000)
