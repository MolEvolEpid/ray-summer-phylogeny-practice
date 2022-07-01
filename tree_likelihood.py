#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from time_tree import TimeTree
from tree_generation import generate_tree
from population_models import con_probability, lin_probability, exp_probability, \
        con_population, lin_population, exp_population

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

def within_tolerance(t1, t2):
    """
    Return whether or not two times are close enough to each other
    to be counted as the same sampling group.
    """
    return t1 - 0.3 <= t2 <= t1 + 0.3

def sampling_groups(tree):
    """
    Organize the leaves of a tree by groups sampled at approximately
    the same time to avoid issues with floating point precision.
    """
    groups = []
    for leaf in tree.iter_leaves():
        for group in groups:
            if within_tolerance(group[0].time, leaf.time):
                group.append(leaf)
                break
        # If the leaf isn't in any groups, add it to a new one
        if not any(leaf in group for group in groups):
            groups.append([leaf])
    if len(groups) != 1:
        print(f"WARNING: sampling_groups returned {len(groups)} groups, which is currently unsupported\n{groups}\n")
    return groups

def count_lineages(tree, time):
    """
    Return the number of nodes at a certain time,
    accounting for sampling groups.
    """
    if time > tree.time:
        raise Exception("Time must be after the tree time")
    for group in sampling_groups(tree):
        if within_tolerance(group[0].time, time):
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
        segments.append((start, end, end-start))
    return segments

#
# Log likelihood of an entire tree
#

def tree_likelihood(tree, population, probability, params):
    """
    Return the log likelihood of a certain tree existing
    based on the given population model and probability function.

    Required parameters:
      Any parameters the probability requires besides k
    """
    log_likelihood = 0
    if "N0" in params:
        params["N"] = params["N0"]
    for (start, end, dist) in tree_segments(tree):
        params["k"] = count_lineages(tree, start)
        if params["k"] == 1:
            # TODO we actually need to handle this
            print("WARNING: k was 1")
        else:
            branch_likelihood = np.log(probability(params, dist)) #np.log(probability(params, dist))
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
    # Figure out what the parameters are
    # Will totally break if there is more than one iterable and one non-iterable
    for key in params:
        try:
            iter(params[key])
            ranged_name = key
            ranged = params[key]
        except TypeError:
            fixed_name = key
            fixed = params[key]

    # Generate a likelihood for each point
    likelihoods = []
    for r in ranged:
        print(f"parameter is now {r}")
        lk = tree_likelihood(tree, population, probability, \
                {ranged_name: r, fixed_name: fixed})
        print(f"  {lk}")
        likelihoods.append(lk)
    return likelihoods

def confidence_intervals(likelihood_surface):
    pass

if __name__ == "__main__":
    t = TimeTree(generate_tree(con_population, {"N0": 1000, "k": 20}))
    
    test_params = {"N0": np.linspace(100, 2000, 1000), "fake": 1}
    log_likelihood = likelihood_surface(t, con_population, con_probability, test_params)
    fig, ax = plt.subplots()
    ax.plot(test_params["N0"], log_likelihood)
    plt.show()
    """
    with open("tree_files/linear_fixed.tre") as treefile:
        for line in treefile.readlines():
            t = TimeTree(line)
            fig, ax = plt.subplots()

            # nan-s out after a while
            params1 = {"N0": 1500, "b": np.linspace(100, 10000, 21)}
            linspace = likelihood_surface(t, lin_population, lin_probability, params1)
            params2 = {"N0": 1500, "b": [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]}
            lst = likelihood_surface(t, lin_population, lin_probability, params2)
            
            ax.plot(params1["b"], linspace, color="red")
            ax.plot(params2["b"], lst, color="blue")
            plt.show()
    """
