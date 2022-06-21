#!/usr/bin/env python3

import matplotlib.pyplot as plt

def probability_overlay(times, x, y, labels):
    """
    Overlay the coalescence probability function with a histogram
    showing the observed times for many replicates.
    """
    color1 = "steelblue"
    color2 = "navy"
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(x, y, color=color2, label="Theoretical probability curve")
    ax.hist(times, bins=range(0, max(times)), density=True, color=color1, \
            label="Simulated coalescence timing")

    # Styles
    ax.set_ylabel("Probability of coalescence (%)")
    ax.set_xlabel("Time (t)")
    ax.legend()

    ## Give the graph a title with the run parameters
    info = "N = " + labels["N"] + ", k = " + labels["k"]
    if labels["type"] == "Exponential":
        info += ", r = " + labels["r"]
    if labels["type"] == "Linear":
        info += ", b = " + labels["b"]
    ax.set_title(labels["type"] + " population growth with " + info)

    ## Padding around the graph
    fig.tight_layout(pad=2)
    
    # Print it! Yay?
    plt.show()

