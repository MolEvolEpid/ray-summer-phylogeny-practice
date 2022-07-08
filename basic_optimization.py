#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv
from time_tree import TimeTree
from tree_likelihood import tree_likelihood
from tree_generation import generate_tree
from scipy.optimize import minimize_scalar
from arviz import hdi
# TODO I eventually wanna support lin and exp too, but I can only generate con right now.
from population_models import con_probability, con_population, \
                              lin_probability, lin_population, \
                              exp_probability, exp_population

#
# Find max with an optimization tool
#

def max_log_lk(tree):
    """
    Maximize the log likelihood for a tree by manipulating N0. Can only be used
    for constant model, so I've hardcoded that in for now.
    """
    fm = lambda x: -tree_likelihood(tree, con_population, con_probability, {"N0": x}) 
    #res = minimize_scalar(fm, method="brent")
    res = minimize_scalar(fm, bracket=(100, 10000), method="brent")
    return res.x

#
# Input and output data files since these models can take a while to run
#

def generate_data(k_range, replicates=100, outfile=None):
    """
    Generate trees using the parameters provided, returning a dict
    of the parameters tested or writing the data to a CSV file.
    """
    data = {}
    for k in k_range:
        print(f"\n\nNEW K SELECTED: {k}")
        run_params = {"N0": 1000, "k": k}
        rep_peaks = []
        for _ in range(replicates):
            print(f"  replicate {_}")
            t = TimeTree(generate_tree(con_population, run_params))
            rep_peaks.append(max_log_lk(t))
        data[k] = rep_peaks

    if outfile:
        with open(outfile, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["k", "peak_data"])
            writer.writeheader()
            for key, value in data.items():
                writer.writerow({"k": key, "peak_data": value})
    else:
        return data

def read_datafile(infile):
    """
    Read data from a file containing k and peaks information 
    and return a dictionary.
    """
    data = {}
    with open(infile, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Turn strings back into the types of data we want
            k = int(row["k"])
            peaks = [float(peak) for peak in row["peak_data"].strip('][').split(', ')]
            data[k] = peaks
    return data

#
# Calculate the error between peak measurements in various ways
#

def error_stdev(peaks):
    """
    Find the standard deviation among the peaks and
    return it as symmetrical error.
    """
    n = len(peaks)
    mean = sum(peaks) / n
    var = sum((x - mean)**2 for x in peaks) / n
    return 1.96 * var ** 0.5

def error_hdi(peaks):
    """
    Find the HDI (highest density interval) among the peaks
    and return it. Error may be asymmetrical.
    """
    low, high = hdi(np.array(peaks), hdi_prob=.95)
    mean = sum(peaks) / len(peaks)
    return np.array([mean - low, high - mean])

def error_listdrop(peaks):
    """
    Find a bootleg version of the HDI by sorting the list of peaks
    and dropping the first and last 2.5% of the items (rounded).
    Error can be asymmetrical, but is not necessarily
    """
    to_drop = round(.025 * len(peaks))
    peaks.sort()
    mean = sum(peaks) / len(peaks)
    trimmed = peaks[to_drop:-to_drop]
    return np.array([mean - trimmed[0], trimmed[-1] - mean])

def calculate_axes(data):
    """
    Turn a data dictionary into two lists -- one of k values,
    the other of mean peak positions.
    """
    k_values = []
    est_population = []
    for k, peaks in data.items():
        k_values.append(k)
        est_population.append(sum(peaks) / len(peaks))
    return k_values, est_population

def calculate_error(data, error_fun):
    """
    Turn a data dictionary into a list of errors using the specified
    error_fun.
    """
    error = []
    for peaks in data.values():
        error.append(error_fun(peaks))
    error_array = np.array(error)
    return np.transpose(error_array)

#
# Plot a nice-ish graph with all three different types of error
#

def plot_all_errors():
    # Data should already be generated
    # Uncomment line in __main__ below to generate it
    data = read_datafile("run.csv")
    
    # Find points and error
    x, y = calculate_axes(data)
    stdev = calculate_error(data, error_stdev)
    hdi = calculate_error(data, error_hdi)
    listdrop = calculate_error(data, error_listdrop)

    # Plot and label all of them
    fig, ax = plt.subplots()
    ax.scatter(x, y, color="#003049", zorder=3)
    ax.errorbar(x, y, yerr=stdev, fmt="none", color="#D62828", label="stdev", capsize=5, zorder=2)
    ax.errorbar(x, y, yerr=hdi, fmt="none", color="#F77F00", label="hdi", capsize=5, zorder=1)
    ax.errorbar(x, y, yerr=listdrop, fmt="none", color="#FCBA36", label="listdrop", capsize=5, zorder=0)
    ax.axhline(y=1000, color="#4DA1A9", linestyle="-", zorder=3)

    # Labeling
    ax.set_xticks(x)
    ax.set_title("Population prediction on constant-population trees (N=1000)")
    ax.set_xlabel("Value of k")
    ax.set_ylabel("Predicted population")
    ax.legend()

    plt.show()

if __name__ == "__main__":
    #generate_data([5, 10, 20, 40, 60, 80, 100], outfile="run.csv", replicates=200)
    plot_all_errors()
