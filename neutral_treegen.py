#!/usr/bin/env python3

import random
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
		parent.add_child(node)
	return parents

def generate_tree(N):
	nodes = create_nodes(N)
	while len(nodes) > 1:
		nodes = step(nodes, N)
	return nodes[0]

if __name__ == "__main__":
	end = generate_tree(10)
	end.show()

	# This will falsely show chains of single parents (like 1-3-3-2-5-9) as a straight
	# line, but that' less important. I think it's following Nordborg's diagram
	# otherwise, especially how there is more coalescence closer to time 0.
	#
	# This makes sense, as N never goes down (1/N never goes up) but there are 
	# fewer nodes to potentially coalesce as the model progresses. Is that a false 
	# understanding, or is it what actually happens?
