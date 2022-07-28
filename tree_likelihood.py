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
    
    coalescence = {0: [], 1: []} # Start, end, and dist for each segment
    no_coalescence = {0: [], 1: []}
    parents = {0: set(), 1: set()} # For coalescing nodes, which parents have we already seen?

    def add_coalescence(node, host, start, end):
        """
        Add a coalescence event to the dictionary
        if one has not already been added with the
        same parent.
        """
        if node.up not in parents[host]:
            coalescence[host].append((start, end, end-start))
            parents[host].add(node.up)

    # Find the state of every branch on the tree and assign it to the
    # correct location.
    for node in tree.iter_descendants():
        start = node.time
        end = node.up.time

        # Try to assign a host. 0 before transmission, based on leaves after
        if start <= T:
            try:
                if node.children:
                    host = node.get_leaves()[0].host
                else:
                    host = node.host
                #print(f"chose host as {host} for {node}")
            except AttributeError:
                print("Could not determine host of leaf. Do all leaves have a host attribute?")
                raise
        else:
            #print(f"auto assigned host as 0 for {node}")
            host = 0

        if end >= T > start:
            no_coalescence[host].append((start, T, T-start))
            add_coalescence(node, 0, T, end) # always host 0 because that half is in donor
        else:
            add_coalescence(node, host, start, end)

    # Sort segments by start time 
    coal_D = coalescence[0]
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

