#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from population_models import con_probability, lin_probability, exp_probability, \
        con_population, lin_population, exp_population
from time_tree import TimeTree

#
# Breaking a tree into parts and finding k
#

def closest_node(tree, time):
    """
    Return the next node back from the specified time.
    """
    closest_node = tree
    for node in tree.traverse():
        if node.time < closest_node.time and node.time > time:
            closest_node = node
    return closest_node

def count_lineages(node, time):
    """
    Return the number of a node's children that exist at a certain time.
    """
    if time > node.time:
        raise Exception("Time must be after the node's own time")
    return len([n for n in node.iter_descendants() if n.time <= time < n.up.time])

def tree_segments(tree):
    """
    Divide a tree into segments based on where k changes
    (on coalescences or the introduction of new branches)
    """
    max_time = tree.time
    segments = []
    time = 0
    while time < max_time:
        next_node = closest_node(tree, time)
        segments.append((time, next_node.time))
        time = next_node.time
    return segments

#
# Log likelihood of an entire tree
#

def tree_likelihood(tree, population, probability, params):
    """
    Return the log likelihood of a certain tree existing
    based on the given population model and probability function.

    Required parameters:
      Any parameters the probability requires besides K
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        params["k"] = count_lineages(tree, (start+end)/2) # TODO should I just use start? or is middle good
        if params["k"] == 1:
            # TODO we actually need to handle this but I can't
            # it involves taking the integral of the probability function and stuff.
            pass
        else:
            log_likelihood += np.log(probability(params, end-start))
        if "N0" in params.keys():
            params["N0"] = population(params, end-start)
    return log_likelihood

#
# Find most likely parameter of a tree by trying many possible values and choosing the best
#

def likelihood_surface(tree, population, probability, params):
    """
    The likelihood surface of a tree with a certain model, one ranged parameter,
    and one fixed parameter.

    Parameters:
      tree        : TimeTree
      population  : con_- lin_- or exp_population
      probability : con_- lin_- or exp_probability
      params      : dictionary with two items
                    one should be an iterable parameter and the other should be fixed
    """
    likelihoods = []
    for p in params.keys():
        try:
            iter(params[p])
            ranged_name, ranged = p, params[p]
        except TypeError:
            fixed_name, fixed = p, params[p]

    for item in ranged:
        lk = tree_likelihood(tree, population, probability, \
                {ranged_name: item, fixed_name: fixed})
        likelihoods.append(lk)

    return likelihoods

if __name__ == "__main__":
    b_range = np.linspace(0, 1000, 10000)
    with open('linear.tre') as file:
        lines = file.readlines()
        for line in lines:
            t = TimeTree(line)
            y = likelihood_surface(t, lin_population, lin_probability, {"N0": 10000, "b": b_range})
            plt.plot(b_range, y)
            plt.show()

