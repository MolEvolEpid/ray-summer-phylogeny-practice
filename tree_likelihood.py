#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from population_models import con_probability, lin_probability, exp_probability, \
        con_population, lin_population, exp_population
from time_tree import TimeTree

#
# Breaking a tree into parts and finding k
#

def closest_parent_node(tree, time):
    """
    Return the next parent node back from the specified time.
    """
    closest = tree
    for node in tree.traverse():
        if node.time < closest.time and node.time > time and node.children:
            closest = node
    return closest

def sampling_groups(tree):
    """
    Organize the leaves of a tree by groups sampled at approximately
    the same time to avoid issues with floating point precision.
    """
    groups = []
    for leaf in tree.iter_leaves():
        for group in groups:
            if (group[0].time - 0.005) <= leaf.time <= (group[0].time + 0.005):
                group.append(leaf)
                break
        # If the leaf isn't in any groups, add it to a new one
        if not any(leaf in group for group in groups):
            groups.append([leaf])
    if len(groups) != 1:
        print("WARNING: sampling_groups returned more than one group, which is currently unsupported")
    return groups

def count_lineages(tree, time):
    """
    Return the number of nodes at a certain time,
    accounting for sampling groups.
    """
    if time > tree.time:
        raise Exception("Time must be after the tree time")
    for group in sampling_groups(tree):
        if (group[0].time - 0.01) <= time <= (group[0].time + 0.01):
            # TODO this won't hold up if we have more than one group since we should also add
            # anything else that exists at the time
            return len(group)
    return len([n for n in tree.iter_descendants() if n.time <= time < n.up.time])

def tree_segments(tree):
    """
    Divide a tree into segments based on the location of parent
    nodes.
    """
    node_times = [0]
    for node in tree.traverse():
        if node.children:
            node_times.append(node.time)
    node_times.sort()

    segments = []
    for start, end in zip(node_times, node_times[1:]):
        segments.append((start, end))
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
    if "N0" in params:
        params["N"] = params["N0"]
    for (start, end) in tree_segments(tree):
        params["k"] = count_lineages(tree, start)
        #print(params["k"])
        if params["k"] == 1:
            # TODO we actually need to handle this
            pass
        else:
            branch_likelihood = np.log(probability(params, end-start))
            print(params)
            print(f"  {branch_likelihood}")
            log_likelihood += branch_likelihood
        params["N"] = population(params, end-start)
    return log_likelihood

#
# Find most likely parameter of a tree by trying many possible values and choosing the best
#

def likelihood_surface(tree, population, probability, params):
    """
    The likelihood surface of a tree with a certain model, one ranged parameter,
    and one fixed parameter.

    Parameters:
    pass
      tree        : TimeTree
      population  : con_- lin_- or exp_population
      probability : con_- lin_- or exp_probability
      params      : dictionary with two items
                    one should be an iterable parameter and the other should be fixed
    """
    # Figure out what the parameters are (this is a mess)
    for p in params.keys():
        try:
            iter(params[p])
            ranged_name, ranged = p, params[p]
        except TypeError:
            fixed_name, fixed = p, params[p]

    # Generate a likelihood for each point
    likelihoods = []
    for item in ranged:
        print(f"{ranged_name}: {item}, {fixed_name}: {fixed}")
        lk = tree_likelihood(tree, population, probability, \
                {ranged_name: item, fixed_name: fixed})
        print(f"    {lk}")
        likelihoods.append(lk)

    return likelihoods

if __name__ == "__main__":
    b_range = np.linspace(0, 1000, 10000)
    with open('linear.tre') as file:
        lines = file.readlines()
        test = TimeTree(lines[0])
        """
        for line in lines:
            t = TimeTree(line)
            y = likelihood_surface(t, lin_population, lin_probability, {"N0": 10000, "b": b_range})
            plt.plot(b_range, y)
            plt.show()
        """
