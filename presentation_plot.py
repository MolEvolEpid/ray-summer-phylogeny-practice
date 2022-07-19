#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from population_models import *
from tree_likelihood import *
from basic_optimization import *

def plot_populations():
    x = np.linspace(0, 10, 1000)

    con_params = {"N0": 2000, "k": 30}
    lin_params = {"N0": 4000, "k": 30, "b": 400}

    con_pop = [con_population(con_params, t) for t in x]
    lin_pop = [lin_population(lin_params, t) for t in x]

    con_prob = [con_probability(con_params, z) for z in x]
    lin_prob = [lin_probability(lin_params, z) for z in x]

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(-x, con_pop, color="#1C5D99", linewidth=3)
    ax1.plot(-x, lin_pop, color="#639FAB", linewidth=3)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel("Time (t)")
    ax1.set_ylabel("Population size (N)")

    ax2.plot(x, con_prob, color="#1C5D99", linewidth=3)
    ax2.plot(x, lin_prob, color="#639FAB", linewidth=3)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xlabel("Time until coalescence (z)")
    ax2.set_ylabel("Coalescence PDF (l)")

    plt.show()

def plot_constant_hdi():
    # Data should already be generated
    # Uncomment line in __main__ below to generate it
    tips_20 = bad_datafile_read(peak_infile="run/peaks_20.csv") # TODO generate these first
    tips_100 = bad_datafile_read(peak_infile="run/peaks_100.csv") 

    fig, (ax1, ax2) = plt.subplots(1, 2)

    for ax, data in zip([ax1, ax2], [tips_20, tips_100]):
        N0, peaks = calculate_axes(data)
        hdi = calculate_error(data, error_hdi)

        ax.scatter(N0, peaks, color="#1C5D99", zorder=3)
        ax.errorbar(N0, peaks, yerr=hdi, fmt="none", color="#639FAB", zorder=2, capsize=5, label="HDI")
        ax.set_xticks(N0)
        ax.set_yticks(N0)
        ax.set_title("Just for centering")
        ax.set_xlabel("Centering")
        ax.set_ylabel("Centering")

    plt.show()

def plot_linear_lk_curve():
    treefile = open("linear-latest.tre")
    tree = TimeTree(treefile.readline())
    treefile.close()

    fm = lambda x: -tree_likelihood(tree, lin_population, lin_probability, {"N0": x, "b": 1100})
    x = np.linspace(1, 2000, 1000)
    y = [fm(N0) for N0 in x]

    fig, ax = plt.subplots()

    ax.plot(x, y, color="#1C5D99", linewidth=3)

    ax.set_xlabel("Value of N0")
    ax.set_ylabel("Negative log likelihood")
    ax.set_title("just to center. b fixed at 1100.")

    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()

    plt.show()


if __name__ == "__main__":
    plot_constant_hdi()
    #plot_linear_lk_curve()


