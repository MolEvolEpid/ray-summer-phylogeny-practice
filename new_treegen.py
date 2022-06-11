#!/usr/bin/env python3

import random
from time_tree import TimeTree

class TreeConstructor(object):
	def __init__(self, n):
		self.leaves = []
		self.make_leaves(n)

	def make_leaves(self, n):
		for i in range(n):
			name = random.choice(["A", "B"])
			dist = random.randint(1, 10)
			self.leaves.append(Leaf(name, self, dist, dist))

	def make_sisters(self, leaves, dist):
		name = "("
		lastleaf = leaves[len(leaves) - 1]
		for leaf in leaves:
			if leaf == lastleaf:
				name += leaf.format()
			else:
				name += leaf.format() + ", "
			self.leaves.remove(leaf) #TODO: Is it safe to remove it at this point?
		name += "):" + str(dist)

		dist = random.randint(1, 10)
		action_time = dist + self.time

		self.leaves.append(Node(newname, self, action_time))

	def make_sisters(self, leaf1, leaf2, dist):
		newname = "(" + leaf1.format() + ", " + leaf2.format() + "):" + dist
		self.remove_leaf(leaf1)
		self.remove_leaf(leaf2)

	def remove_leaf(self, leaf):
		self.leaves.remove(leaf)
		leaf.alive = False # will this have adverse effects if I also use alive for natural death? hmm

	def step(self, time):
		for leaf in self.leaves: #TODO: Will this break if something is removed from leaves?
			leaf.step(time)

	def run(self):
		self.time = 0
		while len(self.leaves) > 1:
			self.step(self.time)
			self.time += 1
		return self.leaves[0].format() + ";"


class Leaf(object):
	def __init__(self, name, tree, dist, action_time):
		self.name = name
		self.tree = tree
		self.dist = dist
		self.action_time = action_time 
		self.action = "pair" # TODO: make them able to die later on, whee!
		self.alive = True # extra precaution, may be necessary when they die

	def format(self):
		return self.name + ":" + str(self.dist)

	def step(self, time):
		if not self.alive:
			return
		if time == self.action_time:
			if self.action == "pair": # the only option right now, but that will change
				partner = self
				while partner == self: # TODO: I think this could technically go infinite
					partner == random.choice(self.tree.leaves)
				print(self, "making pair with", partner)
				self.parent.make_sisters(self, partner)

if __name__ == '__main__':
	c = TreeConstructor(10)
	c.run()
