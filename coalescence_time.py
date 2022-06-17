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
    return math.pow(1 - prob, t-1) * prob #TODO: Was I not supposed to multiply by num_possible_pairs?

def plot_coalescence_probability_overlay(N, k, replicates):
    """
    Overlay the coalescence probability function with a histogram
    showing the observed times for many replicates.
    """
    color1 = "steelblue"
    color2 = "navy"

    # Generate the data
    times = [time_until_coalescence(N, k) for i in range(replicates)]
    x = np.linspace(0, max(times), 1000) # todo: do I need to copy it?
    y = [coalescence_probability(N, k, t) for t in x]

    # Make two X axes to plot both on top of each other
    fig, hist_ax = plt.subplots()
    plot_ax = hist_ax.twinx()

    # Plot the actual data
    hist_ax.hist(times, color=color1)
    plot_ax.plot(x, y, color=color2)
   
    # Styles (what a mess!)
    ## Color and name the histogram y-axis (and the x-axis because I did it weird)
    hist_ax.set_ylabel("Coalesced generations (out of " + str(replicates) + ")")
    hist_ax.yaxis.label.set_color(color1)
    hist_ax.set_xlabel("Time (t)")

    ## Color and name the probability plot y-axis
    plot_ax.set_ylabel("Probability of coalescence")
    plot_ax.yaxis.label.set_color(color2)
    
    ## Give the graph a title with the run parameters
    info = "N = " + str(N) + ", k = " + str(k) + ", replicates = " + str(replicates)
    plt.title("Coalescence time for " + info)

    ## Make sure that zero lines up for both plots
    plt.ylim(bottom=0)

    ## Padding around the graph
    fig.tight_layout(pad=2)
    
    # Print it! Yay?
    plt.show()

def test_things():
    for N in np.arange(100, 1100, 100):
        for k in np.arange(2, 11, 1):
            plot_coalescence_probability_overlay(N, k, 1000)

if __name__ == "__main__":
    #plot_coalescence_probability_overlay(1000, 20, 1000)
    test_things()
