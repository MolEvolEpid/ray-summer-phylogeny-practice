#!/usr/bin/env python3

from ete3 import Tree, NodeStyle, TreeStyle

# Create a list of all nodes in a tree that satisfy is_mixed_node.
def get_mixed_nodes(tree):
	mixed = []
	for node in tree.traverse():
		if len(set(node.get_leaf_names())) > 1:
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

# TODO: How can this work?
# It should put a node (possibly with some title) at every branch of the tree
# in the same spot. I could do this by going to the root of the tree and
# adding a node to every branch (child) from there -- it would need to be recursive.
#	If THIS area contains the right time put a node there
#	Otherwise ask your children to check the same thing
#	If you're past the time throw an error or something, that shouldn't happen the way I just described it
def insert_node_at_time(tree, time): #TODO: Does it need to be a tree, or is it just any node?
	start_point = tree.time
	possible_end_points = []
	for child in tree.children:
		possible_end_points.append(child.time)
	end_point = min(possible_end_points)
	
	if start_point >= time and time > end_point: 
		print("IDK what to do but it should go here", tree, start_point, time, end_point)
	else:
		for child in tree.children:
			insert_node_at_time(child, time)

def get_example_tree():
	t = Tree("challenge.nwk")
	apply_time_values(t)

	point = NodeStyle()
	point["fgcolor"] = "lightgreen"
	point["shape"] = "square" 

	recent = most_recent_mixed_node(t)
	recent.set_style(point)

	ts = TreeStyle()

	return t, ts

if __name__ == "__main__":
	t, ts = get_example_tree()
	# t.render("it_not_work.png", w=400, tree_style=ts)
	t.show(tree_style=ts)

