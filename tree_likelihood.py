#!/usr/bin/env python3

import numpy as np
from time_tree import TimeTree
from tree_generation import generate_tree
from population_models import con_probability, lin_probability, exp_probability, \
        con_population, lin_population, exp_population

#
# Log likelihood of an entire tree
#

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

def tree_likelihood(tree, population, probability, params):
    """
    Return the log likelihood of a tree existing based
    on the given population model and probability function.
    """
    log_likelihood = 0
    params_now = params.copy()
    params_now["k"] = len(tree.get_leaves()) # TODO later will need to by by group
    for (start, end, dist) in tree_segments(tree):
        params_now["N0"] = population(params, start)
        if params_now["k"] == 1:
            print("WARNING: k was 1")
        else:
            #print(f"trying with {params_now}, {dist}")
            segment_lk = np.log(probability(params_now, dist))
            #print(f"    {segment_lk}")
            log_likelihood += segment_lk
        params_now["k"] -= 1
    return log_likelihood

#
# Test many points' likelihood. Also nice for plotting
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
