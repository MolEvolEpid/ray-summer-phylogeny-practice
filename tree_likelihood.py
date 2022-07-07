#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from time_tree import TimeTree
from tree_generation import generate_tree
from scipy.optimize import minimize_scalar, brentq
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

def max_log_lk(tree):
    """
    Maximize the log likelihood for a tree by manipulating N0. Can only be used
    for constant model, so I've hardcoded that in for now.
    """
    fm = lambda x: -tree_likelihood(tree, con_population, con_probability, {"N0": x}) 
    res = minimize_scalar(fm, bounds=(100, 10000), method="bounded")
    return res.x, -fm(res.x)

def confidence_intervals(tree):
    """
    Return the 95% confidence intervals for a tree, along with its peak.
    """
    peak, peak_value = max_log_lk(tree)
    # Weird function that has it roots at peak - 2
    fm = lambda x: tree_likelihood(tree, con_population, con_probability, {"N0": x}) - peak_value + 2
    # TODO I'm sure there's a better way to decide these bounds 
    low_ci = brentq(fm, 1e-10, peak) # TODO this throws a log(0) error but doesn't seem to hurt the result
    high_ci = brentq(fm, peak, 2*peak) 
    return((peak, low_ci, high_ci))

if __name__ == "__main__":
    t = TimeTree("tmp.tmp")
    #t = TimeTree("linear.tre")
    (peak, low_ci, high_ci) = confidence_intervals(t)
    print(f"low {low_ci} peak {peak} high {high_ci}")
