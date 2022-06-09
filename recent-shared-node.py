#!/usr/bin/env python3

from ete3 import NodeStyle, TreeStyle
from timetree import TimeTree

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
