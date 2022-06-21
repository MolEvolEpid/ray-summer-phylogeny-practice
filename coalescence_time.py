#!/usr/bin/env python3

import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Nordborg, M. (2001). Coalescent theory. In D.J. Balding, M.J. Bishop and C. Cannings (eds.),
#   Handbook of Statistical Genetics. John Wiley & Sons, Chichester, pp. 179–212.

def time_until_coalescence(N, k):
    """
    Run a neutral coalescent model until a coalescence occurs,
    returning the total number of generations.
    """
    time = 0
    while True: 
        time += 1
        parents = set()
        for node in range(k):
            choice = random.randint(1, N-1)
            if choice in parents: # sets have good __ in __ lookup times
                return time
            else:
                parents.add(choice)

def coalescence_probability(N, k, t):
    """
    Calculate the probability that a coalescence occurs at time t given N and k, 
    and no earlier or later.
    """
    num_possible_pairs = (k * (k - 1)) / 2
    prob = math.comb(k, 2) / N
    assert prob <= 1, "Coalescence probability should not be above 1"
    return math.pow(1 - prob, t-1) * prob #TODO: Was I not supposed to multiply by num_possible_pairs?

def histogram_data(N, k, replicates):
    """
    Generate the necessary data to create a histogram
    with the given N, k, and number of replicates.
    """
    times = [time_until_coalescence(N, k) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [coalescence_probability(N, k, t) for t in x]

    return times, x, y

def plot_coalescence_probability_overlay(times, x, y):
    """
    Overlay the coalescence probability function with a histogram
    showing the observed times for many replicates.
    """
    color1 = "steelblue"
    color2 = "navy"
    fig, ax = plt.subplots()

    # Plot the data
    ## Probability curve
    ax.plot(x, y, color=color2)
    
    ## Create a histogram, scaling so the total area underneath is 1
    hist, bin_edges = np.histogram(times, bins=20)
    hist_neg_cumulative = [np.sum(hist[i:]) for i in range(len(hist))]
    hist_sum = sum(hist_neg_cumulative)
    hist_neg_cumulative = [term / hist_sum for term in hist_neg_cumulative]
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
    ax.step(bin_centers, hist_neg_cumulative)
   
    # Styles
    ax.set_ylabel("Probability of coalescence (%)")
    ax.set_xlabel("Time (t)")

    ## Give the graph a title with the run parameters
    info = "N = " + str(N) + ", k = " + str(k) + ", replicates = " + str(replicates)
    ax.set_title("Coalescence time for " + info)
    
    ## Padding around the graph
    fig.tight_layout(pad=2)
    
    # Print it! Yay?
    plt.show()

if __name__ == "__main__":
    plot_coalescence_probability_overlay(1000, 20, 1000)
    #test_things()
