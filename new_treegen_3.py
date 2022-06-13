import random
from time_tree import TimeTree

class Generator:
	def __init__(self, tree, n):
		self.tree = tree
		# self.leaves = []
		for i in range(n):
			child = tree.add_child(name=random.choice(["A", "B"]), dist=1)
			# self.leaves.append(child) # TODO: Do I need this or not?

	def step(self):
		if random.random() < 0.15:
			pair = random.sample(self.tree.get_leaves(), k=2)
			self.make_sisters(pair)

	def make_sisters(self, group):
		branch = self.tree.add_child(dist=1)
		for child in group:
			new_dist = child.dist - 1 # TODO: What should 1 actually be? What if child.dist is too low?
			branch.add_child(child=child, dist=new_dist)
			self.tree.remove_child(child)

"""
To add a midpoint, do this:
	Assign what will be the new children to variables
	Call t.add_child(dist=MATH) where math is part of the new distance (half of current time?)
		Or alternately, use 1 and add to the rest of the nodes in the tree so they match?
	This will leave the original children. To remove them, do:
		t.remove_child(a) and t.remove_child(b)
"""


