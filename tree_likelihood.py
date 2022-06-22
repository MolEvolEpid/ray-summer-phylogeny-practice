#!/usr/bin/env python3

import numpy as np
from population_models import con_probability #, lin_probability, exp_probability
from time_tree import TimeTree

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
    return [n for n in node.traverse() if n.time <= time < n.up.time]

def tree_segments(tree):
    """
    Divide the tree into a list of segments based on where coalescences occur.
    """
    max_time = tree.time
    segments = []
    time = 0
    while time < max_time:
        next_parent = closest_parent_node(tree, time)
        segments.append((time, next_parent.time))
        time = next_parent.time
    return segments

def segment_log_likelihood(tree, start, end):
    """
    Return the log likelihood that a certain segment of the tree would coalesce the way
    it did, assuming an arbitrary population size of 1000.
    """
    k = len(children_at_time(tree, start))
    # TODO: when there are multiple start times this will be innaccurate
    N = 1000
    z = end - start
    return np.log(con_probability(k, N, z))

def tree_log_likelihood(tree):
    """
    Return the log likelihood that a certain tree exists (normal likelihood 
    may underflow to zero, which we don't want)
    """
    segments = tree_segments(tree)
    log_likelihood = 0
    for (start, end) in segments:
        log_likelihood += segment_log_likelihood(tree, start, end)
    return log_likelihood

if __name__ == "__main__":
    t = TimeTree("((A:1, B:1):2, C:3);")
    print(tree_log_likelihood(t))
    t.show()


