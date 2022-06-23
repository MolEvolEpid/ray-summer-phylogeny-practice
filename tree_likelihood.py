#!/usr/bin/env python3

import numpy as np
from population_models import con_probability, lin_probability, exp_probability
from time_tree import TimeTree

#
# Breaking a tree into parts and finding k
#

def closest_parent_node(tree, time):
    """
    Return the next closest node backwards from the specified time.
    (for instance, the next node inwards from the leaves at time 0)
    """
    closest_node = tree
    for node in tree.traverse():
        # Any candidates need to be:
        #     Sooner than the current best time
        #     Later than the target time
        #     Have children (not be a leaf)
        if node.time < closest_node.time and node.time > time and node.children:
            closest_node = node
    return closest_node

def closest_node(tree, time):
    closest_node = tree
    for node in tree.traverse():
        if node.time < closest_node.time and node.time > time:
            closest_node = node
    return closest_node

def children_at_time(node, time):
    """
    Return the number of a node's children that exist at a certain time.
    """
    if time >= node.time:
        raise Exception("Time must be after the node's own time")
    return [n for n in node.iter_descendants() if n.time <= time < n.up.time]

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

def count_lineages(tree, start, end):
    """
    Return the number of lineages between the given start and end times 
    """
    k = len(children_at_time(tree, (start+end)/2))
    return k

def con_tree_likelihood(tree, N):
    """
    The log likelihood of a certain tree existing, assuming a
    constant population of N(t) = N
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        k = count_lineages(tree, start, end)
        log_likelihood += np.log(con_probability(k, N, end-start))
    return log_likelihood

def lin_tree_likelihood(tree, N0, b):
    """
    The log likelihood of a certain tree existing, assuming a
    linear population of N(t) = N0 - bt
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        k = count_lineages(tree, start, end)
        log_likelihood += np.log(lin_probability(k, N0, b, end-start))
        N0 -= b*(end-start)
    return log_likelihood

def exp_tree_likelihood(tree, N0, r):
    """
    The log likelihood of a certain tree existing, assuming an
    exponential population of N(t) = N0 * e^-rt
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        k = count_lineages(tree, start, end)
        log_likelihood += np.log(exp_probability(k, N0, r, end-start))
        N0 *= np.exp(-r*(end-start))
    return log_likelihood

if __name__ == "__main__":
    t = TimeTree("(((a:1, a:1):2, a:3):2, (a:3, a:3):2);") # slightly more complex test case

    print(con_tree_likelihood(t, 1000))
    print(lin_tree_likelihood(t, 1000, 10))
    print(exp_tree_likelihood(t, 1000, 0.1))

    t.show()
    

