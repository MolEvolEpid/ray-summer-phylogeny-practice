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
        # TODO jsut check if there are duplicates and return
        nodes = set([random.randint(1, N-1) for i in nodes])
    return time

def coalescence_probability(N, k, t):
    """
    Calculate the probability that a coalescence occurs at time t given N and k, 
    and no earlier or later.
    """
    num_possible_pairs = (k * (k - 1)) / 2
    prob = math.comb(k, 2) / N
    assert prob <= 1, "Coalescence probability should not be above 1"
    return num_possible_pairs * math.pow(1 - prob, t-1) * prob

def plot_coalescence_probability_overlay(N, k, replicates):
    """
    Overlay the coalescence probability function with a histogram
    showing the observed times for many replicates.
    """
    # Generate the data
    times = [time_until_coalescence(N, k) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000) # todo: do I need to copy it?
    y = [coalescence_probability(N, k, t) for t in x]

    # Make two X axes to plot both on top of each other
    fig, hist_ax = plt.subplots()
    plot_ax = hist_ax.twinx()

    # Plot the actual data
    hist_ax.hist(times)
    plot_ax.plot(x, y, color="black")
    plt.ylim(bottom=0)

    plt.show()

if __name__ == "__main__":
    plot_coalescence_probability_overlay(1000, 20, 1000)
