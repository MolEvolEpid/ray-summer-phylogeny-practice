import numpy as np
import warnings
from time_tree import TimeTree
from population_models import *

#
# Log likelihood of an entire tree
#

def tree_segments(tree):
    """
    Divide a tree into segments based on the location of parent
    nodes (coalescence events)
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
    params_now = params.copy()

    log_likelihood = 0
    params_now["k"] = len(tree.get_leaves())

    if params_now['b'] < 0:
        return -np.inf
    elif params_now['a'] < 0:
        return -np.inf
    # we will also eventually want a bound on I, but it doesn't make sense to have one now.

    for (start, end, dist) in tree_segments(tree):
        if params_now["k"] == 1:
            warning.warn(f"WARNING: k was 1 between {start} and {start+dist}. The code can't handle this yet.")
        else:
            segment_lk = np.log(probability(params_now, start, dist))
            if np.isnan(segment_lk):
                warnings.warn("WARNING: segment likelihood came out as nan. You found a case that bypasses the existing bounds.")
            log_likelihood += segment_lk
        params_now["k"] -= 1
    return log_likelihood

