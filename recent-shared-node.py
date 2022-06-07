#!/usr/bin/env python3

from ete3 import Tree

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
	best = tree
	for node in get_mixed_nodes(tree):
		if node.time < best.time:
			best = node
	return best

# Add a time parameter to each node in the tree reflecting its distance from
# the tips of the tree. The most recent node will have a time of 0, and the
# oldest nodes will have large positive times.
def apply_time_values(tree):
	tree_max = tree.get_farthest_node()[1]
	for node in tree.traverse():
		node_dist = distance_from_root(node)
		node.time = tree_max - node_dist

if __name__ == "__main__":
	t = Tree("challenge.nwk")
	apply_time_values(t)

