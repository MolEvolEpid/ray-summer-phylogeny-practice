#!/usr/bin/env python3

"""
The plan for what this needs to be:
    It needs to be able to generate trees, for now I should assume that any pairings are equally
    likely.

    I want all things to start at the same time (time zero).

    I want to be able to make the branch lengths based on a constant population model,
    but also have a decent way to expand it to a linear or exponential model.
        Emma said I should randomly choose from the exponential distribution which has a mean of 
        1/lambda or something. I honestly don't totally know at all.

        But do NOT use the time_until_next() function!!! I need the continuous version, essentially
"""

import numpy as np
import random
from ete3 import TreeNode
from numpy.random import Generator, PCG64
from operator import attrgetter

def generate_nodes(k):
    return [TreeNode(dist=0, name=str(i)) for i in range(k)]

def con_coalescence(nodes, params): # when we have a way to pick from exp and lin dists I can expand this
    # Time until coalescence occurs
    k = len(nodes)
    scale = (2*params["N"]) / (k*(k-1))
    rng = Generator(PCG64()) # TODO this could go outside the function but idk if it should or not
    coal_time = rng.exponential(scale=scale)

    # Choose nodes to pair
    random.shuffle(nodes)
    n1 = nodes.pop()
    n2 = nodes.pop()

    # Assign each node a time so they will be even with each other
    ## Find the max len
    max_len = 0
    for n in [n1, n2]:
        n.len = n.get_farthest_node()[1]
        if n.len > max_len:
            max_len = n.len
    ## Scale each node's dist
    parent = TreeNode(dist=0)
    for n in [n1, n2]:
        n.dist = coal_time + max_len - n.len
        parent.add_child(n) 
    nodes.append(parent)

    return nodes

def create_tree(params):
    """
    Create a tree based on the provided parameters.

    Required parameters:
      k
      Any parameters required by probability (generally either N or N0 and another parameter)
    """
    nodes = generate_nodes(params["k"]) # TODO we never use params["k"] again to generate so it should stay the same
    while len(nodes) > 1:
        nodes = con_coalescence(nodes, params)
    return nodes[0]

if __name__ == "__main__":
    t = create_tree({"N": 1000, "k": 20})
    t.write(format=1, outfile="out.nwk") 
