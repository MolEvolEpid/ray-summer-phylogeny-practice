#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from population_models import *
from tree_likelihood import *
from basic_optimization import *

# Fonts
title_font = {"family": "CMU Sans Serif",
              "size": 32}
main_font = {"family": "CMU Sans Serif",
             "size": 22}
small_font = {"family": "CMU Sans Serif",
              "size": 16}

# Colors
orange = "#E69F00"
lblue  = "#56B4E9"
green  = "#009E73"
yellow = "#F0E442"
dblue  = "#0072B2"
red    = "#D55E00"
pink   = "#CC79A7"
black  = "#000000"

def plot_constant_hdi():
    """
    Accuracy of our predictions of N0 on a constant model.

    BROKEN--WILL NOT WORK WITH NEW PARAMS.
    """
    plt.rcParams['font.size'] = 14
    tips_20 = bad_datafile_read(peak_infile="run/peaks_20.csv") # TODO generate these first
    tips_100 = bad_datafile_read(peak_infile="run/peaks_100.csv") 

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(16, 8)

    for ax, data in zip([ax1, ax2], [tips_20, tips_100]):
        N0, peaks = calculate_axes(data)
        hdi = calculate_error(data, error_hdi)

        ax.plot(N0, N0, color="#56b4e9")

        ax.scatter(N0, peaks, color=dblue, zorder=3, label="Mean of Maximum Likelihood Estimates")
        ax.errorbar(N0, peaks, yerr=hdi, fmt="none", color=red, zorder=2, capsize=5, label="95% Highest Density Interval")
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
    """
    The accuracy of our predictions of N0 when we fix b to be 
    a certain value.

    BROKEN--WILL NOT WORK WITH NEW PARAMS.
    """
    plt.rcParams['font.size'] = 14

    treefile = open("linear-latest.tre")
    tree = TimeTree(treefile.readline())
    treefile.close()

    fm = lambda x: tree_likelihood(tree, lin_population, lin_probability, {"N0": x, "b": 1100})
    x = np.linspace(1, 2000, 1000)
    y = [fm(N0) for N0 in x]

    fig, ax = plt.subplots()

    ax.plot(x, y, color=dblue, linewidth=3)

    ax.set_xlabel("Value of N0", **main_font)
    ax.set_ylabel("Log likelihood of tree", **main_font)
    ax.set_title("Likelihood of N0 values with fixed B", **title_font)
    ax.set_xticks([1100, 1250, 1500, 1750, 2000])

    plt.show()

def plot_various_b():
    """
    The time until the first coalescence occurs with models with
    various b.

    BROKEN--WILL NOT WORK WITH NEW PARAMS.
    """
    N0_list = [505, 1005, 2005, 3005] # TODO do all these work well? Like do they make sense?
    b_list = [5, 10, 20, 30]
    color_list = [orange, lblue, dblue, red]
    
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

def plot_single_tree_likelihood():
    """
    Plot the likelihood curves for several different segments
    on a tree and show how they line with what happened on the tree.
    """
    tree_ex = TimeTree("(D_3:462.54,(D_1:348.141,(D_2:43.4684,D_4:43.4684):304.673):114.399);")
    # The segments we care about:
    #   start=0       z=43.4684 with k=4, a=5, b=3.
    #   start=43.4684 z=304.673 with k=3, a=5, b=3
    #   start=448.141 z=114.399 with k=2, a=5, b=3

    segment_lk = lambda k, start, z: lin_probability({"k": k, "a": 5, "b": 4, "I": 2*(365/1.5)}, start, z)

    fig, ax = plt.subplots()

    for color, label, start, k in zip([green, orange, yellow], ['First segment', 'Second segment', 'Third segment'], [0., 43.4684, 348.141], [4, 3, 2]):
        t_range = np.linspace(2*(365/1.5), 0, 1000)
        #z_range = np.linspace(0, 2*(365/1.5)-start, 1000)
        z_range = np.linspace(0, 2*(365/1.5), 1000)

        lk = [segment_lk(k, start, z) for z in z_range]

        #ax.plot(t_range, lk, label=label)
        ax.fill_between(-t_range, lk, 0, label=label, color=color, alpha=0.5)

    ax.legend()
    ax.set_xticks([-500, -400, -300, -200, -100, 0])
    ax.set_xticklabels(['500', '400', '300', '200', '100', '0'], **small_font)
    ax.set_yticks([0, 0.05, 0.10, 0.15])
    ax.set_yticklabels(['0', '0.05', '0.10', '0.15'], **small_font)
    ax.set_xlabel("Time (generations)", **main_font)
    ax.set_ylabel("Coalescence likelihood", **main_font)
    plt.show()

        


if __name__ == "__main__":
    #plot_constant_hdi()
    #plot_linear_lk_curve()
    #plot_various_b()
    plot_single_tree_likelihood()

