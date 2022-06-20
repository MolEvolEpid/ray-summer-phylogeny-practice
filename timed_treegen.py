#!/usr/bin/env python3

import math
import random
from ete3 import TreeNode
from coalescence_time import time_until_coalescence


def generate_nodes(k):
    return [TreeNode(name=str(i)) for i in range(k)]


def step(N, k, nodes):
    """
    Based on the current N and k, find the time that the 
    next coalescence should occur and randomly cause
    two lineages to coalesce at that point.
    """
    # shuffle the available nodes and take two to pair
    random.shuffle(nodes)
    n1 = nodes.pop()
    n2 = nodes.pop()

    # give them a common parent and set their times
    next_time = time_until_coalescence(N, k)
    parent = TreeNode()
    for node in [n1, n2]:
        node.dist = next_time
        parent.add_child(node)

    # return the new pile of nodes, as well as
    # how many nodes are now in the sample (k)
    nodes.append(parent)
    return next_time, nodes


def run_constant(k, N):
    """
    Run a coalescent model with a constant population.
        N(t) = N
    """
    nodes = generate_nodes(k)
    while k > 1:
        nodes, next_time = step(N, k, nodes)
        k = len(nodes)
    return nodes[0]


def run_linear(k, alpha, beta):
    """
    Run a coalescent model with a linearly increasing population.
        N(t) = α + βt
    """
    nodes = generate_nodes(k)
    t = 0
    while k > 1:
        N = round(alpha + (beta * t))
        print(N, k)
        next_time, nodes= step(N, k, nodes)
        k = len(nodes)
        t += next_time
    return nodes[0]


def run_exponential(k, N0, r):
    """
    Run a coalescent model with an exponentially increasting population.
        N(t) = N0 * e^rt
    """
    nodes = generate_nodes(k)
    t = 0
    while k > 1:
        N = round(N0 * math.pow(math.e, r * t))
        print(N, k)
        next_time, nodes = step(N, k, nodes)
        k = len(nodes)
        t += next_time
    return nodes[0]
