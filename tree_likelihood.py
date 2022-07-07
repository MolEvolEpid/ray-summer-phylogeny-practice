#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from time_tree import TimeTree
from tree_generation import generate_tree
from scipy.optimize import minimize_scalar, brentq
from arviz import hdi
from population_models import con_probability, lin_probability, exp_probability, \
        con_population, lin_population, exp_population

#
# Breaking a tree into parts and finding k
#

def within_tolerance(t1, t2):
    """
    Return whether or not two times are close enough to each other
    to be counted as the same sampling group.
    """
    return t1 - 0.003 <= t2 <= t1 + 0.003

def closest_parent_node(tree, time):
    """
    Return the next parent node back from the specified time.
    """
    closest = tree
    for node in tree.traverse():
        if node.time < closest.time and node.time > time and node.children:
            closest = node
    return closest

def sampling_groups(tree):
    """
    Organize the leaves of a tree by groups sampled at approximately
    the same time to avoid issues with floating point precision.
    """
    groups = []
    for leaf in tree.iter_leaves():
        for group in groups:
            if within_tolerance(group[0].time, leaf.time):
                group.append(leaf)
                break
        # If the leaf isn't in any groups, add it to a new one
        if not any(leaf in group for group in groups):
            groups.append([leaf])
    return groups

def count_lineages(tree, time):
    """
    Return the number of nodes at a certain time,
    accounting for sampling groups.
    """
    if time > tree.time:
        raise Exception("Time must be after the tree time")
    for group in sampling_groups(tree):
        if within_tolerance(group[0].time, time):
            # TODO this won't hold up if we have more than one group since we should
            # also add anything else that exists at the time
            return len(group)
    return len([n for n in tree.iter_descendants() if n.time <= time < n.up.time])

def tree_segments(tree):
    """
    Divide a tree into segments based on the location of parent
    nodes.
    """
    node_times = [0]
    for node in tree.traverse():
        if node.children:
            node_times.append(node.time)
    node_times.sort()

    segments = []
    for start, end in zip(node_times, node_times[1:]):
        segments.append((start, end, end-start))
    return segments

#
# Log likelihood of an entire tree
#

def tree_likelihood(tree, population, probability, params):
    """
    Return the log likelihood of a certain tree existing
    based on the given population model and probability function.

    Required parameters:
      Any parameters the probability requires besides k
    """
    log_likelihood = 0
    for (start, end, dist) in tree_segments(tree):
        # Find the parameters at the current step in time
        params_now = params.copy()
        params_now["k"] = count_lineages(tree, start)
        params_now["N0"] = population(params, start)

        if params_now["k"] == 1:
            # TODO we actually need to handle this
            print("WARNING: k was 1")
        else:
            segment_lk = np.log(probability(params_now, dist))
            log_likelihood += segment_lk
    return log_likelihood

#
# Find most likely parameter of a tree by trying many possible values and choosing the best
#

def likelihood_surface(tree, population, probability, params):
    """
    The likelihood surface of a tree with a certain model, one ranged parameter,
    and one fixed parameter.

    Parameters:
    pass
      tree        : TimeTree
      population  : con_- lin_- or exp_population
      probability : con_- lin_- or exp_probability
      params      : dictionary with two items
                    one should be an iterable parameter and the other should be fixed
    """
    # Figure out what the parameters are
    # Will totally break if there is more than one iterable and one non-iterable
    for key in params:
        try:
            iter(params[key])
            ranged_name = key
            ranged = params[key]
        except TypeError:
            fixed_name = key
            fixed = params[key]

    # Generate a likelihood for each point
    likelihoods = [tree_likelihood(tree, population, probability, \
        {ranged_name: r, fixed_name: fixed}) for r in ranged]
    return likelihoods

#
# Finding max value and confidence intervals based on the probability
# function of a certain tree
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

def error_stdev(peaks):
    n = len(peaks)
    mean = sum(peaks) / n
    var = sum((x - mean)**2 for x in peaks) / n
    stdev = var ** 0.5
    return stdev # maybe [mean - stdev, mean + stdev]

def error_hdi(peaks):
    return hdi(peaks, hdi_prob=.95)

def error_fake(peaks):
    return 3 # or maybe I should return [mean - 3, mean + 3]? I don't know

def changing_k(k_range, error_fun):
    data = []
    error = []
    for k in k_range:
        run_params = {"N0": 1000, "k": k}
        rep_peaks = []
        for _ in range(150):
            t = TimeTree(generate_tree(con_population, run_params))
            rep_peaks.append(max_log_lk(t))
        data.append(sum(rep_peaks) / len(rep_peaks))
        error.append(error_fun(rep_peaks))
    return data, error

if __name__ == "__main__":
    k_range = [5, 10, 20, 40, 60]
    error_fun = error_fake
    data, error = changing_k(k_range, error_fun)
    
    fig, ax = plt.subplots()
    ax.errorbar(k_range, data, yerr=error, fmt='o')
    ax.set_xticks(k_range)
    ax.set_title("Likelihood of constant population trees, N0 = 1000")
    plt.show()


