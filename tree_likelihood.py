import numpy as np
import warnings
from time_tree import TimeTree
from population_models import *

def tree_segments(tree, start=0):
    """
    Divide a tree into segments based on the location of parent
    nodes (coalescence events)
    
    Parameters:
      tree (TimeTree): Tree with a single host and tips at the same time
      start (float, default 0): Initial time value

    Returns:
      segments (list): Tuples containing a start, end, and dist for each segment.
    """
    node_times = [start]
    for node in tree.traverse():
        if node.children:
            node_times.append(node.time)
    node_times.sort()

    segments = []
    for start, end in zip(node_times, node_times[1:]):
        segments.append((start, end, round(end-start, 5)))
    return segments

def tree_segments_multihost(tree, T):
    """
    Divide a tree into three types of segments: Those that occur entirely in either 
    the donor or the recipient and those that occur across the transmission time.

    Parameters:
      tree (TimeTree): ete3 representation of a tree with time values.
      T (float): Time of transmission between donor and recipient. 
        Also can be written As I_R (I sub R)

    Returns:
      coal_D (list): Segments with a coalescence in the donor
      coal_R (list): Segments with a coalescence in the recipient
      none_D (list): Segments without a coalescence in the donor
      none_R (list): Segments without a coalescence in the recipient
    """
    tree.populate_hosts({"D": 0, "R": 1}) # Overwrite any existing host data for what we'll use here
    before, after = tree.split_at_time(T)
    
    coalescence = {0: [], 1: []} # Start, end, and dist for each segment
    no_coalescence = {0: [], 1: []}
    parents = {0: set(), 1: set()} # For coalescing nodes, which parents have we already seen?

    def add_coalescence(node, host, start, end):
        """Add a coalescence event to the relevant list, but only if there
        is not already one with the same host."""
        if node.up not in parents[host]:
            coalescence[host].append((start, end, round(end-start, 5)))
            parents[host].add(node.up)

    for fragment in after:
        try:
            if fragment.children:
                host = fragment.get_leaves()[0].host
            else:
                host = fragment.host
        except AttributeError:
            print("Could not find a host for one of the tree fragments. Please check that all tree tips have hosts.")
            raise

        frag_start = fragment.time
        frag_end = fragment.time + fragment.dist
        no_coalescence[host].append((frag_start, frag_end, round(frag_end-frag_start, 5)))

        for node in fragment.iter_descendants():
            start = node.time
            end = node.up.time
            add_coalescence(node, host, start, end)

    # Sort segments by start time 
    coal_D = coalescence[0] + tree_segments(before, start=T)
    coal_R = coalescence[1]
    none_D = no_coalescence[0]
    none_R = no_coalescence[1]
    for l in [coal_D, coal_R, none_D, none_R]:
        l.sort(key = lambda x: x[0])

    return coal_D, coal_R, none_D, none_R

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

