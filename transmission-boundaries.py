#!/usr/bin/env python3

from ete3 import NodeStyle, TreeStyle
from timetree import TimeTree

def custom_tree_style(tree):
	startpoint = tree.most_recent_mixed_node()
	endpoint = tree.all_hosts_infected_node()

	highlight = NodeStyle()
	highlight["fgcolor"] = "lightgreen"
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
	newick, hosts = read_simulator_file("challenge.nwk")
	t = TimeTree(newick)
	t.populate_hosts(hosts)

	ts = custom_tree_style(t)
	t.show(tree_style=ts)
