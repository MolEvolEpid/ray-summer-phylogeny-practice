import random
from time_tree import TimeTree

class Generator:
	def __init__(self, tree, n):
		self.tree = tree
		# self.leaves = []
		for i in range(n):
			child = tree.add_child(name=random.choice(["A", "B"]))
			# self.leaves.append(child) # TODO: Do I need this or not?

	def step(self):
		if random.random() < 0.15:
			pair = random.sample(self.tree.get_leaves(), k=2)
			self.make_sisters(pair)

	def make_sisters(self, group):
		first = group[0]
		for sister in group[1:]:
			first.add_sister(sister, dist=1) # TODO: but how does the time translate NOW?!



if __name__ == '__main__':
	t = TimeTree()
	g = Generator(t)
