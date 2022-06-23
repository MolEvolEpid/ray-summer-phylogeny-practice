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

def children_at_time(node, time):
    """
    Return the number of a node's children that exist at a certain time.
    """
    if time >= node.time:
        raise Exception("Time must be after the node's own time")
    return [n for n in node.iter_descendants() if n.time <= time < n.up.time]

def tree_segments(tree):
    """
    Divide the tree into a list of segments based on where coalescences occur.
    """
    # TODO needs a rework
    max_time = tree.time
    segments = []
    time = 0
    while time < max_time:
        next_parent = closest_parent_node(tree, time)
        segments.append((time, next_parent.time))
        time = next_parent.time
    return segments

#
# Log likelihood of a certain segment of a tree
#

def con_segment_likelihood(tree, N, start, end):
    """
    Return the log likelihood that a certain segment of the tree would coalesce the way
    it did, assuming constant population.
    """
    k = len(children_at_time(tree, start))
    z = end - start
    #print(f"({start}, {end}) k={k} N={N} z={z}")
    return np.log(con_probability(k, N, z))

def lin_segment_likelihood(tree, N, b, start, end):
    """
    Return the log likelihood that a certain segment of the tree would coalesce the way
    it did, assuming linear population.
    """
    k = len(children_at_time(tree, start))
    z = end - start
    #print(f"({start}, {end}) k={k} N={N} z={z}")
    return np.log(lin_probability(k, N, b, z))

def exp_segment_likelihood(tree, N, r, start, end):
    """
    Return the log likelihood that a certain segment of the tree would coalesce the way
    it did, assuming exponential population.
    """
    k = len(children_at_time(tree, start))
    z = end - start
    #print(f"({start}, {end}) k={k} N={N} z={z}")
    return np.log(exp_probability(k, N, r, z))
#
# Log likelihood of an entire tree
#

def con_tree_likelihood(tree, N):
    """
    The log likelihood of a certain tree existing, assuming a
    constant population of N(t) = N
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        segment_likelihood = con_segment_likelihood(tree, N, start, end)
        log_likelihood += segment_likelihood
        #print(f"  {segment_likelihood}")
    return log_likelihood

def lin_tree_likelihood(tree, N0, b):
    """
    The log likelihood of a certain tree existing, assuming a
    linear population of N(t) = N0 - bt
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        segment_likelihood = lin_segment_likelihood(tree, N0, b, start, end)
        log_likelihood += segment_likelihood
        #print(f"  {segment_likelihood}")
        N0 -= b*(end-start)
    return log_likelihood

def exp_tree_likelihood(tree, N0, r):
    """
    The log likelihood of a certain tree existing, assuming an
    exponential population of N(t) = N0 * e^-rt
    """
    log_likelihood = 0
    for (start, end) in tree_segments(tree):
        #N = N0 * np.exp(-r*(end-start))
        segment_likelihood = exp_segment_likelihood(tree, N0, r, start, end)
        log_likelihood += segment_likelihood
        #print(f"  {segment_likelihood}")
        N0 *= np.exp(-r*(end-start))
    return log_likelihood

if __name__ == "__main__":
    t = TimeTree("(((a:1, a:1):2, a:3):2, (a:3, a:3):2);")

    print(exp_tree_likelihood(t, 1000, 0.1))

