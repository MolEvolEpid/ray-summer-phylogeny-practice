#!/usr/bin/env python3

from ete3 import Tree

t = Tree("challenge.nwk")

# Return whether a node has descendants with multiple names.
# TODO: For more complex trees I need to check the person, not the name itself.
def is_mixed_node(node):
	if len(set(node.get_leaf_names())) == 1:
		return False
	else:
		return True

# Create a list of all nodes in a tree that satisfy is_mixed_node.
def get_mixed_nodes(tree):
	mixed = []
	for node in tree.traverse():
		if is_mixed_node(node):
			mixed.append(node)
	return mixed

# Add up the branch lengths between the node and the root of
# the tree in order to find the total distance of the node.
def distance_from_root(node):
	dist = node.dist
	for ancestor in node.iter_ancestors():
		dist += ancestor.dist
	return dist

# Return the mixed node with the largest distance from
# the root of the tree
# TODO: This may actually not be working. Test with more trees ASAP.
def most_recent_mixed_node(tree):
	best = [None, 0]
	for node in get_mixed_nodes(tree):
		total_dist = distance_from_root(node)
		if total_dist > best[1]:
			best[0] = node
			best[1] = total_dist
	return best
