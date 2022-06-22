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
    ax.set_title(labels["type"] + " coalescence time with " + info)

    ## Padding around the graph
    fig.tight_layout(pad=2)
    
    # Print it! Yay?
    plt.show()

def side_by_side(runs):
    """
    Draw four plots as subplots, in a 2x2 pattern.

    It's sorta complicated, but runs should be a list of four
    dictionaries, and each one should have these keys
        times
        x
        y
        labels
    """
    color1 = "steelblue"
    color2 = "navy"

    fig, axs = plt.subplots(2, 2)

    # To scale them all on the same axis, clumsy implementation
    x_maxes = []
    y_maxes = []
    for run in runs:
        x_maxes.append(max(run["x"]))
        y_maxes.append(max(run["y"]))
    x_max = max(x_maxes)
    y_max = max(y_maxes)

    for (run, ax) in zip(runs, axs.flat):
        x = run["x"]
        y = run["y"]
        times = run["times"]
        labels = run["labels"]
        
        ax.plot(x, y, color=color2, label="Theory")
        ax.hist(times, bins=range(0, max(times)), density=True, color=color1, label="Simulation")

        ax.set_ylim(top=y_max)
        ax.set_xlim(right=x_max)

        ax.set_ylabel("Probability of coalescence (%)")
        ax.set_ylabel("Time (t)")

        info = "N = " + labels["N"] + ", k = " + labels["k"]
        if labels["type"] == "Exponential":
            info += ", r = " + labels["r"]
        if labels["type"] == "Linear":
            info += ", b = " + labels["b"]
        ax.set_title(labels["type"] + " coalescence time with " + info)
    fig.tight_layout(pad=2)
    plt.show()
