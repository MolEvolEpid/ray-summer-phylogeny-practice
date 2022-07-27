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
      donor_segments (list): All segments which happen in the donor, 
        including those between T and the root of the tree.
      recip_segments (list): All segments which occur entirely in the
        recipient, not counting those that cross over T.
      tmiss_segments (list): All segments which cross over the transmission
        time T, from the recipient to the donor.
    """
    # TODO For this, I rely on having each leaf have a host attribute that is 0 or 1.
    # I have a way to calculate these, but I was fighting with the class to get it
    # to calculate that upon creation of the object.

    t.populate_hosts({"D": 0, "R": 1}) # Overwrite any existing host data for what we'll use

    for node in tree.iter_descendants():
        coal_D = [] # Intervals where coalescences occur normally
        coal_R = []
        none_D = [] # Intervals where no coalescence occurs
        none_R = []

        # The start and end of the branch from this node back
        branch_start = node.up.time
        branch_end = node.time

        # T is in the middle of the branch
        # We need to spli everything up. But how? 
        if branch_start >= T > branch_end:
            if node_host == 0:
                none = none_D
            elif node_host == 1:
                none = none_R
            else:
                raise Exception("Host was neither 0 or 1. This should not have happened.")
            none.append((branch_start, T, T-branch_start))
            coal_D.append((T, branch_end, branch_end-T)) # Other side is always in D
        # Chronologically after T (towards tips)
        # The children will all be of the same host, so we only need to check one
        elif branch_start < T and branch_end < T:
            if node_host == 0:
                coal_D.append((branch_start, branch_end, branch_end-branch_start))
            elif node_host == 1:
                coal_R.append((branch_start, branch_end, branch_end-branch_start))
            else:
                raise Exception("Host was neither 0 or 1. This should not have happened.")
        # Chronologically before T (towards root)
        # These branches always have to be contained in the donor.
        elif branch_start >= T and branch_end >= T:
            coal_R.append((branch_start, branch_end, branch_end-branch_start))

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

