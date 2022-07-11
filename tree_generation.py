#!/usr/bin/env python3

import numpy as np
from ete3 import TreeNode
from numpy.random import Generator, PCG64
from population_models import con_population

rng = Generator(PCG64())

def generate_nodes(number, prefix=""):
    nodes = []
    for i in range(number):
        if prefix:
            node_name = prefix + "_" + str(i)
        else:
            node_name = str(i)
        nodes.append(TreeNode(dist=0, name=node_name))
    return nodes

def next_coalescence_time(params, pop_model=con_population):
    if pop_model == con_population:
        scale = (2*params["N0"]) / (params["k"]*(params["k"]-1))
        return rng.exponential(scale=scale)
    else:
        # The rest of it should be general enough, but I have no way to do the rest
        # right now.
        raise Exception("The generator only works on constant population right now.")

def coalescence(nodes, coal_time, params, pop_model=con_population): # TODO expand with linear and exponential later
    # Add distance to all existing nodes
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
    params["N0"] = pop_model(params, coal_time)

    return nodes

def generate_tree(params, pop_model=con_population):
    """
    Create a tree based on the provided parameters.

    Parameters
      params (dict):  a dictionary with run parameters (k, N0, and sometimes n or b)
      pop_model (function): a function that gives the population at a certain time

    Output
      tree (str): the newick representation of a tree
    """
    run_params = params.copy() # Create a single use copy in case we run multiple times
    nodes = [TreeNode(dist=0, name=str(i)) for i in range(run_params["k"])]
    while len(nodes) > 1:
        nodes = coalescence(nodes, population, run_params)
    return nodes[0].write(format=1)

def generate_tree_multisample(start_params, sample_time, lineages_added, pop_model=con_population):
    """
    Generate a tree with the specified start parameters, adding in a certain number
    of lineages from a different host at a certain sample time.
    """
    run_params = start_params.copy() # Don't overwrite the original

    # Initial node generation
    nodes = generate_nodes(run_params["k"], prefix="D")

    # Run until we have one node left
    time = 0
    while len(nodes) > 1:
        coal_time = next_coalescence_time(run_params, pop_model=pop_model)
        # Coalescence at this exact time 
        if time == sample_time: 
            print(f"Adding in {lineages_added} nodes at {time}")
            # TODO even though we give them a new name, we don't treat them differently atm 
            new_nodes = generate_nodes(lineages_added, prefix="R")
            nodes += new_nodes
            run_params["k"] += lineages_added
        # Coalescence occured during coal_time
        elif time < sample_time < time + coal_time:
            # Fast forward to the coalescence time
            print(f"Passed over sample time, fast-forwarding model from {time} to {sample_time}")
            diff = sample_time - time
            time += diff
            for node in nodes:
                node.dist += diff
            continue
        # Normal coalescence
        else:
            nodes = coalescence(nodes, time, run_params, pop_model=pop_model)

        time += coal_time

    # Return text version of the tree
    return nodes[0].write(format=1)

from display_tree import display_tree
from time_tree import TimeTree
if __name__ == "__main__":
    params = {"N0": 500, "k": 20}
    t = TimeTree(generate_tree_multisample(params, 500, 20, pop_model=con_population))
    display_tree(t)
