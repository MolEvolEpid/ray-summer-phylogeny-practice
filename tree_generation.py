#!/usr/bin/env python3

import numpy as np
from ete3 import TreeNode
from numpy.random import Generator, PCG64
from population_models import con_population, lin_population, exp_population

rng = Generator(PCG64())

def con_coalescence(nodes, population, params): # TODO expand with linear and exponential later
    # Time until coalescence occurs
    scale = (2*params["N0"]) / (params["k"]*(params["k"]-1))
    coal_time = rng.exponential(scale=scale)

    # Add distance to all existing nodes to make sure they align
    for n in nodes:
        n.dist += coal_time

    # Choose nodes to pair
    rng.shuffle(nodes)
    n1 = nodes.pop()
    n2 = nodes.pop()

    # Give them a common parent
    parent = TreeNode(dist=0)
    for n in [n1, n2]:
        parent.add_child(n)
    nodes.append(parent)

    # Adjust the population size and k
    params["k"] -= 1
    params["N0"] = population(params, coal_time)

    return nodes

def generate_tree(population, params):
    """
    Create a tree based on the provided parameters.

    Required parameters:
      k
      Any parameters required by probability (generally either N or N0 and another parameter)
    """
    nodes = [TreeNode(dist=0, name=str(i)) for i in range(params["k"])]
    while len(nodes) > 1:
        nodes = con_coalescence(nodes, population, params)
    return nodes[0].write(format=1)

if __name__ == "__main__":
    params = {"N0": 1000, "k": 20}
    t = generate_tree(con_population, params)
