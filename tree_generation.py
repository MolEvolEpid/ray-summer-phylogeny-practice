#!/usr/bin/env python3

import numpy as np
from ete3 import TreeNode
from numpy.random import Generator, PCG64
from population_models import con_population

rng = Generator(PCG64())

def generate_nodes(number, start=0, host=""):
    """
    Generate a certain number of numbered nodes, optionally giving each
    a name prefix corresponding to their name.
    """
    nodes = []
    for i in range(start, start+number):
        if host:
            name = prefix + "_" + str(i)
            node = TreeNode(dist=0, name=name)
            # It's not useful to set node.host since it gets exported to text
        else:
            node = TreeNode(dist=0, name=str(i+1))
        nodes.append(node)
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
    nodes = generate_nodes(run_params["k"])
    while len(nodes) > 1:
        coal_time = next_coalescence_time(run_params, pop_model=pop_model)
        nodes = coalescence(nodes, coal_time, run_params, pop_model=pop_model)
    return nodes[0].write(format=1)

def generate_tree_multisample(start_params, sample_time, lineages_added, pop_model=con_population):
    """
    Generate a tree with the specified start parameters, adding in a certain number
    of lineages from a different host at a certain sample time.

    Parameters
      start_params (dict): a dictionary containing the run parameters including k at time 0.
      sample_time (float): the time that additional lineages should be added
      lineages_added (int): the number of additional lineages to add
      pop_model (function): a function that returns the population at a certain time
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
            time = sample_time
            for node in nodes:
                node.dist += diff
            continue
        # Normal coalescence
        else:
            nodes = coalescence(nodes, time, run_params, pop_model=pop_model)

        time += coal_time

    # Return text version of the tree
    return nodes[0].write(format=1)

def generate_tree_multihost(host1_params, host2_params, transmission_time, model="con"):
    """
    Generate a tree with two hosts, each with their own parameters.

    Params:
      host1_params (dict):
        N0 (int): population size
        k (int): starting nodes
      host2_params (dict):
        N0 (int): population size
        k (int): starting nodes
      transmission_time (real): time of transmission
      model (str): Type of model to use - "con", "lin", or "exp"

    Returns:
      t (str): Newick representation of tree
    """
    h1_run = host1_params.copy()
    h2_run = host2_params.copy()

    if model == "con":
        pop_model = con_population
    else:
        raise Exception("I can only run this on a constant model right now.")

    # Generate nodes for each host, keeping them separate for now
    h1_nodes = generate_nodes(h1_run["k"], host="D")
    h2_nodes = generate_nodes(h2_run["k"], host="R", start=h1_run["k"])

    # Run until we have one node left
    while len(h1_nodes + h2_nodes) > 1:
        for nodes in [h1_nodes, h2_nodes]:
            # Do coalescences...?
            # Need to make sure every time whether we've passed over the transmission time
            # And handle it if so
            # But I can't handle it right now
            pass
        coal_time = next_coalescence_time()


def out():
    params = {"N0": 1000, "k": 20}
    with open("tree.out", "w") as treefile:
        treefile.writelines([generate_tree_multisample(params, 500, 20, pop_model=con_population)])

from time_tree import TimeTree
def read():
    with open("tree.out") as treefile:
        nwk = treefile.readline()
        return TimeTree(nwk)

from display_tree import display_tree
if __name__ == "__main__":
    pass
    #out()
    #t = read()

