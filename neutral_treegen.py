#!/usr/bin/env python3

"""
Based on figures 1 and 2 in Nordborg (2000), which give an example of how
coalescence works on a neutral model where no coalescence is more likely
than another.

Nordborg, M. (2000). Coalescent Theory.

Sorry that citation isn't very helpful, I can't find any info about the paper.
It seems to be a part of a university publication, but that's all I have.
"""

import random
import matplotlib.pyplot as plt
import math
import numpy as np
from ete3 import TreeNode

def create_nodes(N):
	nodes = []
	for i in range(N):
		nodes.append(TreeNode(name=str(i)))
	return nodes

def step(nodes, N):
	parents = []
	for node in nodes:
		parent_name = str(random.randint(0, N-1))
		if not parent_name in [parent.name for parent in parents]:
			parent = TreeNode(name=parent_name)
			parents.append(parent)
		else:
			parent = [p for p in parents if p.name == parent_name][0]
			print("just ch se the same parent as another node", parent_name)
		parent.add_child(node)
	return parents

def generate_tree(N):
	times = [0]
	lineages = [N]

	nodes = create_nodes(N)
	current_time = 0
	while len(nodes) > 1:
		nodes = step(nodes, N)
		current_time += 1
		times.append(current_time)
		lineages.append(len(nodes))
	return nodes[0], times, lineages

def plot_lineages(N):
	"""
	Run the generation model and plot how many lineages exist at each timestep.
	"""
	tree, x, y = generate_tree(N)
	plt.plot(x, y)
	plt.show()

def prob_all_lineages_converge(k, N, t):
	"""
	Given k lineages out of N initial lineages, return the probability
	that all the lineages combine at time t and no earlier.
	This is all I can think to do properly. If they could combine in multiple stages,
	everything opens up way past any understanding I have of the situation.
	"""
	# single generation where they coalesce
	success_generation = 1 / math.pow(N, k-1)
	# t-1 generations whete they do not coalesce
	failed_generations = math.pow(1 - success_generation, t-1)

	# multiplied, they give the overall probability of that t
	return failed_generations * success_generation 

def plot_convergence_time(k, N):
	x = np.linspace(0, N)
	y = []
	for t in x:
		y.append(prob_all_lineages_converge(k, N, t))
	plt.plot(x, y)
	plt.show()

if __name__ == "__main__":
	plot_lineages(100)
