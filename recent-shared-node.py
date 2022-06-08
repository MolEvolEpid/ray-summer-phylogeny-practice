#!/usr/bin/env python3

from ete3 import Tree, NodeStyle, TreeStyle

class TimeTree(Tree):
	"""
	TimeTree is an ete3 Tree with timestamps associated with the branch
	lengths. The most recent node is at time 0, and those further back in the tree
	have positive time values so that they can be used in coalescent modeling.

	apply_time_values()
		Based on the branch lengths in the tree, assign time values starting
		from zero at the furthest leaf and increasing backwards in the tree.
		Automatically called on __init__.
	
	all_hosts_infected_node()
		Return the first node where all hosts are infected.

	get_mixed_nodes()
		Create a list of all nodes that have more than one descendent name.

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
			node_dist = self.get_distance(node) 
			node.time = tree_max - node_dist

	def all_hosts_infected_node(self):
		names_overall = set(self.get_leaf_names())
		names_so_far = set()
		for leaf in sorted(self.get_leaves(), key=lambda x: x.time, reverse=True):
			names_so_far.add(leaf.name)
			if names_overall == names_so_far:
				return leaf
		raise TreeError("Could not find any point where all hosts were infected.")

	def get_mixed_nodes(self):
		mixed = []
		for node in self.traverse():
			if len(set(node.get_leaf_names())) > 1:
				mixed.append(node)
		return mixed

	def most_recent_mixed_node(self):
		recent = self
		for node in self.get_mixed_nodes():
			if node.time < recent.time:
				recent = node
		return recent


def get_example_tree(filename):
	t = TimeTree(filename)

	endpoint = NodeStyle()
	endpoint["fgcolor"] = "lightgreen"

	# Best way I can figure out to highlight them right now. It's nowhere near what
	# we want, but I'm not sure the library can do a line at an arbitrary point.
	# One possible way is by adding an extra node in the middle of every relevant
	# branch and coloring from there? I have an earlier commit with an attempt at that.
	most_recent_mixed_node = t.most_recent_mixed_node()
	most_recent_mixed_node.set_style(endpoint)
	all_infected_node = t.all_hosts_infected_node()
	all_infected_node.set_style(endpoint)

	ts = TreeStyle()

	return t, ts

if __name__ == "__main__":
	t, ts = get_example_tree("challenge.nwk")
	t.show(tree_style=ts)

