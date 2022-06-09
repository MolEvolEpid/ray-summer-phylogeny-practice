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
		super(TimeTree, self).__init__(*args, **kwargs)
		self.populate_times()

	def populate_times(self):
		tree_max = self.get_farthest_node()[1]
		for node in self.traverse():
			node_dist = self.get_distance(node) 
			node.time = tree_max - node_dist

	def populate_hosts(self, hosts):
		if type(hosts) == dict: 
			for node in self.traverse():
				if node.name in hosts:
					node.host = hosts[node.name]
		elif hosts == None:
			for node in self.traverse():
				if node.name:
					node.host = node.name
		else:
			raise TimeTreeError("Could not populate hosts. Hosts should be either a dictionary of names and hosts or None.")
	
	def get_leaf_hosts(self):
		leaf_hosts = []
		for node in self.traverse():
			if node.is_leaf():
				leaf_hosts.append(node.host)
		return leaf_hosts

	def all_hosts_infected_node(self):
		hosts_overall = set(self.get_leaf_hosts())
		hosts_so_far = set()
		# check from the closest (oldest) leaf to the newest one
		for leaf in sorted(self.get_leaves(), key=lambda x: x.time, reverse=True):
			hosts_so_far.add(leaf.host)
			if hosts_overall == hosts_so_far:
				return leaf
		raise TreeError("Could not find any point where all hosts were infected.")

	def get_mixed_nodes(self):
		mixed = []
		for node in self.traverse():
			if len(set(node.get_leaf_hosts())) > 1: # TODO: instead of leaf names must be leaf hosts
				mixed.append(node)
		return mixed

	def most_recent_mixed_node(self):
		recent = self
		for node in self.get_mixed_nodes():
			if node.time < recent.time:
				recent = node
		return recent


def get_example_tree(filename):
	newick, hosts = read_simulator_file(filename)
	t = TimeTree(newick)
	t.populate_hosts(hosts)
	
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
		lines = f.readlines()
		newick = lines[0].rstrip()
		if len(lines) > 1:
			rest = list(map(str.rstrip, lines[1:]))
			hosts = {}
			for entry in rest:
				split = entry.split(" ")
				hosts[split[0]] = int(split[1])
		else:
			hosts = None

	return newick, hosts

if __name__ == "__main__":
	t, ts = get_example_tree("tree001.txt")
	t.show(tree_style=ts)
