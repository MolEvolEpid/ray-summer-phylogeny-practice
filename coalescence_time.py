#!/usr/bin/env python3

import random
import math
import numpy as np
import matplotlib.pyplot as plt

# TODO: need to do something with this citation

# Nordborg, M. (2001). Coalescent theory. In D.J. Balding, M.J. Bishop and C. Cannings (eds.),
#   Handbook of Statistical Genetics. John Wiley & Sons, Chichester, pp. 179–212.

def time_until_coalescence(N, k):
    """
    Run a neutral coalescent model until a coalescence occurs,
    returning the total number of generations.
    """
    nodes = range(k)
    time = 0
    while len(nodes) == k:
        time += 1
        nodes = set([random.randint(1, N-1) for i in nodes])
    return time

def likelihood(N, k, t):
    """
    Calculate the likelihood that a coalescence occurs at time t given N and k.

    For a coalescence to first occur at time t, the likelihood must include
    the probability of t-1 generations without coalescence and 1 generation
    that coalesces.
    """
    possible_pairs = (k * (k - 1)) / 2
    coalescence_prob = math.comb(k, 2) / N
    return possible_pairs * math.pow(1 - coalescence_prob, t-1) * coalescence_prob

def plot_coalescence_time(N, k, iterations):
    """
    Overlay the likelihood function for coalescence time on a histogram
    showing the coalescence time of many iterations of the coalescence model.
    """
    times = [time_until_coalescence(N, k) for i in range(iterations)]
    scaling_factor = (max(times) / N)
    x = np.linspace(0, N, 1000)
    y = [likelihood(N, k, t) for t in x] # TODO: Why do I have another coefficient here?!

    plt.plot(x, y)
    #plt.hist(times)

    plt.show()

if __name__ == "__main__":
    plot_coalescence_time(100, 2, 1000)
