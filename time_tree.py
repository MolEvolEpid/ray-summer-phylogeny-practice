#!/usr/bin/env python3

# timetree.py
#
# TimeTree is an ete3 Tree wit timestamp[s associated with the branch lengths.
# The most recent node is at time 0, and those closer to the root of the tree
# have larger times. 

from ete3 import Tree

class TimeTree(Tree):

	"""
	populate_times()
		Add a time attribute to each node based on its distance from the tips of 
		the tree (lower is more recent). 
		Run on __init__()

	populate_hosts(hosts)
		Add a host attribute to each node. hosts can either being a dictionary containing
		node names and their hosts or the value None, in which case host will have the
		same value as name.
		NOT run on __init__(), be careful!

	all_hosts_infected_node()
		Return the first node where all hosts are infected.

	get_mixed_nodes()
		Create a list of all nodes that have children of multiple descendant hosts.

	most_recent_mixed_node()
		Return the most recent node that has more than one type of host connected to it.
	"""

	def __init__(self, *args, **kwargs):
		super(TimeTree, self).__init__(*args, **kwargs)
		self.populate_times()

	def populate_times(self):
		tree_max = self.get_farthest_node()[1]
		for node in self.traverse():
			node_dist = self.get_distance(node)
			node.add_feature("time", tree_max - node_dist)

	def populate_hosts(self, hosts):
		if type(hosts) == dict: 
			for node in self.traverse():
				if node.name in hosts:
					node.add_feature("host", hosts[node.name])
		elif hosts == None:
			for node in self.traverse():
				if node.name:
					node.add_feature("host", node.name)
		else:
			raise TreeError("Could not populate hosts. Hosts should be either a dictionary of names and hosts or None.")
	
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
		latest_possible = self.all_hosts_infected_node()
		recent = self
		mixed_nodes = self.get_mixed_nodes()
		if mixed_nodes:
			for node in self.get_mixed_nodes():
				if node.time < recent.time and node.time > latest_possible.time:
					recent = node
			return recent
		else:
			raise TreeError("There are no mixed nodes on the tree.")
