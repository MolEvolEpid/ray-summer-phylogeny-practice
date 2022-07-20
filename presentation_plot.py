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
    # Set up all these fonts
    title_font = {"family": "CMU Sans Serif",
                  "size": 32}

    main_font = {"family": "CMU Sans Serif",
                 "size": 22}
    
    plt.rcParams['font.size'] = 14
    tips_20 = bad_datafile_read(peak_infile="run/peaks_20.csv") # TODO generate these first
    tips_100 = bad_datafile_read(peak_infile="run/peaks_100.csv") 

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(16, 8)

    for ax, data in zip([ax1, ax2], [tips_20, tips_100]):
        N0, peaks = calculate_axes(data)
        hdi = calculate_error(data, error_hdi)

        ax.plot(N0, N0, color="#56b4e9")

        ax.scatter(N0, peaks, color="#0072b2", zorder=3, label="Mean of Maximum Likelihood Estimates")
        ax.errorbar(N0, peaks, yerr=hdi, fmt="none", color="#d55e00", zorder=2, capsize=5, label="95% Highest Density Interval")
        ax.set_xticks(N0)
        ax.set_yticks(N0)
        ax.set_ylim(top=15000)
        ax.set_xlabel("Real population size", **main_font)
        ax.set_ylabel("Estimated population size", **main_font)
        ax.legend()

    ax1.set_title("Trees with 20 sequences", **title_font)
    ax2.set_title("Trees with 100 sequences", **title_font)

    plt.savefig("hdi_fig.pdf")
    plt.show()

def plot_linear_lk_curve():
    title_font = {"family": "CMU Sans Serif",
                  "size": 32}

    main_font = {"family": "CMU Sans Serif",
                 "size": 22}

    plt.rcParams['font.size'] = 14

    treefile = open("linear-latest.tre")
    tree = TimeTree(treefile.readline())
    treefile.close()

    fm = lambda x: tree_likelihood(tree, lin_population, lin_probability, {"N0": x, "b": 1100})
    x = np.linspace(1, 2000, 1000)
    y = [fm(N0) for N0 in x]

    fig, ax = plt.subplots()

    ax.plot(x, y, color="#0072b2", linewidth=3)

    ax.set_xlabel("Value of N0", **main_font)
    ax.set_ylabel("Log likelihood of tree", **main_font)
    ax.set_title("Likelihood of N0 values with fixed B", **title_font)
    ax.set_xticks([1100, 1250, 1500, 1750, 2000])

    plt.show()

def plot_various_b():
    title_font = {"family": "CMU Sans Serif",
                  "size": 32}

    main_font = {"family": "CMU Sans Serif",
                 "size": 22}

    N0_list = [505, 1005, 2005, 3005] # TODO do all these work well? Like do they make sense?
    b_list = [5, 10, 20, 30]
    color_list = ["#e69f00", "#56b4e9", "#0072b2", "#d55e00"]
    
    plt.rcParams['font.size'] = 14
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(16, 8)

    time = np.linspace(0, 100, 1000)
    for N0, b, col in zip(N0_list, b_list, color_list):
        # "How does the population change over time?"
        population = [lin_population({"N0": N0, "b": b}, t) for t in time]
        # "Sampling from the end, what is the likelihood that our first coalescence event is at a certain time?"
        probability = [lin_probability({"N0": N0, "b": b, "k": 20}, z) for z in time]
        
        ax1.plot(-time, population, color=col, label=str(b))
        ax2.plot(time, probability, color=col, label=str(b))

    ax1.set_title("Population size over time", **title_font)
    ax1.set_xlabel("Time", **main_font)
    ax1.set_ylabel("Population size", **main_font)
    ax1.legend(title="Value of B")
    # TODO is there a way to do this that's more correct? I get a warning about FixedFormatter.
    ax1.set_xticklabels([0, 0, 20, 40, 60, 80, 100]) # Fake time to line up with expectations

    ax2.set_title("Expected time until first coalescence", **title_font)
    ax2.set_xlabel("Time back to first coalescence", **main_font)
    ax2.set_ylabel("Density", **main_font)
    ax2.legend(title="Value of B")

    plt.savefig("various-b.pdf")
    plt.show()

if __name__ == "__main__":
    #plot_constant_hdi()
    #plot_linear_lk_curve()
    plot_various_b()


