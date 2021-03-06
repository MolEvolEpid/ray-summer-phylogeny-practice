#!/usr/bin/env python3

from ete3 import NodeStyle, TreeStyle, RectFace
from time_tree import TimeTree
import sys
import os.path

def custom_tree_style(tree):
	"""
	Given a TimeTree object, iterate through the nodes and
	place a red dot on the most recent mixed node and the node
	where all hosts are infected. Return a TreeStyle containing
	these changes.
	"""
	startpoint = tree.most_recent_mixed_node()
	endpoint = tree.all_hosts_infected_node()
	
	highlight = NodeStyle()
	highlight["fgcolor"] = "red"
	hidden = NodeStyle()
	hidden["size"] = 0
	
	for node in tree.traverse():
		if node == startpoint or node == endpoint:
			node.set_style(highlight)
		else:
			node.set_style(hidden)
	ts = TreeStyle()
	
	return ts

def read_simulator_file(filename):
	"""
	Read a simulator file in order to extract the newick file from it
	(the first line) and the host information if available (any subsequent lines).
	"""
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
	"""
	Call the file from the command line with a relative filename in order to 
	draw a tree based on that file.
	"""
	if len(sys.argv) > 1:
		if os.path.exists(sys.argv[1]):
			newick, hosts = read_simulator_file(sys.argv[1])
			t = TimeTree(newick)
			t.populate_hosts(hosts)

			ts = custom_tree_style(t)
			t.show(tree_style=ts)
		else:
			raise Exception("The provided file cannot be accessed.")
	else:
		raise Exception("This script should be run with the relative path of a newick file as the first argument.")
