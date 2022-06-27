#!/usr/bin/env python3

import numpy as np
import random
from ete3 import TreeNode
from time_tree import TimeTree
from numpy.random import Generator, PCG64

def generate_nodes(k):
    return [TreeNode(dist=0, name=str(i)) for i in range(k)]

def con_coalescence(nodes, params):
    # TODO when we have a way to pick from exp and lin dists I can expand this

    # Time until coalescence occurs
    k = len(nodes)
    scale = (2*params["N"]) / (k*(k-1))
    rng = Generator(PCG64())
    coal_time = rng.exponential(scale=scale) # TODO this is the big difference. is my scale right?

    # Choose nodes to pair
    random.shuffle(nodes)
    n1 = nodes.pop()
    n2 = nodes.pop()

    # Assign each node a time so they will be even with each other
    max_len = 0
    for n in [n1, n2]:
        n.len = n.get_farthest_node()[1]
        if n.len > max_len:
            max_len = n.len
    parent = TreeNode(dist=0)
    print(f"\ncoa {coal_time}")
    print(f"max {max_len}")
    for n in [n1, n2]:
        print(f"len {n.len}")
        n.dist = coal_time + max_len - n.len
        print(f"dst {n.dist}")
        parent.add_child(n)
    nodes.append(parent)

    return nodes

def generate_tree(params):
    """
    Create a tree based on the provided parameters.

    Required parameters:
      k
      Any parameters required by probability (generally either N or N0 and another parameter)
    """
    nodes = generate_nodes(params["k"])
    while len(nodes) > 1:
        nodes = con_coalescence(nodes, params)
    return nodes[0].write(format=1)

from tree_likelihood import tree_segments
from plot_coalescence_time import probability_overlay, side_by_side
from population_models import con_probability

def plot_time(params):
    times = []
    for i in range(1000):
        t = TimeTree(generate_tree(params))
        groups = tree_segments(t)
        times.append(groups[0][1]) # time until first coalescence on the tree
    x = np.linspace(0, max(times), 1000)
    y = [con_probability(params, z) for z in x]

    labels = {"type": "Constant", "N": str(params["N"]), "k": str(params["k"])}

    probability_overlay(times, x, y, labels)

if __name__ == "__main__":
    params = {"N": 1000, "k": 20}
    plot_time(params)
    #t = TimeTree(generate_tree({"N": 1000, "k": 20}))
    #t.write(format=1, outfile="out.nwk")
