#!/usr/bin/env python3

import random
#from time_tree import TimeTree #TODO: Do I need this?

class Generator:
	def __init__(self, n):
		self.time = 0
		self.leaves = []
		for i in range(n):
			leaf = Leaf(random.choice(["A", "B"]))
			self.leaves.append(leaf)
	
	def step(self):
		if random.random() < 0.15: 
			number_to_pair = 2 # TODO: In the future this could be more maybe 
			sisters = random.sample(self.leaves, k=number_to_pair)
			self.make_sisters(sisters)

	def run(self):
		self.time = 0
		while len(self.leaves) > 1 and self.time < 10000:
			self.step()
			self.time += 1
		return self.leaves[0].name + ":" + str(self.time) + ";"

	def make_sisters(self, sisters):
		name = "("
		last = sisters[len(sisters) - 1]
		for sister in sisters:
			name += sister.name + ":" + str(self.time)
			if sister != last:
				name += ", "
			self.leaves.remove(sister)
		name += ")"

		leaf = Leaf(name)
		self.leaves.append(leaf)

	def find_pair(self):
		first = random.choice(self.leaves)
		second = random.choice(self.leaves)
		while second == first:
			second = random.choice(self.leaves)
		return [first, second]


class Leaf: # TODO: This doesn't need to be a class if it's so bare bones, ugh
	def __init__(self, name):
		self.name = name

	
if __name__ == '__main__':
	g = Generator(10)
	output = g.run()
