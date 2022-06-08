#!/usr/bin/env python3

from ete3 import Tree, NodeStyle, TreeStyle

class TimeTree(Tree):
	"""
	TimeTree is an ete3 Tree with timestamps associated with the branch
	lengths. The most recent node is at time 0, and those further back in the tree
	have positive time values so that they can be used in coalescent modeling.

	TODO: Document all of these procedures ASAP

	TODO: Should I move get_mixed_nodes(tree) into here? I think maybe.

	apply_time_values()
		Based on the branch lengths in the tree, assign time values starting
		from zero at the furthest leaf and increasing backwards in the tree.
		Automatically called on __init__.

	get_between_times(start, end)
		Return a list of all nodes between the start and end time specified.

	next_child_time()
		Return the time of the oldest child. Differentiates between nodes on
		the same layer of the tree if they have different times.

	all_infected_node()
		Return the first node where all hosts are infected.

	most_recent_mixed_node()
		Return the most recent node that has more than one type of
		descendant, as decided by name.
	"""

	def __init__(self, *args, **kwargs):
		super(TimeTree, self).__init__(*args, **kwargs)
		self.apply_time_values()
		
	
	def apply_time_values(self):
		tree_max = self.get_farthest_node()[1]
		for node in self.traverse():
			node_dist = distance_from_root(node)
			node.time = tree_max - node_dist
	
	def get_between_times(self, start, end): 
		between = []
		for node in self.traverse():
			if start <= node.time <= end:
				between.append(node)
		return between

	def next_child_time(self):
		times = []
		for child in self.children:
			times.append(child.time)
		return max(times)

	def all_infected_node(self):
		names_so_far = set()
		names_overall = set(self.

	def most_recent_mixed_node(self):
		recent = self
		for node in get_mixed_nodes(self):
			if node.time < recent.time:
				recent = node
		return recent

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

def get_example_tree(filename):
	t = TimeTree(filename)

	point = NodeStyle()
	point["fgcolor"] = "lightgreen"
	point["shape"] = "square" 

	most_recent_mixed_node = t.most_recent_mixed_node()
	most_recent_mixed_node.set_style(point)

	all_infected_node = t.all_infected_node()
	all_infected_node.set_style(point)

	ts = TreeStyle()

	return t, ts

if __name__ == "__main__":
	t, ts = get_example_tree("challenge.nwk")
	t.show(tree_style=ts)

