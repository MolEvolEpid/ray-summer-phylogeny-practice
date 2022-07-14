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
# Optimize one parameter of a tree
#

def generate_likelihood_function(tree, target_param, fixed_params):
    """
    Based on the name of the target parameter and the name and value of 
    any fixed parameters, return a lambda function that takes the target_param
    as input and outputs the corresponding likelihood.

    Parameters:
      target_param (str): "N0", "b", or "r"
      fixed_params (dict): Dictionary with one item, 
        giving the name and value of the fixed parameter.

    Returns:
      fm (function): Single-parameter function returning the probability of a tree at
        a certain parameter value.
    """
    fixed_names = [name for name in fixed_params.keys()]
    # Constant - N0
    if target_param == "N0" and not fixed_names:
        pop, prob = con_population, con_probability
        fm = lambda x: tree_likelihood(tree, pop, prob, {"N0": x})
    # Linear - N0
    elif target_param == "N0" and "b" in fixed_names:
        pop, prob = lin_population, lin_probability
        fm = lambda x: tree_likelihood(tree, pop, prob, {"N0": x, "b": fixed_params["b"]})
    # Exponential - N0
    elif target_param == "N0" and "r" in fixed_names:
        pop, prob = exp_population, exp_probability
        fm = lambda x: tree_likelihood(tree, pop, prob, {"N0": x, "r": fixed_params["r"]})
    # Linear - b
    elif target_param == "b" and "N0" in fixed_names:
        pop, prob = lin_population, lin_probability
        fm = lambda x: tree_likelihood(tree, pop, prob, {"b": x, "N0": fixed_params["N0"]})
    # Exponential - r
    elif target_param == "r" and "N0" in fixed_names:
        pop, prob = exp_population, exp_probability
        fm = lambda x: tree_likelihood(tree, pop, prob, {"r": x, "N0": fixed_params["N0"]})
    else:
        raise Exception(f"Could not find the correct function for target {target_param} and fixed {fixed_names}. Maybe Ray forgot to add them?")
    return fm

def max_likelihood(tree, target_param, fixed_params={}, output_val=False):
    """
    Use single-parameter optimization to find the most likely value of a target param
    with relation to a tree.

    Parameters:
      tree (TimeTree): Representation of the tree in memory
      target_param (str): The parameter you want to optimize. Can be "N0", "b", or "r".
      fixed_params (dict): Optional dict of fixed values. Each entry should contain
        the name of a fixed param as the key and its value. If no fixed_params is
        provided, a constant model will be assumed.
      output_val (bool): Whether or not to also return the likelihood value at the
        optimized position. Defaults to false.
    """
    lk_func = generate_likelihood_function(tree, target_param, fixed_params)
    fm = lambda x: -lk_func(x)
    res = minimize_scalar(fm, bracket=(2, 100), method="brent")
    if output_val:
        return res.x, lk_func(res.x)
    else:
        return res.x

def confidence_bounds(tree, target_param, fixed_params={}):
    """
    Return the upper and lower bounds on the 95% confidence interval of a tree.
    """
    peak_pos, peak_val = max_likelihood(tree, target_param, fixed_params, output_val=True)
    lk_func = generate_likelihood_function(tree, target_param, fixed_params)
    fm = lambda x: lk_func(x) - peak_val + 1.92 # Has x-intercepts at peak_val - 1.92 
    low_ci = brentq(fm, 1e-10, peak_pos)
    high_ci = brentq(fm, peak_pos, 10*peak_pos)
    print(f"  {low_ci} {peak_pos} {high_ci}")
    return low_ci, high_ci

#
# Input and output data files since these models can take a while to run
#

def write_con_datafiles(k_range, replicates=100, peak_outfile=None, width_outfile=None):
    """
    Generate trees using the parameters provided, writing the peaks and 
    confidence intervals of the tree to the specified output files.

    WARNING: Only uses a constant population model.
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
            peak_pos = maximize_N0(t)
            peaks_out[k].append(peak_pos)
            widths_out[k].append(confidence_width_N0(t, peak_pos))

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

if __name__ == "__main__":
    pass
