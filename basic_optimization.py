#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv
from time_tree import TimeTree
from tree_likelihood import tree_likelihood
from tree_generation import generate_tree
from scipy.optimize import minimize_scalar, brentq
from arviz import hdi
# TODO I eventually wanna support lin and exp too, but I can only generate con right now.
from population_models import con_probability, con_population, \
                              lin_probability, lin_population, \
                              exp_probability, exp_population

#
# Find info about a single tree (peak, confidence interval width)
#

def max_log_lk(tree):
    """
    Maximize the log likelihood for a tree by manipulating N0. Can only be used
    for constant model, so I've hardcoded that in for now.
    """
    fm = lambda x: -tree_likelihood(tree, con_population, con_probability, {"N0": x}) 
    res = minimize_scalar(fm, bracket=(100, 10000), method="brent")
    return res.x

def confidence_width(tree, peak_pos):
    """
    Return the width of the 95% confidence interval of a tree,
    given the value of the peak likelihood.
    """
    peak_val = tree_likelihood(tree, con_population, con_probability, {"N0": peak_pos})
    
    # A function that has its roots at peak - 2 so I can find the roots
    fm = lambda x: tree_likelihood(tree, con_population, con_probability, {"N0": x}) - peak_val + 2

    low_ci = brentq(fm, 1e-10, peak_pos)
    high_ci = brentq(fm, peak_pos, 100*peak_pos)
    return high_ci - low_ci

#
# Input and output data files since these models can take a while to run
#

def write_datafiles(k_range, replicates=100, peak_outfile=None, width_outfile=None):
    """
    Generate trees using the parameters provided, writing the peaks and 
    confidence intervals of the tree to the specified output files.
    """
    # Generate a bunch of trees and extract their data
    peaks_out = {}
    widths_out = {}
    for k in k_range:
        print(f"\n\nNEW K SELECTED: {k}")
        run_params = {"N0": 1000, "k": k}
        peaks_out[k] = []
        widths_out[k] = []
        for _ in range(replicates):
            print(f"  replicate {_}")
            t = TimeTree(generate_tree(con_population, run_params))
            peak_pos = max_log_lk(t)
            peaks_out[k].append(peak_pos)
            widths_out[k].append(confidence_width(t, peak_pos))

    # Write to either or both of the outfiles 
    for outfile, dictionary, data_title in zip([peak_outfile, width_outfile], 
                                               [peaks_out, widths_out], 
                                               ["peaks", "widths"]):
        if outfile:
            with open(outfile, "w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["k", data_title])
                writer.writeheader()
                for k, values in dictionary.items(): 
                    writer.writerow({"k": k, data_title: values})

def read_datafiles(peak_infile=None, width_infile=None):
    """
    Read data and trees from up to two files, returning a dictionary for each of them.
    If only one file is specified, only one dictionary will be returned.
    """
    if not peak_infile and width_infile:
        raise Exception("You must specify at least one file to be read.")
    peaks = {}
    widths = {}
    string_to_list = lambda s: s.strip('][').split(', ')
    for infile, dictionary in zip([peak_infile, width_infile], [peaks, widths]):
        if infile:
            with open(infile) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    k = int(row["k"])
                    try:
                        data_row = [float(peak) for peak in string_to_list(row["peaks"])]
                    except KeyError: # no column titled "peaks"
                        data_row = [float(width) for width in string_to_list(row["widths"])]
                    dictionary[k] = data_row
    to_return = [d for d in [peaks, widths] if d]
    if len(to_return) == 1:
        return to_return[0]
    else:
        return to_return

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
    peaks = read_datafiles(peak_infile="run/peaks.csv")
    
    # Find points and error
    x, y = calculate_axes(peaks)
    stdev = calculate_error(peaks, error_stdev)
    hdi = calculate_error(peaks, error_hdi)
    listdrop = calculate_error(peaks, error_listdrop)

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

def plot_error_vs_width():
    peaks, widths = read_datafiles(peak_infile="run/peaks.csv", width_infile="run/widths.csv")

    # Find error using HDI method
    hdi = calculate_error(peaks, error_hdi)
    hdi_dist = [above + below for [below, above] in hdi.transpose()]
    # Find the average width for each k in the tree
    mean_widths = [sum(w) / len(w) for w in widths.values()]

    # Plotting
    fig, ax = plt.subplots()
    x = list(peaks.keys())
    ax.scatter(x, hdi_dist, label="Between trees (HDI)", color="#D62828")
    ax.scatter(x, mean_widths, label="Within trees (95% CI)", color="#FCBA36")

    ax.set_xticks(x)
    ax.set_title("Difference in variation within and between trees")
    ax.set_xlabel("Value of k")
    ax.set_ylabel("Mean variation")
    ax.legend()

    plt.show()

if __name__ == "__main__":
    #write_datafiles([5, 10, 20, 40, 60, 80, 100], peak_outfile="run/peaks.csv", width_outfile="run/widths.csv", replicates=200)
    plot_error_vs_width()
    #plot_all_errors()
