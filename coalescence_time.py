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
            if choice in parents:
                return time
            else:
                parents.add(choice)

def coalescence_probability(N, k, t):
    """
    Calculate the probability that a coalescence occurs at time t given N and k,
    and no earlier or later.
    """
    lmd = (k * (k - 1)) / (2 * N)
    return lmd * math.exp(-lmd * t)

def histogram_data(N, k, replicates):
    """
    Generate the necessary data to create a histogram
    with the given N, k, and number of replicates.
    """
    times = [time_until_coalescence(N, k) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000)
    y = [coalescence_probability(N, k, t) for t in x]
    
    labels = {"N": str(N), "k": str(k), "replicates": str(replicates)}

    return times, x, y, labels

def plot_coalescence_probability_overlay(times, x, y, labels):
    """
    Overlay the coalescence probability function with a histogram
    showing the observed times for many replicates.
    """
    color1 = "steelblue"
    color2 = "navy"
    fig, ax = plt.subplots()

    # Plot the data
    ## Probability curve
    ax.plot(x, y, color=color2, label="Theoretical probability curve")

    ## Create a histogram, scaling so the total area underneath is 1
    hist, bin_edges = np.histogram(times, bins=range(0, max(times)))
    hist_neg_cumulative = [np.sum(hist[i:]) for i in range(len(hist))]
    hist_sum = sum(hist_neg_cumulative)
    hist_neg_cumulative = [term / hist_sum for term in hist_neg_cumulative]
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
    ax.step(bin_centers, hist_neg_cumulative, color=color1, label="Simulated coalescence timing")

    # Styles
    ax.set_ylabel("Probability of coalescence (%)")
    ax.set_xlabel("Time (t)")
    ax.legend()

    ## Give the graph a title with the run parameters
    info = "N = " + labels["N"] + \
           ", k = " + labels["k"] + \
           ", replicates = " + labels["replicates"]
    ax.set_title("Coalescence time for " + info)
    
    ## Padding around the graph
    fig.tight_layout(pad=2)
    
    # Print it! Yay?
    plt.show()

def test_things():
    N_range = np.arange(1000, 11000, 100)
    k_range = np.arange(2, 11, 1)
    for N in N_range:
        for k in k_range:
            times, x, y, labels = histogram_data(N, k, 1000)
            plot_coalescence_probability_overlay(times, x, y, labels)

if __name__ == "__main__":
    #test_things()
    times, x, y, labels = histogram_data(1000, 20, 1000)
    plot_coalescence_probability_overlay(times, x, y, labels)
