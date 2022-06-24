#!/usr/bin/env python3

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

if __name__ == "__main__":
    t = TimeTree("(((a:1, a:1):2, a:3):2, (a:3, a:3):2);") # slightly more complex test case
    t2 = TimeTree("((a:4, a:2):1, a:3);")

    print(tree_likelihood(t, con_population, con_probability, {"N": 1000}))
    print(tree_likelihood(t, lin_population, lin_probability, {"N0": 1000, "b": 10}))
    print(tree_likelihood(t, exp_population, exp_probability, {"N0": 1000, "r": 0.1}))

    t2.show()
    

