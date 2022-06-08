#!/usr/bin/env python3

from ete3 import Tree, NodeStyle, TreeStyle

class TimeTree(Tree):

	"""
	TimeTree is an ete3 Tree with timestamps associated with the branch
	lengths. The most recent node is at time 0, and those further back in the tree
	have positive time values so that they can be used in coalescent modeling.

	populate_times()
		Add a time attribute to each node based on its distance from the tips of 
		the tree (lower is more recent).

	populate_hosts(hosts)
		Add a host attribute to each node based on a dictionary containing
		names and their hosts (read in from a simulator file).

	all_hosts_infected_node()
		Return the first node where all hosts are infected.

	get_mixed_nodes()
		Create a list of all nodes that have more than one descendent name.

	most_recent_mixed_node()
		Return the most recent node that has more than one type of
		descendant, as decided by name.
	"""

	def __init__(self, *args, **kwargs):
		new_kwargs = {}
		for key, value in kwargs.items():
			if key != "hosts":
				new_kwargs[key] = value
		super(TimeTree, self).__init__(*args[:1], **new_kwargs)
		if "hosts" in **kwargs.keys():
			self.populate_hosts(hosts)
		self.populate_times()
		
	def populate_times(self):
		tree_max = self.get_farthest_node()[1]
		for node in self.traverse():
			node_dist = self.get_distance(node) 
			node.time = tree_max - node_dist

	def populate_hosts(self, hosts):
		for node in self.traverse():
			node.host = hosts[node.name]
	
	def get_leaf_hosts(self):
		leaf_hosts = []
		for node in self.traverse():
			if node.is_leaf():
				leaf_hosts.append(node.host)
		return leaf_hosts
				
	def all_hosts_infected_node(self):
		names_overall = set(self.get_leaf_names())
		names_so_far = set()
		# check from the closest (oldest) leaf to the newest one
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
	# TODO: This is a bad way to solve this problem! 
	# What it does now is try to load it as a normal Newick file, and
	# if it can't be done tries to read it in as a sort of Nexus file.
	try:
		t = TimeTree(filename)
	except NewickError:
		newick, hosts = read_simulator_file(filename)
		t = TimeTree(newick, hosts)

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

def read_simulator_file(filename):
	with open(filename) as f:
		newick = f.readline().rstrip()
		rest = list(map(str.rstrip, f.readlines()[1:]))
		hosts = {}
		for entry in rest:
			split = entry.split(" ")
			hosts[split[0]] = int(split[1])
	return newick, hosts

if __name__ == "__main__":
	newick, hosts = read_simulator_file("tree001.txt")

