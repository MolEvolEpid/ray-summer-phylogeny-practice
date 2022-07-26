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
    # Make sure the tree starts at or after I. If not, warn the user.
    if params['I'] < tree.time:
        warnings.warn(f"Tree time {tree.time} was further back than transmission time {params['I']}")

    # Check params are valid, return -inf if they are not.
    # Does not raise warnings, as it is meant to work with an optimizer.
    if 'b' in params: # Linear model
        if params['b'] <= 0:
            return -np.inf
        if params['a'] < 0:
            return -np.inf
    elif 'N' in params: # Constant model
        if params['N'] <= 0:
            return -np.inf
    else: # Neither model fits -> raise an error
        raise Exception("params contained neither b nor N, so a population model could not be determined.")

    # If we've not had any issues yet, find the probability step by step
    params_now = params.copy()
    log_likelihood = 0
    params_now["k"] = len(tree.get_leaves()) # TODO this will not work when we have multiple hosts

    for (start, end, dist) in tree_segments(tree):
        segment_lk = np.log(probability(params_now, start, dist))
        if params_now["k"] == 1: # TODO is this check still necessary?
            warnings.warn(f"Only one node from {start} to {end}. Not sure what's happening.")
        if end > params_now["I"]:
            warnings.warn(f"Tree node at {end} was beyond I {params_now['I']}. We should have 2 hosts but don't.")
        if np.isnan(segment_lk):
            warnings.warn(f"Segment likelihood was nan from {start} to {end}. This didn't get caught already.") # TODO should no longer be necessary
        log_likelihood += segment_lk
        params_now["k"] -= 1

    return log_likelihood

