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
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Plot the actual data
    ax1.hist(times, color=color1)
    ax2.plot(x, y, color=color2)
   
    # Styles (what a mess!)
    ## Color and name the histogram y-axis (and the x-axis because I did it weird)
    ax1.set_ylabel("Coalesced generations (out of " + str(replicates) + ")")
    ax1.yaxis.label.set_color(color1)
    ax1.set_xlabel("Time (t)")

    ## Color and name the probability plot y-axis
    ax2.set_ylabel("Probability of coalescence")
    ax2.yaxis.label.set_color(color2)
    
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
    #N_range = np.concatenate((np.arange(100, 1000, 100), np.arange(1000, 11000, 1000)))
    N_range = np.arange(1000, 11000, 1000)
    k_range = np.arange(2, 11, 1)
    for N in N_range:
        for k in k_range:
            plot_coalescence_probability_overlay(N, k, 1000)

if __name__ == "__main__":
    #plot_coalescence_probability_overlay(1000, 20, 1000)
    #test_things()
    pass
