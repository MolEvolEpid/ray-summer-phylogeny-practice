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
from ete3 import TreeNode
import matplotlib.pyplot as plt

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

def likelihood_curve(N):
	# what on earth should the curve be??!?!?!?!?!
	# new idea: start with a bunch of lineages and plot how many there are at
	# different times and maybe that will be something that's even vaguely useful
	pass

def plot_lineages(N):
	tree, x, y = generate_tree(N)
	plt.plot(x, y)
	plt.show()
	print(times)
	print(lineages)

if __name__ == "__main__":
	plot_lineages(100)
