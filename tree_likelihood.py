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
        params["k"] = count_lineages(tree, (start+end)/2)
        if params["k"] == 1:
            pass
        else:
            log_likelihood += np.log(probability(params, end-start))
        if "N0" in params.keys():
            params["N0"] = population(params, end-start)
    return log_likelihood

#
# Find most likely parameter of a tree by trying many possible values and choosing the best
#

def con_likelihood_surface(tree, N_range):
    """
    Create a likelihood surface for a tree. IDK what to do at all hellllppppp
    """
    likelihoods = []
    for N in N_range:
        likelihoods.append(tree_likelihood(tree, con_population, con_probability, {"N": N}))
    return likelihoods

def likelihood_surface(tree, population, probability, fixed, ranged):
    """
    I don't know yet

    Parameters:
      tree        : TimeTree
      population  : con_- lin_- or exp_population
      probability : con_- lin_- or exp_probability
      fixed       : tuple with string name and value
      ranged      : tuple with string name and list of values
    """
    likelihoods = []
    for item in ranged[1]:
        likelihoods.append(tree_likelihood(tree, population, probability, \
                {ranged[0]: item, fixed[0]: fixed[1]})) # we need to provide a fake "fixed" value for con
    return likelihoods


if __name__ == "__main__":
    x = np.linspace(10, 10000, 10000)
    with open('linear.tre') as file:
        lines = file.readlines()
        for line in lines:
            t = TimeTree(line)
            y = [tree_likelihood(t, lin_population, lin_probability, {"N0": 10000, "b": b}) for b in x]
            plt.plot(x, y)
            plt.show()

