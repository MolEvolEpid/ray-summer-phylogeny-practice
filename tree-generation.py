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
			leaves.append(Node(i, chr(random.randint(65, 90)), 1))
		return leaves

	def remove_leaf(self, leaf):
		self.leaves.remove(leaf)
		del leaf

	def display_leaf(self, leaf):
		index = self.leaves.index(leaf)
		self.leaves[index].display()

	def make_sisters(self, leaf1, leaf2, dist):
		leaf1.add_sister(leaf2, dist)
		self.remove_leaf(leaf2)


class Node:
	def __init__(self, id, name, dist):
		self.id = id
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
