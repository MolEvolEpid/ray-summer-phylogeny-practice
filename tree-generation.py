#!/usr/bin/env python3

import random

# NewTree(n)
# Create a tree with n leaves.
class NewTree:
	"""
	generate_leaves(n)
		Create a list of leaves with sequential ids and random names. For
		the moment, all leaves will have a dist of one.
	
	remove_leaf(leaf)
		Delete a leaf from the list of leaves, and also deallocate it.

	display_leaf(leaf)
		Call a certain leaf's display function. 

	make_sisters(leaf1, leaf2, dist)
		Combine two leaves into one, renaming them in newick format and applying
		dist to them.
	"""

	#TODO: Display should be different
	def __init__(self, n):
		self.leaves = self.generate_leaves(n) # TODO: This will only happen once, RIGHT? RIGHT?!

	def generate_leaves(self, n):
		leaves = []
		for i in range(n):
			leaves.append(Node(chr(random.randint(65, 90))))
		return leaves

	def remove_leaf(self, leaf):
		self.leaves.remove(leaf)
		del leaf

	def display_leaves(self):
		leaves = []
		for leaf in self.leaves:
			leaves.append(leaf.display())
		return leaves
	
	def make_sisters(self, leaf1, leaf2, dist=1):
		leaf1.add_sister(leaf2, dist)
		self.remove_leaf(leaf2)

	def timestep(self):
		for node in self.leaves:
			if random.random() < 0.15:
				sister = node
				while sister == node:
					sister = random.choice(self.leaves)
				self.make_sisters(node, sister) 

	def run(self):
		while len(self.leaves) > 1:
			self.timestep()
			print(self.display_leaves())
		final_root = self.display_leaves()[0] + ";\n"
		with open('output.nwk', 'w') as output:
			output.write(final_root)

			

class Node:
	def __init__(self, name, dist=1):
		self.name = name
		self.dist = dist

	def display(self):
		return self.name + ":" + str(self.dist)

	def add_sister(self, node, new_dist):
		self.name = "(" + self.display() + ", " + node.display() + ")"
		self.dist = new_dist


if __name__ == '__main__':
	# create a tree with a certain number of nodes
	pass
